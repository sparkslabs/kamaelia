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
"""
This module contains the UrlList.  This is used to route requests to the proper
application by the WsgiHandler.  Please note that order DOES matter here.  The
URL matcher will use the first item in the list that it gets a match with.  In
particular, the .* element MUST be listed last.

You may use regular expressions here, but I'd reccommend not doing anything too
fancy unless you really know what you're doing.  I do reccommend placing ?/ in
front of and behind each item so that the items will match whether or not there
is a beginning or trailing slash
"""

UrlList = [
    ('/?simple/?', 'Wsgi.Apps.simple_app', 'simple_app', 'Simple WSGI Application'),
    ('.*', 'Wsgi.Apps.error_handler', 'application', 'Error Handler')
]
