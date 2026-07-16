import click

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option('1.0.0', '-v', '--version', prog_name='CLI Click Example')
@click.option('--name', prompt='Your name', help='The person to greet.')
@click.option('--color', default='yellow', help='Color of the greeting (for demonstration, does not actually colorize in this basic example).')
def hello(name, color):
    """Simple program that greets NAME."""
    click.echo(f"Hello {name}, your color is {color}!")

if __name__ == '__main__':
    hello()
