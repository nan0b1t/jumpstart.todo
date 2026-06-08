from dataclasses import dataclass
from platformdirs import user_config_dir
from pathlib import Path
from prompt_toolkit import choice
from importlib.resources import files
import shutil

@dataclass
class Config:
    """Core configuration class"""

    ...


def bootstrap() -> Config:
    config_dir = Path(user_config_dir("jumpstart.todo"))
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file = config_dir / "config.toml"

    if not config_file.exists():
        result = choice(
            message="Couldn't find configuration. Create one?",
            options=[("Created config", "Yes"), ("Did not create config", "No")],
        )

        if result == "Created config":
            data = (
                files("jumpstart_todo.data")
                .joinpath("default_config.toml")
            )

            with data.open('rb') as src, open(config_file, 'wb') as dst:
                shutil.copyfileobj(src, dst)

        print(result)

    return Config()
