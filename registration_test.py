# Copyright (c) 2020 Ken Bannister. All rights reserved.
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

"""
Tests registration with LwM2M server.
"""

import pytest
import os
import re

from conftest import ExpectHost

pwd = os.getcwd()

#
# fixtures and utility functions
#

@pytest.fixture
def leshan_server():
    base_folder = os.environ.get('LESHAN_BASE', None)
    board       = os.environ.get('BOARD', 'native')

    term_cmd = 'java -jar ../repo/leshan-server-demo/target/leshan-server-demo-1.0.0-SNAPSHOT-jar-with-dependencies.jar --coaphost [fd00:bbbb::1]'
    term_resp = 'Web server started'
        
    host = ExpectHost(os.path.join(base_folder, '../share'), term_cmd)
    term = host.connect()
    term.expect(term_resp)

    yield host

    # teardown
    host.disconnect()

#
# tests
#

def test_register(leshan_server):
    #nano_block_client.send_recv('post fd00:bbbb::1 5683', signature)
    pass
