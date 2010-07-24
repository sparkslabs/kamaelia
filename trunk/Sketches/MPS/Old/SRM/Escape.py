#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re as _re

def escape(message,substring = None):
    result = _re.sub("%", "%25", message)
    if substring is not None:
        escaped_substring = "".join(["%"+hex(ord(x))[2:] for x in substring])
        result = _re.sub(substring, escaped_substring, result)
    return result

def unescape(message,substring = None):
    result = message
    if substring is not None:
        escaped_substring = "".join(["%"+hex(ord(x))[2:] for x in substring])
        result = _re.sub(escaped_substring, substring, result)
    result = _re.sub("%25", "%", result)
    return result
