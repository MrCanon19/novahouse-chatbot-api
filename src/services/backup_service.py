"""
Backup & Export Service
=======================
Automated backups and RODO-compliant data export
"""

import csv
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List


class BackupService:
    """Automated backup and data export"""

    def __init__(self):
        # Use /tmp for App Engine (only writable directory)
        # In production, backups should be moved to Google Cloud Storage
        if os.environ.get("GAE_ENV", "").startswith("standard"):
            # Running on App Engine - use /tmp
            self.backup_dir = "/tmp/backups"
        else:
            # Local development - use project directory
            self.backup_dir = os.path.join(
                os.path.dirname(__file__), "..", "..", "backups", "automated"
            )

        os.makedirs(self.backup_dir, exist_ok=True)

    def export_all_data(self, format: str = "json") -> str:
        """
        Export all database data

        Args:
            format: 'json' or 'csv'

        Returns:
            File path to exported data
        """
        try:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

            if format == "json":
                return self._export_json(timestamp)
            elif format == "csv":
                return self._export_csv(timestamp)
            else:
                raise ValueError(f"Unsupported format: {format}")

        except Exception as e:
            print(f"❌ Export failed: {e}")
            raise

    def _export_json(self, timestamp: str) -> str:
        """Export to JSON format"""
        from src.models.analytics import Analytics, Booking, Lead
        from src.models.chatbot import ChatSession, Message
        from src.models.user import User

        data = {
            "export_date": datetime.now(timezone.utc).isoformat(),
            "version": "2.2",
            "tables": {},
        }

        # Export Users
        users = User.query.all()
        data["tables"]["users"] = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ]

        # Export Chat Sessions
        sessions = ChatSession.query.all()
        data["tables"]["chat_sessions"] = [
            {
                "id": s.id,
                "session_id": s.session_id,
                "status": s.status,
                "language": s.language,
                "rating": s.rating,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "last_activity": s.last_activity.isoformat() if s.last_activity else None,
            }
            for s in sessions
        ]

        # Export Messages
        messages = Message.query.all()
        data["tables"]["messages"] = [
            {
                "id": m.id,
                "session_id": m.session_id,
                "sender": m.sender,
                "content": m.content,
                "intent": m.intent,
                "confidence": m.confidence,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ]

        # Export Leads
        leads = Lead.query.all()
        data["tables"]["leads"] = [
            {
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "interested_package": lead.interested_package,
                "budget_range": lead.budget_range,
                "status": lead.status,
                "created_at": lead.created_at.isoformat() if lead.created_at else None,
            }
            for lead in leads
        ]

        # Export Bookings
        bookings = Booking.query.all()
        data["tables"]["bookings"] = [
            {
                "id": b.id,
                "lead_id": b.lead_id,
                "appointment_date": b.appointment_date.isoformat() if b.appointment_date else None,
                "status": b.status,
                "created_at": b.created_at.isoformat() if b.created_at else None,
            }
            for b in bookings
        ]

        # Export Analytics
        analytics = Analytics.query.all()
        data["tables"]["analytics"] = [
            {
                "id": a.id,
                "event_type": a.event_type,
                "event_data": a.event_data,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in analytics
        ]

        # Save to file
        filename = f"backup_{timestamp}.json"
        filepath = os.path.join(self.backup_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON export saved: {filepath}")
        return filepath

    def _export_csv(self, timestamp: str) -> str:
        """Export to CSV format (separate files per table)"""
        from src.models.analytics import Lead
        from src.models.chatbot import ChatSession, Message

        csv_dir = os.path.join(self.backup_dir, f"csv_{timestamp}")
        os.makedirs(csv_dir, exist_ok=True)

        # Export Chat Sessions
        sessions = ChatSession.query.all()
        session_file = os.path.join(csv_dir, "chat_sessions.csv")
        with open(session_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["id", "session_id", "status", "language", "rating", "created_at"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in sessions:
                writer.writerow(
                    {
                        "id": s.id,
                        "session_id": s.session_id,
                        "status": s.status,
                        "language": s.language,
                        "rating": s.rating,
                        "created_at": s.created_at.isoformat() if s.created_at else None,
                    }
                )

        # Export Messages
        messages = Message.query.all()
        msg_file = os.path.join(csv_dir, "messages.csv")
        with open(msg_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["id", "session_id", "sender", "content", "intent", "created_at"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for m in messages:
                writer.writerow(
                    {
                        "id": m.id,
                        "session_id": m.session_id,
                        "sender": m.sender,
                        "content": m.content,
                        "intent": m.intent,
                        "created_at": m.created_at.isoformat() if m.created_at else None,
                    }
                )

        # Export Leads
        leads = Lead.query.all()
        leads_file = os.path.join(csv_dir, "leads.csv")
        with open(leads_file, "w", encoding="utf-8", newline="") as f:
            fieldnames = [
                "id",
                "name",
                "email",
                "phone",
                "interested_package",
                "status",
                "created_at",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for lead in leads:
                writer.writerow(
                    {
                        "id": lead.id,
                        "name": lead.name,
                        "email": lead.email,
                        "phone": lead.phone,
                        "interested_package": lead.interested_package,
                        "status": lead.status,
                        "created_at": (lead.created_at.isoformat() if lead.created_at else None),
                    }
                )

        print(f"✅ CSV export saved: {csv_dir}")
        return csv_dir

    def export_user_data(self, user_identifier: str) -> Dict[str, Any]:
        """
        RODO-compliant: Export all data for specific user

        Args:
            user_identifier: Email, phone, or session_id

        Returns:
            Dictionary with all user data
        """
        try:
            from src.models.analytics import Booking, Lead
            from src.models.chatbot import ChatSession, Message

            user_data = {
                "export_date": datetime.now(timezone.utc).isoformat(),
                "user_identifier": user_identifier,
                "data": {},
            }

            # Find by email
            lead = Lead.query.filter(
                (Lead.email == user_identifier) | (Lead.phone == user_identifier)
            ).first()

            if lead:
                user_data["data"]["personal_info"] = {
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "interested_package": lead.interested_package,
                    "budget_range": lead.budget_range,
                    "created_at": lead.created_at.isoformat() if lead.created_at else None,
                }

                # Get bookings
                bookings = Booking.query.filter_by(lead_id=lead.id).all()
                user_data["data"]["bookings"] = [
                    {
                        "appointment_date": (
                            b.appointment_date.isoformat() if b.appointment_date else None
                        ),
                        "status": b.status,
                        "created_at": (b.created_at.isoformat() if b.created_at else None),
                    }
                    for b in bookings
                ]

            # Find chat sessions
            sessions = ChatSession.query.filter_by(session_id=user_identifier).all()
            if sessions:
                user_data["data"]["chat_sessions"] = []
                for s in sessions:
                    messages = Message.query.filter_by(session_id=s.session_id).all()
                    user_data["data"]["chat_sessions"].append(
                        {
                            "session_id": s.session_id,
                            "created_at": s.created_at.isoformat() if s.created_at else None,
                            "messages": [
                                {
                                    "sender": m.sender,
                                    "content": m.content,
                                    "created_at": (
                                        m.created_at.isoformat() if m.created_at else None
                                    ),
                                }
                                for m in messages
                            ],
                        }
                    )

            return user_data

        except Exception as e:
            print(f"❌ User data export failed: {e}")
            raise

    def delete_user_data(self, user_identifier: str) -> Dict[str, int]:
        """
        RODO-compliant: Delete all data for specific user (Right to be forgotten)

        Args:
            user_identifier: Email, phone, or session_id

        Returns:
            Dictionary with deletion counts
        """
        try:
            from src.database import db
            from src.models.analytics import Booking, Lead
            from src.models.chatbot import ChatSession, Message

            deleted = {"leads": 0, "bookings": 0, "sessions": 0, "messages": 0}

            # Find and delete lead
            lead = Lead.query.filter(
                (Lead.email == user_identifier) | (Lead.phone == user_identifier)
            ).first()

            if lead:
                # Delete bookings
                bookings = Booking.query.filter_by(lead_id=lead.id).all()
                for b in bookings:
                    db.session.delete(b)
                    deleted["bookings"] += 1

                # Delete lead
                db.session.delete(lead)
                deleted["leads"] += 1

            # Find and delete chat sessions
            sessions = ChatSession.query.filter_by(session_id=user_identifier).all()
            for s in sessions:
                # Delete messages
                messages = Message.query.filter_by(session_id=s.session_id).all()
                for m in messages:
                    db.session.delete(m)
                    deleted["messages"] += 1

                # Delete session
                db.session.delete(s)
                deleted["sessions"] += 1

            db.session.commit()

            print(f"✅ User data deleted: {deleted}")
            return deleted

        except Exception as e:
            db.session.rollback()
            print(f"❌ User data deletion failed: {e}")
            raise

    def cleanup_old_backups(self, days_to_keep: int = 30):
        """
        Delete backups older than X days

        Args:
            days_to_keep: Number of days to keep backups (default: 30)

        Returns:
            Number of deleted backups
        """
        try:
            from datetime import timedelta

            deleted_count = 0
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)

            for filename in os.listdir(self.backup_dir):
                if filename.startswith("backup_") and filename.endswith(".json"):
                    filepath = os.path.join(self.backup_dir, filename)

                    # Check file creation time
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath), tz=timezone.utc)

                    if file_time < cutoff_date:
                        os.remove(filepath)
                        deleted_count += 1
                        print(f"🗑️  Deleted old backup: {filename}")

            if deleted_count > 0:
                print(f"✅ Cleaned up {deleted_count} old backup(s)")
            else:
                print(f"✅ No old backups to clean (keeping last {days_to_keep} days)")

            return deleted_count

        except Exception as e:
            print(f"❌ Backup cleanup failed: {e}")
            return 0

    def automated_backup_with_cleanup(self):
        """
        Perform backup and cleanup old files
        This is the main function called by scheduler
        """
        try:
            # Create new backup
            filepath = self.export_all_data(format="json")
            print(f"✅ Automated backup created: {filepath}")

            # Clean up old backups (keep last 30 days)
            self.cleanup_old_backups(days_to_keep=30)

        except Exception as e:
            print(f"❌ Automated backup failed: {e}")

    def schedule_automated_backup(self):
        """
        Schedule daily backup using APScheduler

        Returns:
            Scheduler job
        """
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger

            scheduler = BackgroundScheduler()

            # Daily backup at 3 AM with automatic cleanup
            scheduler.add_job(
                func=self.automated_backup_with_cleanup,
                trigger=CronTrigger(hour=3, minute=0),
                id="daily_backup",
                name="Daily Automated Backup + Cleanup",
                replace_existing=True,
            )

            scheduler.start()
            print("✅ Automated backup scheduled (daily at 3 AM, keeps last 30 days)")

            return scheduler

        except Exception as e:
            print(f"❌ Backup scheduling failed: {e}")
            raise

    def get_backup_list(self) -> List[Dict[str, Any]]:
        """Get list of available backups"""
        backups = []

        for filename in os.listdir(self.backup_dir):
            if filename.startswith("backup_") and filename.endswith(".json"):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)

                backups.append(
                    {
                        "filename": filename,
                        "size": stat.st_size,
                        "created_at": datetime.fromtimestamp(
                            stat.st_ctime, tz=timezone.utc
                        ).isoformat(),
                    }
                )

        return sorted(backups, key=lambda x: x["created_at"], reverse=True)


# Global instance
backup_service = BackupService()
