__author__ = 'BearBear'

import libbluebox as bluebox

box = bluebox.BlueBox(width=80)

box.text_out('Do you want to eat cake? ', newline=False)

text = box.text_in(newline=False, prompt=False)

box.set_graphics()

box.draw_point(60, 24, bluebox.color_bold)
box.draw_point(62, 24, bluebox.color_half)
box.draw_point(64, 24, bluebox.color_on)

box.draw_line(0, 0, 50, 30)
box.draw_line(0, 0, 30, 50)

box.display_screen()

box.text_in()

box.set_graphics(flag=False)

box.text_out('output: ' + text)

box.text_in(prompt=True)