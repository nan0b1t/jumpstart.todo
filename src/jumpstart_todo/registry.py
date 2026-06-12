from pathlib import Path
from typing import Any
import platformdirs
import tomllib
import tomli_w

class Registry:
    file: Path
    data: dict[str, Any]

    def __init__(self) -> None:
        self.file = Path(platformdirs.user_data_dir(appname="jumpstart.todo")) / "registry.toml"

        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self.data = {}
            self._save()
            return

        try:
            with self.file.open("rb") as f:
                self.data = tomllib.load(f)
        except (tomllib.TOMLDecodeError, PermissionError):
            self.data = {}

    def _save(self) -> None:
        try:
            with self.file.open("wb") as f:
                tomli_w.dump(self.data, f)
        except PermissionError as e:
            print(f"Error: Unable to write to registry file due to permissions: {e}")

    def add_project(self, name: str, path: str) -> None:
        self.data.setdefault("project", [])

        project_entry = {"name": name, "path": path}
        if project_entry not in self.data["project"]:
            self.data["project"].append(project_entry)
            self._save()
