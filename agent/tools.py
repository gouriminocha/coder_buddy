import pathlib
import subprocess
from typing import Tuple

from langchain_core.tools import tool

BASE_PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"


# ✅ Use dynamic project_root
def safe_path_for_project(path: str, project_root: str) -> pathlib.Path:
    base = pathlib.Path(project_root)
    p = (base / path).resolve()

    if base.resolve() not in p.parents and base.resolve() != p:
        raise ValueError("Attempt to write outside project root")

    return p


@tool
def write_file(path: str, content: str, project_root: str) -> str:
    """Write content to a file inside the project root."""
    p = safe_path_for_project(path, project_root)
    p.parent.mkdir(parents=True, exist_ok=True)

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"WROTE:{p}"


@tool
def read_file(path: str, project_root: str) -> str:
    """Read content from a file inside the project root."""
    p = safe_path_for_project(path, project_root)

    if not p.exists():
        return ""

    return p.read_text(encoding="utf-8")


@tool
def list_file(directory: str, project_root: str) -> str:
    """List all files inside a directory within the project root."""
    p = safe_path_for_project(directory, project_root)

    if not p.is_dir():
        return "Not a directory"

    return "\n".join(
        str(f.relative_to(project_root))
        for f in p.glob("**/*")
        if f.is_file()
    )


@tool
def run_cmd(cmd: str, project_root: str, timeout: int = 30) -> Tuple[int, str, str]:
    """Run a shell command inside the project root."""
    base = pathlib.Path(project_root)

    res = subprocess.run(
        cmd,
        shell=True,
        cwd=str(base),
        capture_output=True,
        text=True,
        timeout=timeout
    )

    return res.returncode, res.stdout, res.stderr


def init_project_root():
    BASE_PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(BASE_PROJECT_ROOT)