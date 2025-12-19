import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    url = os.environ.get(
        "DATABASE_URL", "postgresql://docling:docling@localhost:5432/docling"
    )
    if "connect_timeout=" not in url:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}connect_timeout=3"
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url
