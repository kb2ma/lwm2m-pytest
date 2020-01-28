# Copyright (c) 2018-2020 Ken Bannister. All rights reserved.
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

"""
Utilities for tests
"""

import pytest
import pexpect
import os
import signal
import logging

class ExpectHost():
    """
    A networking host wrapped in a pexpect spawn. There are two ways to run
    the host:

    1. connect() to start an interactive session, followed by send_recv() or
       directly sending commands from the returned pexpect 'term' object.
       Finally, use disconnect() to kill the session.

    2. run() to start and run the process to completion with no interaction.
    """

    def __init__(self, folder, term_cmd, putenv={}, timeout=10):
        """
        :putenv: Additional entries for os.environ dictionary to pass to
                 spawned process
        """
        self.folder   = folder
        self.term     = None
        self.term_cmd = term_cmd
        self.timeout  = timeout
        self.putenv   = putenv

    def connect(self):
        """
        Starts OS host process.

        :return: pexpect spawn object; the 'term' attribute for ExpectHost
        """
        if self.folder:
            os.chdir(self.folder)

        self.term = pexpect.spawnu(self.term_cmd, timeout=self.timeout,
                                   env=self._build_env(), codec_errors='replace')
        return self.term

    def run(self):
        """
        Runs OS host process to completion

        :return: String output from process
        """
        if self.folder:
            os.chdir(self.folder)
        return pexpect.run(self.term_cmd, env=self._build_env())

    def disconnect(self):
        """Kill OS host process"""
        try:
            os.killpg(os.getpgid(self.term.pid), signal.SIGKILL)
        except ProcessLookupError:
            logging.info("Process already stopped")

    def send_recv(self, out_text, in_text):
        """Sends the given text to the host, and expects the given text
           response."""
        self.term.sendline(out_text)
        self.term.expect(in_text, self.timeout)

    def _build_env(self):
        """Builds full os.environ dictionary if putenv instance variable has
           been defined."""
        env = None
        if self.putenv:
            env = os.environ.copy()
            env.update(self.putenv)
        return env
