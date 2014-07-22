__author__ = 'BearBear'

import libbluebox as bluebox
import libtcodpy as libtcod

box = bluebox.BlueBox(width=80)

box.text_out('Do you want to eat cake? ', newline=False)

text = box.text_in(newline=False, prompt=False)

box.set_graphics()

box.draw_point(60, 24, libtcod.chartreuse)

box.display_screen()

box.set_graphics(flag=False)

box.text_out('some graphics and ' + text)

box.text_in(prompt=True)

