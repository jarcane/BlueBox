__author__ = 'BearBear'

import libbluebox as bluebox
import libtcodpy as libtcod

box = bluebox.BlueBox(width=80)

box.text_out('Do you want to eat cake? ', newline=False)

text = box.text_in(newline=False, prompt=False)

box.clear_screen()

box.text_out('some graphics and ' + text)

box.text_in(prompt=True)

