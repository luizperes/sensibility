#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright 2017 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from . import Language


class Python(Language):
    extensions = {'.py'}

    def tokenize(self, source: str) -> None:
        raise NotImplementedError

    def check_syntax(self, source: str) -> bool:
        r"""
        Given a source file, returns True if the file compiles.
        >>> Python().check_syntax('print("Hello, World!")')
        True
        >>> Python().check_syntax('import java.util.*;')
        False
        >>> Python().check_syntax('\x89PNG\x0D\x0A\x1A\x0A\x00\x00\x00\x0D')
        False
        >>> Python().check_syntax(r"AWESOME_CHAR_ESCAPE = '\x0G'")
        False
        """

        # I have the sneaking suspicion that compile() puts stuff in a cache that
        # is NOT garbage collected! Since I consider this a pretty serious memory
        # leak, I implemented this batshit crazy technique. Basically, let the
        # operating system be our garbage collector.

        pid = os.fork()
        if pid == 0:
            # Child process. Let it crash!!!
            try:
                compile(source, '<unknown>', 'exec')
            except:
                # Use _exit so it doesn't raise a SystemExit exception.
                os._exit(-1)
            else:
                os._exit(0)
        else:
            # Parent process.
            child_pid, status = os.waitpid(pid, 0)
            return status == 0
