import os
import sys


def load_env(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def main() -> int:
    env_path = sys.argv[1] if len(sys.argv) > 1 else ".env"
    load_env(env_path)
    host = os.environ.get("LANGFUSE_HOST", "")
    print(f"LANGFUSE_HOST={host}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
