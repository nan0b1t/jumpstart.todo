import click
from jumpstart_todo.config import Config, bootstrap


@click.group()
@click.pass_context
def main(ctx: click.Context):
    ctx.obj = ctx.ensure_object(Config)
    ctx.obj = bootstrap()
    pass


@main.command()
def test():
    print("testing")
