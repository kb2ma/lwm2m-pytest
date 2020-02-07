# Copyright (c) 2020 Ken Bannister. All rights reserved.
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

"""
Tests registration with LwM2M server.
"""

import pytest
#import logging
import os
import time

from conftest import ExpectHost

pwd = os.getcwd()
#logging.basicConfig(level=logging.INFO, filename='regtest.log')

#
# fixtures and utility functions
#

@pytest.fixture(scope="session")
def tmpdir(tmpdir_factory):
    return tmpdir_factory.mktemp("leshan")


@pytest.fixture
def leshan_server(tmpdir):
    """
    Provides an ExpectHost that runs the Leshan LwM2M server app.
    """
    base_folder = os.environ.get('LESHAN_BASE', None)
    board       = os.environ.get('BOARD', 'native')

    jar = '{0}/leshan-server-demo/target/leshan-server-demo-1.0.0-SNAPSHOT-jar-with-dependencies.jar'.format(base_folder)
    term_cmd = 'java -jar {0} --coaphost [fd00:bbbb::1]'.format(jar)
    term_resp = 'Web server started'

    host = ExpectHost(tmpdir, term_cmd)
    term = host.connect()
    term.expect(term_resp)

    yield host

    # teardown
    host.disconnect()


@pytest.fixture
def lwm2m_client():
    """
    Provides an ExpectHost that runs the LwM2M client app.
    """
    base_folder = os.environ.get('RIOTAPPSBASE', None)

    host = ExpectHost(os.path.join(base_folder, 'lwm2m-client'), 'make term')
    term = host.connect()
    term.expect('This is RIOT!')

    # set ULA
    host.send_recv('ifconfig 6 add unicast fd00:bbbb::2/64','success:')

    yield host

    # teardown
    host.disconnect()

#
# tests
#

def test_register(leshan_server, lwm2m_client):
    """Registers to Leshan"""
    lwm2m_client.send_recv('lwm2m state', 'Client state: 0')
    
    lwm2m_client.term.sendline('lwm2m start')
    # wait for registration to complete
    time.sleep(2)
    
    lwm2m_client.send_recv('lwm2m state', 'Client state: 2')
    
