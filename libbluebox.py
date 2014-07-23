"""
libbluebox.py - BlueBox core library

This file contains the basic class object BlueBox and its subroutines.

"""

import libtcodpy as libtcod

# the standard "colors" for the Blue Box monochrome
# The monochrome display accepts 4 intensity levels,
# though the bold setting was prone to inducing screen burn-in
color_off = libtcod.black
color_half = libtcod.darker_green
color_on = libtcod.dark_green
color_bold = libtcod.green


class BlueBox:
    # the BlueBox instance object
    def __init__(self, win_name='BlueBox', boot_msg=True, graphics_layer=False, img=None,
                 width=40, height=24, fps=48, foreground=color_on, background=color_off):
        # declare initial graphics colors and resolution (40 or 80 column modes)
        self.win_name = win_name
        self.boot_msg = boot_msg
        self.graphics_layer = graphics_layer
        self.img = img
        self.width = width
        self.height = height
        self.fps = fps
        self.foreground = foreground
        self.background = background

        # initialize libtcod console and store to self.con
        if width == 80:
            libtcod.console_set_custom_font('bluebox80.png',
                                            libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        else:
            libtcod.console_set_custom_font('bluebox.png',
                                            libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(self.width, self.height, self.win_name, False)
        libtcod.sys_set_fps(self.fps)
        self.con = libtcod.console_new(self.width, self.height)

        # set console colors and alignment
        libtcod.console_set_default_foreground(self.con, self.foreground)
        libtcod.console_set_default_background(self.con, self.background)
        libtcod.console_set_alignment(self.con, libtcod.LEFT)

        # create the cursor
        self.cursor = Cursor()

        # create an array containing the screen contents
        self.screen = [[' ' for y in range(self.height)] for x in range(self.width)]

        # if graphics layer is enabled, initialize it.
        if graphics_layer:
            self.img = libtcod.image_new(self.width * 2, self.height * 2)
            libtcod.image_clear(self.img, self.background)

        # Display the default boot message, disable with boot_msg=False
        if boot_msg:
            self.text_out('BUTTECH CAI-1 (C) 1987')
            self.text_out('PRODUCED UNDER CONTRACT FOR THE BUTTE')
            self.text_out('COUNTY BOARD OF EDUCATION')
            self.text_out('')

    def change_resolution(self, target_width, target_height=24):
        # wipes the screen and changes the text mode to the target
        self.width = target_width
        self.height = target_height
        if self.width == 80:
            libtcod.console_set_custom_font('bluebox80.png',
                                            libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        else:
            libtcod.console_set_custom_font('bluebox.png',
                                            libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(self.width, self.height, self.win_name, False)

        # reinitialize self.screen
        self.screen = [[' ' for y in range(self.height)] for x in range(self.width)]
        self.clear_screen()

    def clear_graphics(self):
        # wipes the current graphics layer
        if self.img is not None:
            libtcod.image_clear(self.img, self.background)

    def clear_screen(self):
        # wipes the screen buffer and graphics layer, resets the cursor back to 0,0
        for x in range(self.width):
            for y in range(self.height):
                self.screen[x][y] = ' '
        self.clear_graphics()
        self.cursor.x = 0
        self.cursor.y = 0
        self.display_screen()

    def display_screen(self):
        # display current screen contents, including graphics layer if active
        for x in range(self.width):
            for y in range(self.height):
                libtcod.console_put_char_ex(self.con, x, y, self.screen[x][y], self.foreground, self.background)

        libtcod.console_blit(self.con, 0, 0, self.width, self.height, 0, 0, 0)
        if self.graphics_layer and self.img is not None:
            libtcod.image_set_key_color(self.img, self.background)
            libtcod.image_blit_2x(self.img, 0, 0, 0)
        libtcod.console_flush()

    def draw_point(self, x, y, color=None):
        # draw a pixel to the screen's semigraphics layer
        # fails silently if there is currently no graphics layer
        if color is None:
            color = self.foreground

        if self.graphics_layer and self.img is not None:
            libtcod.image_put_pixel(self.img, x, y, color)
            return

    def set_graphics(self, flag=True):
        # if the graphics layer hasn't been initialized, start it
        self.graphics_layer = flag
        if self.graphics_layer:
            self.img = libtcod.image_new(self.width * 2, self.height * 2)
            libtcod.image_clear(self.img, self.background)

    def text_out(self, text, newline=True):
        # prints the received text to the console, wrapping if needed, and scrolling the screen up if needed
        for i in text:
            # iterate through chars in passed text
            if self.cursor.x >= self.width:
                # if the cursor has hit the end of the line, move to the next line
                self.new_line()

            # update screen at cursor to portion of i
            self.screen[self.cursor.x][self.cursor.y] = i

            # call display_screen to display the new results
            self.display_screen()

            # increment the x position of the cursor in preparation for the next character.
            self.cursor.x += 1

        # end by starting a new line if newline is True
        if newline is True:
            self.new_line()

    def text_in(self, newline=False, prompt=False, prompt_text='> '):
        # takes input from the console, displaying as the user types.
        # the additional arguments are as follows:
        # newline: If true, moves the cursor to a new line before beginning input
        # prompt: If true, prints the contents of prompt_text to the console before taking input
        if newline:
            self.new_line()
        if prompt:
            self.text_out(prompt_text, newline=False)

        # timer for the cursor blink routine
        timer = 0
        text = ""
        first_line = True
        line_count = 0

        # set a leftward margin for the first line of input, so the user can't backspace over the prompt
        left_margin = self.cursor.x
        original_margin = left_margin

        while not libtcod.console_is_window_closed():
            # loop while we wait for the user to type something.

            # check for a key press
            key = libtcod.console_check_for_keypress(libtcod.KEY_PRESSED)

            # increment the timer and create the input accumulator
            timer += 1

            # check the timer multiplier, and if it is the right state, change the cursor character and reset timer
            # in this way, we create a blink effect for the cursor.
            # note that because we do not update self.screen this effect is independent of screen status
            if timer % (self.fps // 4) == 0:
                if timer % (self.fps // 2) == 0:
                    timer = 0
                    self.screen[self.cursor.x][self.cursor.y] = self.cursor.char
                else:
                    self.screen[self.cursor.x][self.cursor.y] = ' '

            if key.vk == libtcod.KEY_BACKSPACE:
                # delete the last character and move the cursor back one space
                if self.cursor.x > left_margin:
                    # move cursor in the same line if the line hasn't wrapped, but only if not empty
                    # ie. at the left_margin
                    self.screen[self.cursor.x][self.cursor.y] = " "
                    text = text[:-1]
                    self.cursor.x -= 1
                elif not first_line:
                    # otherwise, check if this isn't the first line of input, and if it is, backspace to the previous
                    # line
                    self.cursor.y -= 1
                    self.cursor.x = self.width - 1
                    text = text[:-1]
                    line_count -= 1

                    # if the line_count has been reduced back to the first line, reset first line and margin
                    if line_count <= 0:
                        # keep track of number of lines entered, and if back to the first line, reset the flag
                        line_count = 0
                        first_line = True
                        left_margin = original_margin
            elif key.vk == libtcod.KEY_ENTER:
                # insert a new_line and break to the return
                self.new_line()
                break
            elif key.vk == libtcod.KEY_ESCAPE:
                # on an ESC, dump the text buffer and break, thus returning an empty string
                text = ""
                break
            elif key.c > 0:
                # Otherwise, if the character is a real character, we add it to the text buffer and move cursor
                letter = chr(key.c)
                self.screen[self.cursor.x][self.cursor.y] = letter
                self.cursor.x += 1
                if self.cursor.x >= self.width:
                    # if the cursor has exceeded the screen width, we send a new line and tell the rest of the
                    # routine that it's no longer the first line.
                    self.new_line()
                    first_line = False
                text += letter

            # draw the current screen
            self.display_screen()

            # remove the left margin if no longer on the first line
            if not first_line:
                left_margin = 0

        return text

    def new_line(self):
        # sends a new line to the console and updates the screen
        self.cursor.x = 0
        self.cursor.y += 1
        if self.cursor.y >= self.height:
            # if the cursor has hit the end of the screen, scroll screen upward by deleting row 0
            # and appending a new row of blank spaces
            for x in range(self.width):
                del self.screen[x][0]
                self.screen[x].append(' ')
            self.cursor.y -= 1


class Cursor:
    # a simple class for packaging the cursor parameters
    def __init__(self, x=0, y=0, char=chr(176)):
        self.x = x
        self.y = y
        self.char = char