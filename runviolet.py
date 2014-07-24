"""
runviolet.py - The Interpreter object for parsing and executing VIOLET code

"""

import shlex
import libbluebox as bluebox


class Interpreter:
    def __init__(self, program, box):
        self.program = program
        self.box = box

    def run(self):
        self.box.text_out('pork')