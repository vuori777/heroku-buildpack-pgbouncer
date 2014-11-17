#!/usr/bin/env python

import argparse
import os
import os.path
import subprocess
import multiprocessing
import sys
import time
import pg8000
import os
import hashlib

from jinja2 import Environment, FileSystemLoader
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'templates')

# Register database schemes in URLs.


def main():
    command = sys.argv
    generate_config()

def generate_config():
    options = parse_options(os.environ())
    render_file('pgbouncer.ini', options, '/app/vendor/pgbouncer/')
    render_file('stunnel.conf', options, '/app/vendor/stunnel/')
    render_file('users.txt', options, '/app/vendor/pgbouncer/')

def render_file(filename, values, base_dir):
    """Renders given template and writes to given base_dir"""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR),
                      trim_blocks=True)
    template = env.get_template(filename)
    output_from_parsed_template = template.render(values)

    with open(os.path.join(base_dir, filename), "wb") as fh:
        fh.write(output_from_parsed_template)

def parse_options(env={}):
    """extracts options and applies defaults"""

    options = { 'postgres_urls'        : env.get('POSTGRES_URLS', 'DATABASE_URL'),
                'pool_mode'            : env.get('PGBOUNCER_POOL_MODE', 'transaction'),
                'max_client_conn'      : env.get('PGBOUNCER_MAX_CLIENT_CONN', '100'),
                'default_pool_size'    : env.get('PGBOUNCER_DEFAULT_POOL_SIZE', '1'),
                'reserve_pool_size'    : env.get('PGBOUNCER_RESERVE_POOL_SIZE', '1'),
                'reserve_pool_timeout' : env.get('PGBOUNCER_RESERVE_POOL_TIMEOUT', '1'),
                'log_connections'      : env.get('PGBOUNCER_LOG_CONNECTIONS', '1'),
                'log_disconnections'   : env.get('PGBOUNCER_LOG_DISCONNECTIONS', '1'),
                'log_pooler_errors'    : env.get('PGBOUNCER_LOG_POOLER_ERRORS', '1'),
                'stats_period'         : env.get('PGBOUNCER_STATS_PERIOD', '60'),
            }

    if 'PGBOUNCER_SERVER_RESET_QUERY' not in env and options['pool_mode']=='session':
        options['server_reset_query'] = 'DISCARD ALL'
    else:
        options['server_reset_query'] = ''


    for idx, postgres_url in enumerate(options['postgres_urls'].split):
        options[postgres_url] = parse_url(postgres_url, color=postgres_url, index=idx)
        print options[postgres_url]

    return options

def parse_url(url, color, index):
    """Parses a database URL."""

    config = {}

    urlparse.uses_netloc.append('postgres')
    urlparse.uses_netloc.append('postgresql')

    url = urlparse.urlparse(url)

    # Remove query strings.
    path = url.path[1:]
    path = path.split('?', 2)[0]

    # Generate md5sum of password
    md5pass = hashlib.md5("{}{}".format(url.password, url.username)).hexdigest()

    # Handle postgres percent-encoded paths.
    hostname = url.hostname or ''
    if '%2f' in hostname.lower():
        hostname = hostname.replace('%2f', '/').replace('%2F', '/')

    # Update with environment configuration.
    config.update({
        'name': path or '',
        'user': url.username or '',
        'password': url.password or '',
        'host': hostname,
        'port': url.port or '',
        'color': color,
        'md5pass': 'md5{}'.format(md5pass),
        'client_name': "db{}".format(index),
        })

    return config


if __name__ == '__main__':
    main()
