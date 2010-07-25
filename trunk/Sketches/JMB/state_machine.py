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

from Axon.Component import component

class StateMachine(component):
    States = ["initial"]
    def __init__(self, initial_index =0, **argd):
        super(StateMachine, self).__init__(**argd)
        self._state_table = {}
        self.index = initial_index

    def main(self):
        self.current_state = self._getState(self.States[self.index])
        self.not_done = True
        
        while self.not_done:
            try:
                yield self.current_state.next()
            except StopIteration:
                state_name = self.States[self.index]
                self.current_state = self._getNextState()
                self._state_table[state_name] = None
                
                
    def _initializeState(self, state):
        state_func = getattr(self, state)
        self._state_table[state] = state_func()
        
    def _getState(self, state, noinitialize=False):
        state_iter = self._state_table.get(state, None)
        if state_iter or noinitialize:
            return state_iter
        else:
            self._initializeState(state)
            return self._state_table[state]
            
    def _getNextState(self):
        self.index += 1
        if self.index >= len(self.States):
            self.index = 0
        return self._getState(self.States[self.index])
    
    def initial(self):
        print 'Hello, world!'
        yield 1
        
    def advance(self, next_state=''):
        if next_state:
            self.current_state = self._getState(next_state)
        else:
            self.current_state = self._getNextState()
            
    def end(self):
        self.not_done = False
        
if __name__ == '__main__':
    class GreeterStateMachine(StateMachine):
        States = ['initial', 'print_comma', 'print_world']
        def initial(self):
            yield 1
            print 'Hello'
        def print_comma(self):
            yield 1
            print ','
        def print_world(self):
            counter = 0
            while True:
                print 'world!'
                counter += 1
                if counter < 5:
                    self.advance()
                    yield 1
                else:
                    self.end()
                    yield 1
                    
            
            
    GreeterStateMachine().run()