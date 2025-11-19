"""
WebSocket Service
=================
Real-time communication with Flask-SocketIO
"""

from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
import time
from datetime import datetime, timezone

# Initialize SocketIO (will be attached to app in main.py)
socketio = SocketIO(
    cors_allowed_origins="*", async_mode="threading", logger=True, engineio_logger=False
)

# Track active connections
active_connections = {}


@socketio.on("connect")
def handle_connect():
    """Handle client connection"""
    session_id = request.args.get("session_id", "anonymous")

    active_connections[request.sid] = {
        "session_id": session_id,
        "connected_at": time.time(),
        "ip": request.remote_addr,
    }

    print(f"✅ WebSocket connected: {request.sid} (session: {session_id})")

    emit(
        "connected",
        {
            "message": "Connected to NovaHouse Chatbot",
            "sid": request.sid,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection"""
    if request.sid in active_connections:
        session_id = active_connections[request.sid]["session_id"]
        del active_connections[request.sid]
        print(f"❌ WebSocket disconnected: {request.sid} (session: {session_id})")


@socketio.on("join")
def handle_join(data):
    """Join a room (for targeted broadcasts)"""
    room = data.get("room")
    if room:
        join_room(room)
        emit("joined", {"room": room}, room=request.sid)
        print(f"🚪 {request.sid} joined room: {room}")


@socketio.on("leave")
def handle_leave(data):
    """Leave a room"""
    room = data.get("room")
    if room:
        leave_room(room)
        emit("left", {"room": room}, room=request.sid)
        print(f"🚪 {request.sid} left room: {room}")


@socketio.on("chat_message")
def handle_chat_message(data):
    """Handle incoming chat message"""
    session_id = data.get("session_id")
    message = data.get("message")
    data.get("user_id", "anonymous")

    print(f"💬 Message from {session_id}: {message}")

    # Emit to user's room (for their own clients)
    emit(
        "message_received",
        {
            "session_id": session_id,
            "message": message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "received",
        },
        room=request.sid,
    )

    # Process message with chatbot AI
    try:
        from src.routes.chatbot import process_chat_message

        result = process_chat_message(message, session_id)

        emit(
            "bot_response",
            {
                "session_id": session_id,
                "response": result.get("response", "Przepraszam, wystąpił błąd."),
                "conversation_id": result.get("conversation_id"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            room=request.sid,
        )

    except Exception as e:
        print(f"❌ WebSocket AI processing error: {e}")
        emit(
            "bot_response",
            {
                "session_id": session_id,
                "response": "Przepraszam, wystąpił problem z przetwarzaniem wiadomości. Spróbuj ponownie.",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": True,
            },
            room=request.sid,
        )


@socketio.on("typing")
def handle_typing(data):
    """Handle typing indicator"""
    session_id = data.get("session_id")
    is_typing = data.get("is_typing", False)

    # Broadcast to admins monitoring this session
    socketio.emit(
        "user_typing",
        {
            "session_id": session_id,
            "is_typing": is_typing,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        room="admin",
    )


@socketio.on("ping")
def handle_ping():
    """Heartbeat ping"""
    emit("pong", {"timestamp": time.time()})


# Helper functions for server-side emits


def broadcast_analytics_update(data: dict):
    """Broadcast analytics update to all admin clients"""
    socketio.emit("analytics_update", data, room="admin")


def broadcast_new_lead(lead_data: dict):
    """Broadcast new lead notification to admins"""
    socketio.emit(
        "new_lead",
        {"lead": lead_data, "timestamp": datetime.now(timezone.utc).isoformat()},
        room="admin",
    )


def send_notification_to_user(session_id: str, notification: dict):
    """Send notification to specific user session"""
    socketio.emit("notification", notification, room=session_id)


def broadcast_system_message(message: str, level: str = "info"):
    """Broadcast system message to all connected clients"""
    socketio.emit(
        "system_message",
        {"message": message, "level": level, "timestamp": datetime.now(timezone.utc).isoformat()},
    )


def get_active_connections_count() -> int:
    """Get number of active WebSocket connections"""
    return len(active_connections)


def get_active_connections_list() -> list:
    """Get list of active connections"""
    return [
        {
            "sid": sid,
            "session_id": info["session_id"],
            "connected_at": info["connected_at"],
            "duration": time.time() - info["connected_at"],
            "ip": info["ip"],
        }
        for sid, info in active_connections.items()
    ]
