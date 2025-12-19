import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    url = os.environ.get(
        "DATABASE_URL", "postgresql://docling:docling@localhost:5432/docling"
    )
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url
