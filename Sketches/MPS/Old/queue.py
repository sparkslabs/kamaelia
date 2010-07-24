# -*- coding: utf-8 -*-
#
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
# -------------------------------------------------------------------------
class Queue(list):
	def shift(self):
		if self == []:
		   return None
		result = self[0]
		del self[0]
		return result
	def push(self, value):
		self.append(value)

class MessageQueue(Queue):
	def read(Queue):
		raise NotImplementedError
	def write(Queue):
		raise NotImplementedError

class InboundQueue(MessageQueue):
	def read(Queue):
		"Should be defined in this class"
class OutboundQueue(MessageQueue):
	def write(Queue, *Messages):
		"Should be defined in this class"

