from memory_backends.base import MemoryBackend, MemoryBackendError

__all__ = ["MemoryBackend", "MemoryBackendError", "get_memory_backend"]

_backend_instance = None


def get_memory_backend() -> MemoryBackend:
    """
    Return a process-wide memory backend instance, chosen by
    config.MEMORY_BACKEND, creating it lazily on first use.

    To add a new backend later, register it here and implement a
    class with the same interface as MemoryBackend (see base.py).
    """
    global _backend_instance
    if _backend_instance is None:
        _backend_instance = _create_backend()
    return _backend_instance


def _create_backend() -> MemoryBackend:
    from config import config

    name = config.MEMORY_BACKEND.lower()

    if name == "local":
        from memory_backends.local_backend import LocalMemoryBackend
        return LocalMemoryBackend()

    if name == "cloud":
        from memory_backends.cloud_backend import CloudMemoryBackend
        return CloudMemoryBackend()

    raise ValueError(
        f"Unknown MEMORY_BACKEND '{config.MEMORY_BACKEND}'. "
        f"Supported values: 'local', 'cloud'."
    )
