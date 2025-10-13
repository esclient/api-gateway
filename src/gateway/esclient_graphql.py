from typing import Any

from gateway.clients.base_client import GrpcClient


class GQLContextViewer:
    def __init__(self) -> None:
        self.clients: dict[str, GrpcClient] = {}

    def get_current(self, request: Any) -> dict[str, Any]:
        return {"request": request, "clients": self.clients}
