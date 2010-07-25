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
def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type','text/html'),('Pragma','no-cache')]
    write = start_response(status, response_headers)
    print 'start_response called!\n'
    writable = environ['wsgi.errors']
    writable.write('Writing to log!\n')

    yield '<P> My Own Hello World!\n'
    write('<p>Hello from the write callable!</p>')
    for i in sorted(environ.keys()):
        yield "<li>%s: %s\n" % (i, environ[i])
    yield "<li> wsgi.input:<br/><br/><kbd>"
    for line in environ['wsgi.input'].readlines():
        yield "%s<br/>" % (line)
    yield "</kbd>"
    writable = environ['wsgi.errors']
    writable.writelines(['Writing to log!'])
    writable.flush()
    yield 'done!'
