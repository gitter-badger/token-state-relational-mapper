"""
Simple ERC20 token state relational mapper service that gathers data from Ethereum blockchain about specific token.
Recent token state is stored in the database.
"""

from flask import Flask, jsonify
from .mapper_options import MapperOptions
import click

app = Flask('token-state-relational-mapper')
app.config.from_envvar('TSRM_SETTINGS')


@app.route('/api/configuration', methods=['GET'])
def get_configuration():
    return jsonify({
        'options': app.config['MapperOptions'].serialize(),
        'parity_node_uri': app.config['PARITY_NODE_URI'],
        'sql_connection': app.config['DATABASE_URI']
    })


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
