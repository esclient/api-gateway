from typing import Any

from gateway.clients.base_client import AsyncGRPCClient, GRPCClient


class GQLContextViewer:
    def __init__(self) -> None:
        self.clients: dict[str, GRPCClient | AsyncGRPCClient] = {}

    def get_current(self, request: Any) -> dict[str, Any]:
        return {"request": request, "clients": self.clients}
