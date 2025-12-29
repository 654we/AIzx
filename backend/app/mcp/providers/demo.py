class DemoMCPPlugin:
    name = "demo-local"
    capabilities = ["search", "summarize"]
    schema = {"query": "string", "limit": 10}
    timeout_sec = 5


PLUGIN = DemoMCPPlugin()


def health_check() -> str:
    return "ok"
