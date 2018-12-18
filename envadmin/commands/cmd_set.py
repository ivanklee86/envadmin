import os
from pathlib import Path
import click
from gitsecret import GitSecret
from tinydb import Query
from envadmin import constants
from envadmin.cli import pass_context, Context
from envadmin.utilities import config, db


@click.command()
@click.option('-c', '--config-path', default=str(Path.home()), type=click.Path(), help="Folder to create .envadmin file.")
@click.option('-n', '--namespace', type=str, required=True, help="Namespace of variable.")
@click.option('-v', '--variation', type=str, help="Variation of variable.")
@click.option('-e', '--encrypt', is_flag=True, default= False, help="Encrypts variable.")
@click.option('-o', '--overwrite', is_flag=True, help="Encrypts variable.")
@click.argument('key')
@click.argument('value')
@pass_context
def cli(ctx: Context, key: str, value: str, config_path: Path, namespace: str, variation: str, encrypt: False, overwrite: False) -> None:
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

    variable_value = {
        'value': None,
        'encrypted': False
    }

    # Update database
    if encrypt:
        gitsecret_repo = GitSecret(path=Path(ctx.config.get("main", "repo_path")))
        gitsecret_repo.reveal()

        with open(os.path.join(path, "key.txt"), "r") as key_file:
            key_read = key_file.read().encode("UTF-8")

        f1 = Fernet(key_read)
        click.echo(f1.decrypt(token))
    else:
        variable_value['value'] = value

    if key in variable_values.keys() and not overwrite:
        raise click.ClickException("Attempted to overwrite an existing k:v pair, but '--overwrite' flag not supplied.")
    elif (key in variable_values.keys() and overwrite) or (key not in variable_values.keys()):
        variable_values[key] = variable_value

    # Save back to db.
    ctx.database_table.upsert(variable_values, variation_query.name == variation)