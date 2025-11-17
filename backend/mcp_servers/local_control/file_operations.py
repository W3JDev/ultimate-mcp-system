"""
File Operations - Safe file system operations
"""

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


class FileOperations:
    """Safe file system operations"""

    def __init__(self):
        """Initialize file operations with safety checks"""
        self.allowed_extensions = {
            ".txt",
            ".json",
            ".csv",
            ".md",
            ".log",
            ".yaml",
            ".yml",
            ".xml",
            ".html",
            ".css",
            ".js",
            ".py",
        }
        self.forbidden_paths = {
            "C:\\Windows",
            "C:\\Program Files",
            "/etc",
            "/sys",
            "/proc",
        }
        logger.info("📁 File operations initialized")

    def read_file(self, path: str) -> Dict[str, Any]:
        """
        Read file contents

        Args:
            path: File path

        Returns:
            File contents
        """
        try:
            if not self._is_path_safe(path):
                raise PermissionError(f"Access denied to path: {path}")

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            logger.info(f"📖 Read file: {path}")
            return {"success": True, "content": content, "path": path}

        except Exception as e:
            logger.error(f"Read file error: {e}")
            return {"success": False, "error": str(e)}

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Write content to file

        Args:
            path: File path
            content: Content to write

        Returns:
            Operation result
        """
        try:
            if not self._is_path_safe(path):
                raise PermissionError(f"Access denied to path: {path}")

            # Create parent directories if needed
            Path(path).parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.info(f"✍️  Wrote file: {path}")
            return {"success": True, "path": path, "bytes_written": len(content)}

        except Exception as e:
            logger.error(f"Write file error: {e}")
            return {"success": False, "error": str(e)}

    def list_directory(self, path: str = ".") -> Dict[str, Any]:
        """
        List directory contents

        Args:
            path: Directory path

        Returns:
            Directory contents
        """
        try:
            if not self._is_path_safe(path):
                raise PermissionError(f"Access denied to path: {path}")

            items = []
            for item in Path(path).iterdir():
                items.append(
                    {
                        "name": item.name,
                        "path": str(item),
                        "is_dir": item.is_dir(),
                        "is_file": item.is_file(),
                        "size": item.stat().st_size if item.is_file() else 0,
                    }
                )

            logger.info(f"📂 Listed directory: {path}")
            return {"success": True, "path": path, "items": items}

        except Exception as e:
            logger.error(f"List directory error: {e}")
            return {"success": False, "error": str(e)}

    def create_directory(self, path: str) -> Dict[str, Any]:
        """
        Create directory

        Args:
            path: Directory path

        Returns:
            Operation result
        """
        try:
            if not self._is_path_safe(path):
                raise PermissionError(f"Access denied to path: {path}")

            Path(path).mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Created directory: {path}")

            return {"success": True, "path": path}

        except Exception as e:
            logger.error(f"Create directory error: {e}")
            return {"success": False, "error": str(e)}

    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete file

        Args:
            path: File path

        Returns:
            Operation result
        """
        try:
            if not self._is_path_safe(path):
                raise PermissionError(f"Access denied to path: {path}")

            Path(path).unlink()
            logger.info(f"🗑️  Deleted file: {path}")

            return {"success": True, "path": path}

        except Exception as e:
            logger.error(f"Delete file error: {e}")
            return {"success": False, "error": str(e)}

    def copy_file(self, src: str, dst: str) -> Dict[str, Any]:
        """
        Copy file

        Args:
            src: Source path
            dst: Destination path

        Returns:
            Operation result
        """
        try:
            if not self._is_path_safe(src) or not self._is_path_safe(dst):
                raise PermissionError("Access denied to path")

            shutil.copy2(src, dst)
            logger.info(f"📋 Copied {src} → {dst}")

            return {"success": True, "src": src, "dst": dst}

        except Exception as e:
            logger.error(f"Copy file error: {e}")
            return {"success": False, "error": str(e)}

    def move_file(self, src: str, dst: str) -> Dict[str, Any]:
        """
        Move file

        Args:
            src: Source path
            dst: Destination path

        Returns:
            Operation result
        """
        try:
            if not self._is_path_safe(src) or not self._is_path_safe(dst):
                raise PermissionError("Access denied to path")

            shutil.move(src, dst)
            logger.info(f"📦 Moved {src} → {dst}")

            return {"success": True, "src": src, "dst": dst}

        except Exception as e:
            logger.error(f"Move file error: {e}")
            return {"success": False, "error": str(e)}

    def _is_path_safe(self, path: str) -> bool:
        """
        Check if path is safe to access

        Args:
            path: Path to check

        Returns:
            True if safe
        """
        abs_path = str(Path(path).resolve())

        # Check forbidden paths
        for forbidden in self.forbidden_paths:
            if abs_path.startswith(forbidden):
                return False

        return True
