#!/usr/bin/env python

from mfrc522 import SimpleMFRC522
import time
import requests


reader = SimpleMFRC522()



try:
        id, text = reader.read()
        print(id)
        print(text)
finally:
        print(1)















