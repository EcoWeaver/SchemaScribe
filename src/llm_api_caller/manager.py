import importlib.util
import logging
from pathlib import Path

from .base_api_caller import Base_api_caller
from .errors_plugin_caller import PluginError, UnknownPluginError

log = logging.getLogger(__name__)


class Plugin_manager:
    def __init__(self) -> None:
        self._plugins: dict[str, type[Base_api_caller]] = {}

    def register(self, name: str):
        def deco(cls):
            if not (isinstance(cls, type) and issubclass(cls, Base_api_caller)):
                raise PluginError(f"{cls!r} erbt nicht von BaseAPICaller")
            if name in self._plugins:
                raise PluginError(f"Plugin '{name}' ist schon registriert")
            cls.name = name
            self._plugins[name] = cls
            return cls

        return deco

    def load_directory(self, path: Path) -> None:
        if not path.is_dir():
            return
        for file in sorted(path.glob("*.py")):
            if file.name.startswith("_"):
                continue
            try:
                spec = importlib.util.spec_from_file_location(
                    f"api_caller_plugin_{file.stem}", file
                )
                if spec is None or spec.loader is None:
                    raise PluginError(
                        f"{file.name} kann nicht als Modul geladen werden"
                    )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception as e:
                log.warning("Plugin %s übersprungen: %s", file.name, e)
                log.debug("Details:", exc_info=True)

    def get(self, name: str) -> type[Base_api_caller]:
        try:
            return self._plugins[name]
        except KeyError:
            raise UnknownPluginError(name, self.available()) from None

    def available(self) -> list[str]:
        return sorted(self._plugins)
