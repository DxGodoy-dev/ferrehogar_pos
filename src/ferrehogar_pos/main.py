from __future__ import annotations

import os
import subprocess
import sys
from contextlib import nullcontext
from pathlib import Path
from typing import Any


def ejecutar_pos(log_path: str | Path | None = None) -> int:
    """Lanza el POS en un subproceso desacoplado y retorna su PID."""
    env = os.environ.copy()
    pythonpath_parts = list(sys.path)
    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(part for part in pythonpath_parts if part)

    popen_kwargs: dict[str, Any] = {
        "stdin": subprocess.DEVNULL,
        "close_fds": True,
        "env": env,
    }

    if os.name == "nt":
        # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        flags = getattr(subprocess, "DETACHED_PROCESS", 0x00000008) | getattr(
            subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200
        )
        popen_kwargs["creationflags"] = flags
    else:
        popen_kwargs["start_new_session"] = True

    if log_path:
        target_path = Path(log_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        file_ctx = open(target_path, "w", encoding="utf-8")  # noqa: SIM115
    else:
        file_ctx = nullcontext(subprocess.DEVNULL)

    with file_ctx as log_target:
        proceso = subprocess.Popen(
            [sys.executable, "-m", "ferrehogar_pos.worker"],
            stdout=log_target,
            stderr=log_target,
            **popen_kwargs,
        )

    return proceso.pid


def main() -> None:
    """Punto de entrada principal para ejecución interactiva y CLI."""
    pid = ejecutar_pos()
    print(f"FerreHogar POS iniciado en segundo plano (PID: {pid}).")


if __name__ == "__main__":
    main()