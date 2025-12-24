# problems/storage/base.py
from abc import ABC, abstractmethod

class StorageBackend(ABC):
    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str):
        pass

    @abstractmethod
    def delete_prefix(self, remote_prefix: str):
        pass
