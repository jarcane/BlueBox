"""
runviolet.py - The Interpreter object for parsing and executing VIOLET code

"""

import shlex


class Interpreter:
    def __init__(self, program, box, pointer=0, w_pointer=0, running=False):
        self.program = program
        self.box = box

        # initialize the pointer and stored pointer used by WHILE
        self.pointer = pointer
        self.w_pointer = w_pointer

        # set the 'running' flag, which is used by self.run to know if it should keep executing.
        self.running = running

        # establishing the operator lexicon
        self.lex = ['PROGRAM', 'IGNORE', 'IF', 'IFY', 'IFN', 'WHILE', 'WHEND', 'GOTO', 'SET', 'PRINT',
                    'PROMPT', 'ADD', 'SUB', 'MULT', 'DIV']

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
        while self.running:
            # parse the next line of the program
            exec_line = shlex.split(self.program[self.pointer])

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

        return

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
        elif line[0] == 'SET':
            return self.set(line[1], line[2])
        elif line[0] == 'PRINT':
            output = ''
            for i in line[1:]:
                output += ' ' + str(self.name_lookup(i))
            self.box.text_out(output)
            return 'SUCCESS', 1
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
        print test

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
        if result is None:
            return 'WRONG TEST OPERATOR', 0
        elif result:
            r = 1
        elif not result:
            r = 0

        return 'SUCCESS', r

    def set(self, name, value):
        # create a new variable or modify an existing one with the value given
        if name[0] == '#':
            try:
                value = int(value)
            except ValueError:
                return 'TYPE ERROR', 0
        elif name[0] == '%':
            try:
                value = float(value)
            except ValueError:
                return 'TYPE ERROR', 0
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
        if x[0] in ['#', '%', '$', '&']:
            if x in self.names.keys():
                return self.names[x]
            else:
                return None
        else:
            return x