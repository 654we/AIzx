from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any


@dataclass
class MCPPluginInfo:
    name: str
    capabilities: list[str]
    schema: dict[str, Any]
    timeout_sec: int


class MCPPluginError(RuntimeError):
    pass


def load_plugin(module_path: str) -> MCPPluginInfo:
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as exc:
        raise MCPPluginError(f"插件模块不存在: {module_path}") from exc
    if not hasattr(module, "PLUGIN"):
        raise MCPPluginError("插件缺少 PLUGIN 定义")
    plugin = module.PLUGIN
    for field in ("name", "capabilities", "schema", "timeout_sec"):
        if not hasattr(plugin, field):
            raise MCPPluginError(f"插件缺少字段: {field}")
    return MCPPluginInfo(
        name=plugin.name,
        capabilities=list(plugin.capabilities),
        schema=dict(plugin.schema),
        timeout_sec=int(plugin.timeout_sec),
    )


def test_plugin(module_path: str) -> str:
    plugin = load_plugin(module_path)
    if hasattr(importlib.import_module(module_path), "health_check"):
        result = importlib.import_module(module_path).health_check()
        return str(result)
    return f"{plugin.name} 已加载"
