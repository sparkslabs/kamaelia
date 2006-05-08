from Axon.Component import component
from time import sleep

class Lagger(component):
	def main(self):
		while 1:
			yield 1
			sleep(0.1)
