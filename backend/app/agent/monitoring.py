import os
from typing import Optional

from langfuse import Langfuse


def get_langfuse_client() -> Optional[Langfuse]:
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    host = os.environ.get(
        "LANGFUSE_HOST",
        os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000"),
    )

    if not public_key or not secret_key:
        return None

    return Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host,
        environment="dev",
    )
