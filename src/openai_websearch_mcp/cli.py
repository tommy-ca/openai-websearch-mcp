import json
import sys
from pathlib import Path
from typing import Optional, Dict
import logging
import sys
import os
import typer
from shutil import which


logger = logging.getLogger(__file__)

app = typer.Typer(
    name="openapi-websearch-mcp",
    help="openapi-websearch-mcp install tools",
    add_completion=False,
    no_args_is_help=True,  # Show help if no args provided
)



def get_claude_config_path() -> Path | None:
    """Get the Claude config directory based on platform."""
    if sys.platform == "win32":
        path = Path(Path.home(), "AppData", "Roaming", "Claude")
    elif sys.platform == "darwin":
        path = Path(Path.home(), "Library", "Application Support", "Claude")
    else:
        return None

    if path.exists():
        return path
    return None


def update_claude_config(
    server_name: str,
    command: str,
    args: list[str],
    *,
    env_vars: Optional[Dict[str, str]] = None,
) -> bool:
    """Add or update a FastMCP server in Claude's configuration.
    """
    config_dir = get_claude_config_path()
    if not config_dir:
        raise RuntimeError(
            "Claude Desktop config directory not found. Please ensure Claude Desktop "
            "is installed and has been run at least once to initialize its configuration."
        )

    config_file = config_dir / "claude_desktop_config.json"
    if not config_file.exists():
        try:
            config_file.write_text("{}")
        except Exception as e:
            logger.error(
                "Failed to create Claude config file",
                extra={
                    "error": str(e),
                    "config_file": str(config_file),
                },
            )
            return False

    try:
        config = json.loads(config_file.read_text())
        if "mcpServers" not in config:
            config["mcpServers"] = {}

        # Always preserve existing env vars and merge with new ones
        if (
            server_name in config["mcpServers"]
            and "env" in config["mcpServers"][server_name]
        ):
            existing_env = config["mcpServers"][server_name]["env"]
            if env_vars:
                # New vars take precedence over existing ones
                env_vars = {**existing_env, **env_vars}
            else:
                env_vars = existing_env

        server_config = {
            "command": command,
            "args": args,
        }

        # Add environment variables if specified
        if env_vars:
            server_config["env"] = env_vars

        config["mcpServers"][server_name] = server_config

        config_file.write_text(json.dumps(config, indent=2))
        logger.info(
            f"Added server '{server_name}' to Claude config",
            extra={"config_file": str(config_file)},
        )
        return True
    except Exception as e:
        logger.error(
            "Failed to update Claude config",
            extra={
                "error": str(e),
                "config_file": str(config_file),
            },
        )
        return False


@app.command()
def install() -> None:
    """Install a current server in the Claude desktop app.
    """

    if not get_claude_config_path():
        logger.error("Claude app not found")
        sys.exit(1)

    name = "openapi-websearch-mcp"

    env_dict = {}
    home = os.environ['HOME']
    path = os.environ['PATH']
    api_key = os.environ['OPENAI_API_KEY'] if "OPENAI_API_KEY" in os.environ else "your-api-key-here"
    if home:
        env_dict["PATH"] = f"{home}:{path}"

    env_dict["OPENAI_API_KEY"] = api_key

    uv = which('uvx')
    command = uv if uv else "uvx"
    args = [name]

    # print("------------update_claude_config", command, args, env_dict)

    if update_claude_config(
        command,
        name,
        args,
        env_vars=env_dict,
    ):
        logger.info(f"Successfully installed {name} in Claude app")
    else:
        logger.error(f"Failed to install {name} in Claude app")
        sys.exit(1)
