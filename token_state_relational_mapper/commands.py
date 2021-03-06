"""
Simple ERC20 token state relational mapper service that gathers data from Ethereum blockchain about specific token.
Recent token state is stored in the database.
"""
import click
from . import app, db
from .mapper.mapper_options import MapperOptions


@app.cli.command()
@click.option('--address', help='The address of ERC20 contract to watch.')
@click.option('--start', type=int, help='The starting block where mapper starts gathering data about contract.')
@click.option('--end', type=int, help='The end block where mapper ends gathering data about contract and terminates.')
@click.option('--min-block-height', type=int, help='The minimum block height of block to be mapped')
def start_mapping(start, end, address, min_block_height):
    """Command to start application. It starts server and starts gathering state of token. """
    click.echo('Started mapping contract at address %s.' % address)
    click.echo('Starting block: %i' % start)
    if end is not None:
        click.echo('Ending block: %i' % end)

    click.echo('Connecting to parity node: %s' % app.config['PARITY_NODE_URI'])
    app.config['MapperOptions'] = MapperOptions(address, start, end, min_block_height)

    app.run()


@app.cli.command()
def init_db():
    """ Initialize the database using connection string from config. """
    db.create_all()
    click.echo('Initialized database under %s' % app.config['SQLALCHEMY_DATABASE_URI'])


@app.cli.command()
def drop_db():
    """ Drop the database using connection string from config. """
    db.drop_all()
    click.echo('Dropped database under %s' % app.config['SQLALCHEMY_DATABASE_URI'])
