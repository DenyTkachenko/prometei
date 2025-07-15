import pickle
import shutil
import logging
from pathlib import Path
from typing import Callable, Optional, Generic, Type
from datetime import datetime
from storage.interface import StorageInterface, T


class PickleStorage(StorageInterface[T], Generic[T]):
    def __init__(
        self,
        filename: str = "addressbook.pkl",
        factory: Optional[Callable[[], T]] = None,
        backup: bool = True,
        max_backups: int = 5,
        backup_dir: str = "backups",
        expected_type: Optional[Type[T]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.filename = Path(filename)
        self.factory = factory
        self.backup = backup
        self.max_backups = max_backups
        self.backup_dir = self.filename.parent / backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.expected_type = expected_type

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.NullHandler())

    def _cleanup_backups(self):
        backup_files = sorted(
            self.backup_dir.glob(f"{self.filename.stem}_backup_*.pkl"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        for old_backup in backup_files[self.max_backups :]:
            try:
                old_backup.unlink()
                self.logger.info(f"Deleted old backup: {old_backup}")
            except Exception as e:
                self.logger.warning(f"Failed to delete backup {old_backup}: {e}")

    def _make_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_path = self.backup_dir / f"{self.filename.stem}_backup_{timestamp}.pkl"
        try:
            shutil.copy2(self.filename, backup_path)
            self.logger.info(f"Backup created: {backup_path}")
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            raise
        self._cleanup_backups()

    def load(self) -> T:
        if not self.filename.exists():
            if self.factory is None:
                raise ValueError("No factory provided and file does not exist.")
            self.logger.info(f"File {self.filename} not found, creating new instance via factory")
            return self.factory()

        try:
            with self.filename.open("rb") as f:
                data = pickle.load(f)
            if self.expected_type is not None and not isinstance(data, self.expected_type):
                raise TypeError(f"Loaded object type {type(data)} does not match expected type {self.expected_type}")

            return data
        except Exception as e:
            self.logger.error(f"Failed to load data from {self.filename}: {e}")
            self.logger.warning("Attempting to load the latest backup...")

            # Emergency recovery of a file from backup
            backup_files = sorted(
                self.backup_dir.glob(f"{self.filename.stem}_backup_*.pkl"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )

            for backup_file in backup_files:
                try:
                    with backup_file.open("rb") as f:
                        data = pickle.load(f)
                    self.logger.warning(f"Loaded data from backup: {backup_file}")
                    return data
                except Exception as backup_err:
                    self.logger.warning(f"Failed to load backup {backup_file}: {backup_err}")
                    continue

            self.logger.error(f"Failed to load data from {self.filename}, and no valid backups found.")
            raise RuntimeError(
                f"Failed to load data from {self.filename}, and no valid backups found."
            )

    def save(self, data: T) -> None:
        try:
            if self.backup and self.filename.exists():
                self._make_backup()

            temp_file = self.filename.with_suffix(".tmp")
            with temp_file.open("wb") as f:
                pickle.dump(data, f)
            temp_file.replace(self.filename)
            self.logger.info(f"Data saved to {self.filename}")
        except Exception as e:
            self.logger.error(f"Failed to save data to {self.filename}: {e}")
            raise RuntimeError(f"Failed to save data to {self.filename}: {e}")
