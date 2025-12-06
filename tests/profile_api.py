#!/usr/bin/env python3
"""
Performance Profiling Tool for NovaHouse Chatbot API
Identifies bottlenecks and slow code paths

Usage:
    python profile_api.py                    # Profile main routes
    python profile_api.py --endpoint chatbot # Profile specific endpoint
    python profile_api.py --full             # Full app profiling
"""

import cProfile
import io
import pstats
import sys
from pathlib import Path
from pstats import SortKey

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def profile_chatbot_endpoint():
    """Profile chatbot message processing"""
    from flask import Flask
    from src.routes.chatbot import chatbot_bp

    app = Flask(__name__)
    app.register_blueprint(chatbot_bp)

    with app.test_client() as client:
        profiler = cProfile.Profile()
        profiler.enable()

        # Simulate requests
        for _ in range(100):
            client.post(
                "/api/chatbot/message",
                json={"message": "Jakie są ceny projektów?", "session_id": "test-session"},
            )

        profiler.disable()
        return profiler


def profile_search_endpoint():
    """Profile knowledge base search"""
    from flask import Flask
    from src.routes.search import search_bp

    app = Flask(__name__)
    app.register_blueprint(search_bp)

    with app.test_client() as client:
        profiler = cProfile.Profile()
        profiler.enable()

        # Simulate searches
        for query in ["projekt", "cena", "realizacja", "technologia"]:
            for _ in range(25):
                client.get(f"/api/knowledge/search?query={query}")

        profiler.disable()
        return profiler


def profile_analytics_endpoint():
    """Profile analytics aggregation"""
    from flask import Flask
    from src.routes.analytics import analytics_bp

    app = Flask(__name__)
    app.register_blueprint(analytics_bp)

    with app.test_client() as client:
        profiler = cProfile.Profile()
        profiler.enable()

        # Simulate analytics queries
        for _ in range(50):
            client.get("/api/analytics/summary")
            client.get("/api/analytics/detailed")

        profiler.disable()
        return profiler


def profile_full_app():
    """Profile entire application startup and basic flow"""
    profiler = cProfile.Profile()
    profiler.enable()

    # Import and initialize app
    from src.main import app

    with app.test_client() as client:
        # Simulate typical user journey
        client.get("/api/health")
        client.get("/api/knowledge/search?query=projekt")
        client.post(
            "/api/chatbot/message", json={"message": "Witam", "session_id": "profile-session"}
        )
        client.get("/api/analytics/summary")

    profiler.disable()
    return profiler


def print_profile_stats(profiler, title, top_n=30):
    """Print formatted profiling statistics"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")

    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(top_n)

    print(s.getvalue())

    # Print additional insights
    print(f"\n{'─' * 80}")
    print("📊 Top Time-Consuming Functions (by cumulative time):")
    print(f"{'─' * 80}\n")

    s2 = io.StringIO()
    ps2 = pstats.Stats(profiler, stream=s2).sort_stats(SortKey.TIME)
    ps2.print_stats(15)

    # Extract just function names
    lines = s2.getvalue().split("\n")
    for line in lines[5:20]:  # Skip header
        if line.strip():
            print(line)


def main():
    """Main profiling entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Profile NovaHouse Chatbot API")
    parser.add_argument(
        "--endpoint",
        choices=["chatbot", "search", "analytics", "all"],
        default="all",
        help="Endpoint to profile",
    )
    parser.add_argument("--full", action="store_true", help="Profile full application")
    parser.add_argument("--output", help="Save profile to file (use with snakeviz)")
    parser.add_argument("--top", type=int, default=30, help="Number of top functions to show")

    args = parser.parse_args()

    print("🔍 NovaHouse Chatbot API Performance Profiler")
    print("=" * 80)

    if args.full:
        profiler = profile_full_app()
        print_profile_stats(profiler, "Full Application Profile", args.top)
    elif args.endpoint == "all":
        print("\n📌 Profiling all endpoints...\n")

        profilers = [
            (profile_chatbot_endpoint(), "Chatbot Endpoint"),
            (profile_search_endpoint(), "Search Endpoint"),
            (profile_analytics_endpoint(), "Analytics Endpoint"),
        ]

        for profiler, title in profilers:
            print_profile_stats(profiler, title, args.top)
    else:
        endpoint_map = {
            "chatbot": (profile_chatbot_endpoint, "Chatbot Endpoint"),
            "search": (profile_search_endpoint, "Search Endpoint"),
            "analytics": (profile_analytics_endpoint, "Analytics Endpoint"),
        }

        func, title = endpoint_map[args.endpoint]
        profiler = func()
        print_profile_stats(profiler, title, args.top)

    # Save profile if requested
    if args.output:
        profiler.dump_stats(args.output)
        print(f"\n💾 Profile saved to: {args.output}")
        print(f"   View with: snakeviz {args.output}")

    print("\n✅ Profiling complete!")
    print("\n💡 Tips:")
    print("   • Focus on functions with high cumulative time")
    print("   • Look for unexpected calls or loops")
    print("   • Use --output to save and visualize with snakeviz")
    print("   • Install snakeviz: pip install snakeviz")


if __name__ == "__main__":
    main()
