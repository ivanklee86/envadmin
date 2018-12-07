"""
With credit to https://github.com/pallets/click/tree/master/examples/complex.
"""
import os
import sys
import click


CONTEXT_SETTINGS = dict(auto_envvar_prefix='COMPLEX')


class Context():
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()
        self.database = None
        self.config = None
        self.namespace = None
        self.database_table = None

    def log(self, msg, *args):  # pylint: disable= R0201
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)  # pylint: disable = C0103
CMD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        commands = []
        for filename in os.listdir(CMD_FOLDER):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                commands.append(filename[4:-3])
        commands.sort()
        return commands

    def get_command(self, ctx, cmd_name):
        try:
            if sys.version_info[0] == 2:
                cmd_name = cmd_name.encode('ascii', 'replace')
            mod = __import__('envadmin.commands.cmd_' + cmd_name, None, None, ['cli'])
        except ImportError:
            return None
        return mod.cli


@click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    """A complex command line interface."""
    ctx.verbose = verbose
