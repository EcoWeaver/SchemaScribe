from pathlib import Path

from .base_api_caller import Base_api_caller, CallResult
from .manager import Plugin_manager

__all__ = ["Base_api_caller", "CallResult", "Plugin_manager"]

manager = Plugin_manager()
register = manager.register

manager.load_directory(Path(__file__).parent / "plugins")
