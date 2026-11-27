class PluginError(Exception):
    """Error"""


class UnknownPluginError(PluginError):
    def __init__(self, name: str, available: list[str]):
        super().__init__(f"unknown Plugin '{name}'. Available: {available}")
