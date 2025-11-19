"""
File Upload Service
===================
Image upload, optimization, and cloud storage
"""

import hashlib
import io
import os
from datetime import datetime, timezone

from google.cloud import storage
from PIL import Image
from werkzeug.utils import secure_filename

# Allowed extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Image sizes
THUMBNAIL_SIZE = (150, 150)
MEDIUM_SIZE = (800, 800)
LARGE_SIZE = (1920, 1920)


class FileUploadService:
    """Handle file uploads with optimization and cloud storage"""

    def __init__(self):
        self.gcs_bucket = os.getenv("GCS_BUCKET_NAME", "novahouse-uploads")
        self.local_upload_folder = os.getenv("UPLOAD_FOLDER", "uploads")
        self.use_gcs = os.getenv("USE_CLOUD_STORAGE", "false").lower() == "true"

        # Create local folder if not exists
        if not self.use_gcs:
            os.makedirs(self.local_upload_folder, exist_ok=True)

        # Initialize GCS client if enabled
        if self.use_gcs:
            try:
                self.storage_client = storage.Client()
                self.bucket = self.storage_client.bucket(self.gcs_bucket)
                print(f"✅ Google Cloud Storage connected: {self.gcs_bucket}")
            except Exception as e:
                print(f"⚠️ GCS unavailable, using local storage: {e}")
                self.use_gcs = False
                os.makedirs(self.local_upload_folder, exist_ok=True)

    def allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def validate_mime_type(self, file_bytes: bytes) -> bool:
        """
        SECURITY: Validate actual MIME type, not just extension
        Prevents shell scripts disguised as images
        """
        try:
            # Check magic bytes for real image format
            if file_bytes[:4] == b"\x89PNG":
                return True  # PNG
            elif file_bytes[:3] == b"\xff\xd8\xff":
                return True  # JPEG
            elif file_bytes[:6] in (b"GIF87a", b"GIF89a"):
                return True  # GIF
            elif file_bytes[:4] == b"RIFF" and file_bytes[8:12] == b"WEBP":
                return True  # WEBP
            return False
        except:
            return False

    def generate_filename(self, original_filename: str, prefix: str = "") -> str:
        """Generate unique filename with timestamp and hash"""
        ext = original_filename.rsplit(".", 1)[1].lower()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        random_hash = hashlib.md5(f"{original_filename}{timestamp}".encode()).hexdigest()[:8]

        if prefix:
            return f"{prefix}_{timestamp}_{random_hash}.{ext}"
        return f"{timestamp}_{random_hash}.{ext}"

    def optimize_image(self, image: Image.Image, max_size: tuple, quality: int = 85) -> Image.Image:
        """Optimize image: resize and compress"""
        # Convert RGBA to RGB if needed
        if image.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(
                image, mask=image.split()[-1] if image.mode in ("RGBA", "LA") else None
            )
            image = background

        # Resize if larger than max_size
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        return image

    def create_variants(self, image_bytes: bytes, filename: str) -> dict:
        """Create thumbnail, medium, and large variants"""
        try:
            # Load image
            image = Image.open(io.BytesIO(image_bytes))

            # Get original dimensions
            original_width, original_height = image.size

            # Create variants
            variants = {}

            # Thumbnail
            thumb = self.optimize_image(image.copy(), THUMBNAIL_SIZE, quality=80)
            thumb_io = io.BytesIO()
            thumb.save(thumb_io, format="JPEG", quality=80, optimize=True)
            thumb_io.seek(0)
            variants["thumbnail"] = {
                "bytes": thumb_io.getvalue(),
                "size": thumb.size,
                "filename": f"thumb_{filename}",
            }

            # Medium
            medium = self.optimize_image(image.copy(), MEDIUM_SIZE, quality=85)
            medium_io = io.BytesIO()
            medium.save(medium_io, format="JPEG", quality=85, optimize=True)
            medium_io.seek(0)
            variants["medium"] = {
                "bytes": medium_io.getvalue(),
                "size": medium.size,
                "filename": f"medium_{filename}",
            }

            # Large (original optimized)
            large = self.optimize_image(image.copy(), LARGE_SIZE, quality=90)
            large_io = io.BytesIO()
            large.save(large_io, format="JPEG", quality=90, optimize=True)
            large_io.seek(0)
            variants["large"] = {
                "bytes": large_io.getvalue(),
                "size": large.size,
                "filename": f"large_{filename}",
            }

            return variants

        except Exception as e:
            print(f"Error creating variants: {e}")
            return {}

    def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        folder: str = "general",
        create_variants: bool = True,
    ) -> dict:
        """
        Upload file with optional variants

        Returns:
            dict with URLs for each variant
        """
        try:
            # SECURITY: Validate file extension
            if not self.allowed_file(filename):
                raise ValueError(f"File type not allowed. Allowed: {ALLOWED_EXTENSIONS}")

            # SECURITY: Validate actual MIME type (prevent disguised files)
            if not self.validate_mime_type(file_bytes):
                raise ValueError("Invalid image file. File content does not match image format.")

            # SECURITY: Check file size
            if len(file_bytes) > MAX_FILE_SIZE:
                raise ValueError(f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB")

            # Generate unique filename
            secure_name = secure_filename(filename)
            unique_filename = self.generate_filename(secure_name, prefix=folder)

            result = {
                "original": None,
                "thumbnail": None,
                "medium": None,
                "large": None,
                "metadata": {
                    "original_filename": filename,
                    "uploaded_at": datetime.now(timezone.utc).isoformat(),
                    "folder": folder,
                },
            }

            # Create image variants if enabled
            variants = {}
            if create_variants and self.allowed_file(filename):
                variants = self.create_variants(file_bytes, unique_filename)

            # Upload to GCS or local
            if self.use_gcs:
                # Upload original
                result["original"] = self._upload_to_gcs(file_bytes, f"{folder}/{unique_filename}")

                # Upload variants
                for variant_name, variant_data in variants.items():
                    result[variant_name] = self._upload_to_gcs(
                        variant_data["bytes"], f"{folder}/{variant_data['filename']}"
                    )
            else:
                # Save to local
                result["original"] = self._save_to_local(file_bytes, f"{folder}/{unique_filename}")

                # Save variants
                for variant_name, variant_data in variants.items():
                    result[variant_name] = self._save_to_local(
                        variant_data["bytes"], f"{folder}/{variant_data['filename']}"
                    )

            return result

        except Exception as e:
            print(f"Upload error: {e}")
            return {"error": str(e)}

    def _upload_to_gcs(self, file_bytes: bytes, blob_name: str) -> str:
        """Upload to Google Cloud Storage"""
        try:
            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(file_bytes, content_type="image/jpeg")
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print(f"GCS upload error: {e}")
            raise

    def _save_to_local(self, file_bytes: bytes, filepath: str) -> str:
        """Save to local filesystem"""
        try:
            full_path = os.path.join(self.local_upload_folder, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "wb") as f:
                f.write(file_bytes)

            # Return relative URL
            return f"/uploads/{filepath}"
        except Exception as e:
            print(f"Local save error: {e}")
            raise

    def delete_file(self, file_url: str) -> bool:
        """Delete file from storage"""
        try:
            if self.use_gcs:
                # Extract blob name from URL
                blob_name = file_url.split(f"{self.gcs_bucket}/")[-1]
                blob = self.bucket.blob(blob_name)
                blob.delete()
            else:
                # Delete local file
                filepath = file_url.replace("/uploads/", "")
                full_path = os.path.join(self.local_upload_folder, filepath)
                if os.path.exists(full_path):
                    os.remove(full_path)
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False


# Global instance
file_upload_service = FileUploadService()
