import asyncio
import sys

import uvicorn


def main() -> None:
    config = uvicorn.Config(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        log_level="warning",
    )
    server = uvicorn.Server(config)

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(server.serve(), loop_factory=asyncio.SelectorEventLoop)
        return

    asyncio.run(server.serve())


if __name__ == "__main__":
    main()
