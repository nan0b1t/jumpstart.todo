import click
import pprint
from jumpstart_todo.config import Config, bootstrap


@click.group()
@click.pass_context
def main(ctx: click.Context):
    ctx.ensure_object(dict)

    config_data: Config | None = bootstrap()
    if config_data is None:
        ctx.exit(0)

    ctx.obj["config"] = config_data


@main.command()
@click.pass_context
def ShowConfig(ctx: click.Context):
    pprint.pprint(
        ctx.obj["config"].data, indent=ctx.obj["config"].data["display"]["indent"]
    )


@main.command()
@click.pass_context
def init(ctx: click.Context):
    try:
        open(".todo", "x").close()
        if ctx.obj["config"].data["display"]["cheerfulness"] < 7:
            print("Created .todo file")
        else:
            print("Created .todo file. Time to get started!")

    except FileExistsError:
        print(".todo file already exists in current directory")
