from pathlib import Path
import click
from tinydb import Query
from envadmin import constants
from envadmin.cli import pass_context, Context
from envadmin.utilities import config, db


@click.group()
@click.option('-c', '--config-path', default=str(Path.home()), type=click.Path(), help="Folder to create .envadmin file.")
@click.option('-n', '--namespace', type=str, required=True, help="Namespace to modify.")
@pass_context
def cli(ctx: Context, config_path: Path, namespace: str) -> None:
    """Variation-related tasks."""
    ctx.config = config.get_config(config_path)
    ctx.database = db.get_db(Path(ctx.config.get("main", "repo_path")))
    ctx.namespace = namespace

    try:
        ctx.database_table = ctx.database.table(ctx.namespace)
    except Exception as excp:
        click.echo("Namespace could not be loaded!")
        raise click.ClickException("Error: %s" % excp)


@cli.command()
@pass_context
def list(ctx: Context) -> None:  # pylint: disable=redefined-builtin
    """Lists all variations in envadmin db."""

    click.echo('The following variations for namespace "%s" are present:' % ctx.namespace)
    for variation in ctx.database_table.all():
        if variation['name'] != constants.DEFAULT_TABLE:
            click.echo("• " + variation['name'])


@cli.command()
@click.option('-v', '--variation', default=None, type=str, help="Name of variation.")
@pass_context
def create(ctx: Context, variation: str) -> None:
    """Creates a variation for a namespace."""
    variation_query = Query()

    if not ctx.database_table.search(variation_query.name == variation):
        ctx.database_table.insert({'name': variation})
    else:
        raise click.ClickException("Namespace already present")


@cli.command()
@click.option('-v', '--variation', default=None, type=str, help="Name of variation.")
@pass_context
def delete(ctx: Context, variation: str) -> None:
    """Deletes a variation in envadmin db."""
    if variation == constants.DEFAULT_TABLE:
        click.echo("Cannot delete namespace defaults.")
    else:
        if click.confirm('Do you want to delete the "%s" variation in the "%s" namespace?' % (variation, ctx.namespace)):
            variation_query = Query()
            ctx.database_table.remove(variation_query.name == variation)
