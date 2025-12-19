import os
import subprocess
import sys
import time
from pathlib import Path

import httpx


def wait_for_server(
    client: httpx.Client,
    url: str,
    process: subprocess.Popen,
    timeout: float = 90.0,
) -> None:
    start = time.time()
    while time.time() - start < timeout:
        if process.poll() is not None:
            raise RuntimeError("Uvicorn exited before server became ready.")
        try:
            resp = client.get(url)
            if resp.status_code == 200:
                return
        except httpx.RequestError:
            pass
        time.sleep(1)
    raise RuntimeError("Server did not become ready in time.")


def main() -> None:
    os.environ.setdefault("SKIP_DOCLING_INIT", "1")
    base_dir = Path(__file__).resolve().parents[1]

    command = [
        sys.executable,
        "scripts/run_api.py",
    ]

    process = subprocess.Popen(
        command,
        cwd=base_dir,
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        with httpx.Client(timeout=1.0) as client:
            try:
                wait_for_server(client, "http://127.0.0.1:8001/health", process)
            except RuntimeError:
                process.terminate()
                output, _ = process.communicate(timeout=10)
                if output:
                    print(output)
                raise

            start_resp = client.post(
                "http://127.0.0.1:8001/api/v1/audit/start",
                json={"input_text": "review me"},
            )
            start_data = start_resp.json()

            resume_resp = client.post(
                "http://127.0.0.1:8001/api/v1/audit/resume",
                json={
                    "thread_id": start_data["thread_id"],
                    "decision": "approved",
                    "notes": "ok",
                },
            )
            resume_data = resume_resp.json()

        print("start_status", start_resp.status_code)
        print("resume_status", resume_resp.status_code)
        print("resume_data", resume_data)
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


if __name__ == "__main__":
    main()
