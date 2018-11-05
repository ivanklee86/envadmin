import click
from envadmin.cli import PASS_CONTEXT, Context


@click.command('status', short_help='Shows file changes.')
@PASS_CONTEXT
def cli(ctx: Context) -> None:
    """Shows file changes in the current working directory."""
    ctx.log('Hello!')
    ctx.vlog('Hello this is envadmin!')
