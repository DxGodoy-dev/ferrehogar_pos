from __future__ import annotations

import os
import subprocess
import sys
from contextlib import nullcontext
from pathlib import Path


def ejecutar_pos(log_path: str | Path | None = None) -> int:
    """Lanza el POS en un subproceso desacoplado y retorna su PID."""
    print("DEBUG: Iniciando lanzamiento...")
    env = os.environ.copy()
    pythonpath_parts = list(sys.path)
    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(part for part in pythonpath_parts if part)

    popen_kwargs: dict = {
        "stdin": subprocess.DEVNULL,
        "close_fds": True,
        "env": env,
    }

    if os.name == "nt":
        popen_kwargs["creationflags"] = 0x00000008 | 0x00000200
    else:
        popen_kwargs["start_new_session"] = True

    if log_path:
        target_path = Path(log_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        file_ctx = open(target_path, "w", encoding="utf-8") # noqa: SIM115
    else:
        file_ctx = nullcontext(subprocess.DEVNULL)

    with file_ctx as log_target:
        proceso = subprocess.Popen(
            [sys.executable, "-m", "ferrehogar_pos.worker"],
            stdout=log_target,
            stderr=log_target,
            **popen_kwargs,
        )

    print(f"DEBUG: Lanzado con PID {proceso.pid}. Terminando padre.")
    return proceso.pid


if __name__ == "__main__":
    ejecutar_pos()