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
    app_secret_key: str = os.getenv("APP_SECRET_KEY", "dev-secret")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
