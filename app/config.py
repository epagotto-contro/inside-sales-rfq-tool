import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    tenant_id: str = os.getenv("TENANT_ID", "")
    client_id: str = os.getenv("CLIENT_ID", "")
    client_secret: str = os.getenv("CLIENT_SECRET", "")
    shared_mailbox: str = os.getenv("SHARED_MAILBOX", "")
    graph_scope: str = os.getenv("GRAPH_SCOPE", "https://graph.microsoft.com/.default")

    @property
    def graph_configured(self) -> bool:
        return all((self.tenant_id, self.client_id, self.client_secret, self.shared_mailbox))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
