from pathlib import Path
import click
from tinydb import Query
from envadmin import constants
from envadmin.cli import pass_context, Context
from envadmin.utilities import config, db


@click.command()
@click.option('-c', '--config-path', default=str(Path.home()), type=click.Path(), help="Folder to create .envadmin file.")
@click.option('-n', '--namespace', type=str, required=True, help="Namespace of variable.")
@click.option('-v', '--variation', type=str, help="Variation of variable.")
@click.argument('key')
@click.argument('value')
@pass_context
def cli(ctx: Context, key: str, value: str, config_path: Path, namespace: str, variation: str) -> None:
    """Variable-related tasks."""
    # Load database.
    ctx.config = config.get_config(config_path)
    ctx.database = db.get_db(Path(ctx.config.get("main", "repo_path")))
    ctx.namespace = namespace

    try:
        ctx.database_table = ctx.database.table(ctx.namespace)
    except Exception as excp:
        click.echo("Namespace could not be loaded!")
        raise click.ClickException("Error: %s" % excp)

    # Get variation values.
    variation_query = Query()

    if variation:
        if ctx.database_table.search(variation_query.name == variation):
            variation_name = variation
        else:
            raise click.ClickException("Variation isn't present.")
    else:
        variation_name = constants.DEFAULT_TABLE

    variable_values = ctx.database_table.search(variation_query.name == variation_name)[0]


    # Save back to db.
    ctx.database_table.upsert(variable_values, variation_query.name == variation)
