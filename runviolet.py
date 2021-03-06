"""
runviolet.py - The Interpreter object for parsing and executing VIOLET code

Copyright 2014 by John S. Berry III.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import shlex


class Interpreter:
    def __init__(self, program, box, pointer=0, running=False):
        self.program = program
        self.box = box

        # initialize the pointer and stored pointer used by WHILE
        self.pointer = pointer
        self.w_pointer = []

        # set the 'running' flag, which is used by self.run to know if it should keep executing.
        self.running = running

        # establishing the operator lexicon
        self.lex = ['PROGRAM', 'IGNORE', 'IF', 'IFY', 'IFN', 'WHILE', 'WHEND', 'GOTO', 'SET', 'PRINT',
                    'PROMPT', 'PRINTLINES', 'ADD', 'SUB', 'MULT', 'DIV']

        # establishing text operator lexicon
        self.test_lex = {
            'EQUALS': '==',
            'NOTEQ': '!=',
            'GREATER': '>',
            'LESSER': '<',
            'AND': 'and',
            'OR': 'or'
        }

        # establishing the variable namespace
        self.names = {
            '&LAST': 0
        }

    def run(self):
        # the main execution loop for the interpreter
        # first check to see if it's running, and if it's not, check the first line of program
        # to see if it should
        # At this point, the interpreter will exit if the listing is not bookended properly
        #  with PROGRAM START and PROGRAM STOP
        if not self.running:
            program_start = shlex.split(self.program[self.pointer])
            if program_start[0] == 'PROGRAM' and program_start[1] == 'START':
                program_stop = shlex.split(self.program[len(self.program) - 1])
                if program_stop[0] == 'PROGRAM' and program_stop[1] == 'STOP':
                    self.running = True
                else:
                    self.box.text_out('PROGRAM DOES NOT STOP')
                    return
            else:
                self.box.text_out('PROGRAM DOES NOT START')
                return

        # Main execution loop
        while self.running and not self.box.check_interrupt():
            # check the pointer to make sure some errant GOTO hasn't left the program space
            if self.pointer > len(self.program):
                self.box.text_out('ERROR - POINTER HAS LEFT THE PROGRAM')
                return

            # parse the next line of the program
            exec_line = self.parse(self.program[self.pointer])

            # execute the code, receiving back a signal string and new &LAST
            evaluate = self.execute(exec_line)
            if evaluate[0] == 'SUCCESS' or evaluate[0] == 'START':
                # increment the pointer
                self.pointer += 1
                self.names['&LAST'] = evaluate[1]
            elif evaluate[0] == 'STOP':
                self.running = False
            else:
                self.box.text_out(evaluate[0] + ' IN LINE ' + str(self.pointer))
                self.running = False

        self.box.text_out('PROGRAM STOP AT LINE ' + str(self.pointer))

        return

    @staticmethod
    def parse(line):
        # parse an incoming line of code and return it as a list of tokens
        token_list = shlex.split(line)

        # step through the token list, and properly convert numeric values to their appropriate types
        for i in range(len(token_list)):
            try:
                token_list[i] = float(token_list[i])
            except ValueError:
                pass
            try:
                token_list[i] = int(token_list[i])
            except ValueError:
                pass
        return token_list

    def execute(self, line):
        # execute the operator in a parsed line of code
        # all successful executions return a tuple, containing a message to run() and the new &LAST value

        # check the lexicon for the operator
        if line[0] not in self.lex:
            return 'SYNTAX ERROR', 0

        # The IGNORE operator has no function, and simply passes a successful execution
        if line[0] == 'IGNORE':
            return 'SUCCESS', 1
        elif line[0] == 'PROGRAM':
            return line[1], 1
        elif line[0] == 'IF':
            return self.do_if(line[1], line[2], line[3])
        elif line[0] == 'IFY':
            if self.names['&LAST'] == 1:
                self.execute(line[1:])
                return 'SUCCESS', 1
            else:
                return 'SUCCESS', 0
        elif line[0] == 'IFN':
            if self.names['&LAST'] == 0:
                self.execute(line[1:])
                return 'SUCCESS', 0
            else:
                return 'SUCCESS', 1
        elif line[0] == 'WHILE':
            test = self.test(line[1], self.name_lookup(line[2]), self.name_lookup(line[3]))
            if test:
                self.w_pointer.append(self.pointer)
                return 'SUCCESS', 1
            elif not test:
                count = 0
                inners = 0
                for i in self.program[self.pointer:]:
                    if 'WHEND' in i:
                        if inners <= 1:
                            self.pointer += count
                            break
                        else:
                            inners -= 1
                    elif 'WHILE' in i:
                        inners += 1
                    count += 1
                return 'SUCCESS', 0
        elif line[0] == 'WHEND':
            if len(self.w_pointer) != 0:
                self.pointer = self.w_pointer.pop() - 1
            return 'SUCCESS', 1
        elif line[0] == 'GOTO':
            if not isinstance(self.name_lookup(line[1]), str):
                if self.name_lookup(line[1]) is not None:
                    self.pointer = int(self.name_lookup(line[1])) - 1
                else:
                    return 'REFERENCE ERROR', 0
            return 'SUCCESS', 1
        elif line[0] == 'SET':
            return self.set(line[1], line[2])
        elif line[0] == 'ADD':
            for i in range(len(line[1:])):
                index = i + 1
                line[index] = self.name_lookup(line[index])
            try:
                total = sum(line[1:])
            except TypeError:
                try:
                    total = ''.join(line[1:])
                except TypeError:
                    return 'TYPE MISMATCH', 0
            return 'SUCCESS', total
        elif line[0] == 'SUB':
            try:
                value = self.name_lookup(line[1]) - self.name_lookup(line[2])
                return 'SUCCESS', value
            except TypeError:
                return 'ERROR - SUB NEEDS NUMBERS', 0
        elif line[0] == 'MULT':
            try:
                total = 1
                for i in line[1:]:
                    total *= self.name_lookup(i)
                return 'SUCCESS', total
            except TypeError:
                return 'ERROR - MULT NEEDS NUMBERS', 0
        elif line[0] == 'DIV':
            try:
                value = self.name_lookup(line[1]) / self.name_lookup(line[2])
                return 'SUCCESS', value
            except TypeError:
                return 'ERROR - DIV NEEDS NUMBERS', 0
        elif line[0] == 'PRINT':
            output = ''
            for i in line[1:]:
                output += ' ' + str(self.name_lookup(i))
            self.box.text_out(output)
            return 'SUCCESS', 1
        elif line[0] == 'PRINTLINES':
            for i in line[1:]:
                self.box.text_out(i)
            return 'SUCCESS', 1
        elif line[0] == 'PROMPT':
            return self.prompt(*line[1:])

        # If execute has got this far, it's failed, so we let the run loop know it did
        return 'RUNTIME ERROR', 0

    def test(self, operator, x, y):
        # performs a test comparing x and y with operator (if valid)

        # check if the operator is valid
        if operator not in self.test_lex.keys():
            return None

        # check if the parameters are strings and rewrap with "" if they are
        string = 'str'  # make a string to compare the object types
        if type(x) == type(string):
            x = '"' + x + '"'
        else:
            x = str(x)
        if type(y) == type(string):
            y = '"' + y + '"'
        else:
            y = str(y)

        # construct the test
        test = x + self.test_lex[operator] + y

        # eval the test
        result = eval(test)

        return result

    def do_if(self, test, x, y):
        # handle the IF tests, with name substitution for variables.
        # look up x and y in the namespace and return with an error if they're bad variables
        x = self.name_lookup(x)
        y = self.name_lookup(y)
        if y is None or x is None:
            return 'UNDEFINED VARIABLE', 0

        result = self.test(test, x, y)
        r = None
        if result is None:
            return 'WRONG TEST OPERATOR', 0
        elif result:
            r = 1
        elif not result:
            r = 0
        return 'SUCCESS', r

    def set(self, name, value):
        # create a new variable or modify an existing one with the value given
        value = self.name_lookup(value)
        if name[0] == '#':
            try:
                value = int(value)
            except ValueError:
                return 'TYPE ERROR - NOT AN INT', 0
        elif name[0] == '%':
            try:
                value = float(value)
            except ValueError:
                return 'TYPE ERROR - NOT A FLOAT', 0
        elif name[0] == '$':
            value = str(value)
        elif name[0] == '&':
            return 'ILLEGAL ASSIGNMENT', 0
        else:
            return 'NOT A VALID NAME', 0
        self.names[name] = value
        return 'SUCCESS', value

    def name_lookup(self, x):
        # look up a given value in the names dict and return the value or the new value if in names
        if not isinstance(x, str):
            return x
        if x[0] in ['#', '%', '$', '&']:
            if x in self.names.keys():
                return self.names[x]
            else:
                return None
        else:
            return x

    def prompt(self, data_type, prompt=None):
        # present an input prompt to the user, and return a value of the requested type
        if data_type not in ['#', '%', '$']:
            return 'MISSING OR INCORRECT TYPE', 0

        output = None
        while output is None:
            if prompt is None:
                data = self.box.text_in(prompt=True)
            else:
                data = self.box.text_in(prompt=True, prompt_text=prompt)

            if data == '' and self.box.check_interrupt():
                return 'BREAK', 0

            if data_type == '#':
                try:
                    output = int(data)
                except ValueError:
                    self.box.text_out('WRONG TYPE - NEEDS INTEGER')
            elif data_type == '%':
                try:
                    output = float(data)
                except ValueError:
                    self.box.text_out('WRONG TYPE - NEEDS FLOATING POINT')
            elif data_type == '$':
                output = data

        return 'SUCCESS', output