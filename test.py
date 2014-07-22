__author__ = 'BearBear'

import libbluebox as bluebox

box = bluebox.BlueBox()

box.text_out('Do you want to eat cake?')

x = box.text_in(newline=False, prompt=True)

box.text_out(x)
