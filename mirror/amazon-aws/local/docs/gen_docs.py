from os import system
from time import sleep
import sys

if __name__ == '__main__':
  while(1):
    system('sphinx-build -a ./source ./build/html')
    sleep(.5)

