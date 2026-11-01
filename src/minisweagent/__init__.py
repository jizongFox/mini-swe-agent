"""
This file provides:

- Path settings for global config file & relative directories
- Version numbering
- Protocols for the core components of mini-swe-agent.
  By the magic of protocols & duck typing, you can pretty much ignore them,
  unless you want the static type checking.
"""

__version__ = "2.4.6"

import os
from pathlib import Path
from typing import Any, Protocol

import dotenv
from platformdirs import user_config_dir
from rich.console import Console

from minisweagent.utils.log import logger

package_dir = Path(__file__).resolve().parent


global_config_dir = Path(os.getenv("MSWEA_GLOBAL_CONFIG_DIR") or user_config_dir("mini-swe-agent"))
global_config_dir.mkdir(parents=True, exist_ok=True)
global_config_file = Path(global_config_dir) / ".env"

if not os.getenv("MSWEA_SILENT_STARTUP"):
    Console().print(
        f"This is [bold green]mini-swe-agent[/bold green] version [bold green]{__version__}[/bold green].\n"
        f"Check the [bold red]v2 migration guide[/] at [bold red]https://klieret.short.gy/mini-v2-migration[/]\n"
        f"Loading global config from [bold green]'{global_config_file}'[/bold green]",
    )
dotenv.load_dotenv(dotenv_path=global_config_file)


# === Protocols ===
# You can ignore them unless you want static type checking.


class Model(Protocol):
    """Protocol for language models."""

    config: Any

    def query(self, messages: list[dict[str, str]], **kwargs: Any) -> dict:
        """Return a model message with parsed actions and accounting metadata."""
        ...

    def format_message(self, **kwargs: Any) -> dict:
        """Build a provider-compatible message from role, content, and extra fields."""
        ...

    def format_observation_messages(
        self, message: dict, outputs: list[dict], template_vars: dict | None = None
    ) -> list[dict]:
        """Render action outputs as provider-compatible observation messages."""
        ...

    def get_template_vars(self, **kwargs: Any) -> dict[str, Any]:
        """Return variables available to prompt and observation templates."""
        ...

    def serialize(self) -> dict:
        """Return model configuration and metadata for trajectory serialization."""
        ...


class Environment(Protocol):
    """Protocol for execution environments."""

    config: Any

    def execute(self, action: dict, cwd: str = "") -> dict[str, Any]:
        """Execute an action, returning output, returncode, and exception information."""
        ...

    def get_template_vars(self, **kwargs: Any) -> dict[str, Any]:
        """Return environment-specific template variables."""
        ...

    def serialize(self) -> dict:
        """Return environment configuration for trajectory serialization."""
        ...


class Agent(Protocol):
    """Protocol for agents."""

    config: Any

    def run(self, task: str, **kwargs: Any) -> dict:
        """Run a task and return terminal metadata, including status and submission."""
        ...

    def save(self, path: Path | None, *extra_dicts: dict) -> dict:
        """Merge extra data into a trajectory, optionally write it, and return it."""
        ...


__all__ = [
    "Agent",
    "Model",
    "Environment",
    "package_dir",
    "__version__",
    "global_config_file",
    "global_config_dir",
    "logger",
]
