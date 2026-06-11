# pyright: basic

from platformdirs import user_config_dir
from pathlib import Path
from prompt_toolkit import choice
from importlib.resources import files
import shutil
import tomllib
from typing import Any


class Config:
    """Core configuration class"""

    data: dict[str, Any]  # type: ignore[reportAny]

    def __init__(self, data=None) -> None:
        if data == None:
            self.data = {}
        else:
            self.data = data


def find_file(file: str, start_path: Path | str = ".") -> Path | None:
    current = Path(start_path).resolve()

    while True:
        target = current / file
        if target.is_file():
            return target

        if current == current.parent:
            break

        current = current.parent

    return None


def deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:

    result: dict[str, Any] = dict(dict1)

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def bootstrap() -> Config | None:
    config_dir = Path(user_config_dir("jumpstart.todo"))
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file = config_dir / "config.toml"

    data = files("jumpstart_todo.data").joinpath("default_config.toml")

    if not config_file.exists():
        result = choice(
            message="Couldn't find configuration. Create one?",
            options=[("Created config", "Yes"), ("Did not create config", "No")],
        )

        if result == "Created config":
            with data.open("rb") as src, open(config_file, "wb") as dst:
                shutil.copyfileobj(src, dst)

        print(result)

    # Load default config
    with data.open("rb") as default_config:
        default_config = tomllib.load(default_config)

    with config_file.open("rb") as user_config:
        user_config = tomllib.load(user_config)

    local_config_file = find_file(".todoconf")

    if local_config_file == None:
        print(
            "Couldn't find local config file. Create one at project root called .todoconf"
        )
        return None

    with local_config_file.open("rb") as local_config_file:
        local_config_data = tomllib.load(local_config_file)

    final_data = deep_merge(default_config, user_config)
    final_data = deep_merge(final_data, local_config_data)
    return Config(data=final_data)
