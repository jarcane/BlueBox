__author__ = 'BearBear'

import libbluebox as bluebox

box = bluebox.BlueBox()

box.text_out('Do you want to eat cake? ', newline=False)

x = box.text_in(newline=False, prompt=False)

box.text_out(x)


