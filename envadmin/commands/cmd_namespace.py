from pathlib import Path
import click
from envadmin import constants
from envadmin.cli import pass_context, Context
from envadmin.utilities import config, db


@click.group()
@click.option('-c', '--config-path', default=str(Path.home()), type=click.Path(), help="Folder to create .envadmin file.")
@pass_context
def cli(ctx: Context, config_path: Path) -> None:
    """Namespace-related tasks."""
    ctx.config = config.get_config(config_path)
    ctx.database = db.get_db(Path(ctx.config.get("main", "repo_path")))


@cli.command()
@pass_context
def list(ctx: Context) -> None:  # pylint: disable=redefined-builtin
    """Lists all namespaces in envadmin db."""
    database_tables = ctx.database.tables()

    click.echo("The following namespaces are present:")
    for table in database_tables:
        if table != "_default":
            click.echo("• " + table)


@cli.command()
@click.option('-n', '--namespace', default=None, type=str, help="Name of namespace.")
@pass_context
def create(ctx: Context, namespace: str) -> None:
    """Creates a namespace in envadmin db."""
    if namespace not in ctx.database.tables():
        ctx.database.table(name=namespace).insert({'name': constants.DEFAULT_TABLE})
    else:
        raise click.ClickException("Namespace already present")


@cli.command()
@click.option('-n', '--namespace', default=None, type=str, help="Name of namespace.")
@pass_context
def delete(ctx: Context, namespace: str) -> None:
    """Deletes a namespace in envadmin db."""
    if click.confirm('Do you want to delete the "%s" namespace?' % namespace):
        ctx.database.purge_table(name=namespace)
