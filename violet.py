"""
violet.py - Verbose Interpreted Operating Language for Educational Terminals

An interpreter for the CAI-1 "Blue Box" VIOLET programming language
"""

import libbluebox as bluebox


def main_prompt():
    controls = ['BEGIN', 'APPEND', 'INSERT', 'LIST', 'SAVE', 'LOAD', 'RUN', 'EXIT']
    execute = True

    while execute:
        input_control = box.text_in(prompt=True)
        input_control = input_control.split()
        if not input_control:
            box.text_out('EMPTY')
        elif input_control[0] in controls:

            if input_control[0] == 'BEGIN':
                program = entry_mode()
            elif input_control[0] == 'APPEND':
                try:
                    program = entry_mode(program)
                except UnboundLocalError:
                    box.text_out('NO PROGRAM IN MEMORY')
            elif input_control[0] == 'INSERT':
                try:
                    program = insert_mode(program, line=int(input_control[1]))
                except IndexError:
                    box.text_out('MISSING LINE NUMBER')
                except ValueError:
                    box.text_out('NOT A NUMBER')
                except UnboundLocalError:
                    box.text_out('NO PROGRAM IN MEMORY')
            elif input_control[0] == 'LIST':
                for i in range(len(program)):
                    box.text_out(str(i) + '. ' + program[i])
            elif input_control[0] == 'SAVE':
                save_program(program, input_control[1])
            elif input_control[0] == 'LOAD':
                program = load_program(input_control[1])
            elif input_control[0] == 'RUN':
                run_program(program)
            elif input_control[0] == 'EXIT':
                execute = False
        else:
            box.text_out('NOT A COMMAND')

    return


def entry_mode(program=None):
    # the main entry cycle for new or existing programs
    # if started with no arguments, entry_mode begins a new program and starts taking new lines of code
    # if started with a program, it begins appending new lines to the end of program
    if program is None:
        program = []
    entry = True

    index = len(program)
    while entry:
        new_line = box.text_in(prompt=True, prompt_text=str(index) + '. ')
        if new_line != '':
            # entering a blank line exits entry mode
            program.append(new_line)
            index += 1
        else:
            entry = False

    return program


def insert_mode(program, line):
    # inserts lines into the middle of a program after line=
    # first check if line exceeds program length
    if line > len(program):
        box.text_out('LINE OUT OF RANGE')
        return program  # we still have to return program even though we've done nothing to it.

    # call the entry mode with only the first part of the program, in order to feed it the correct length
    insert_block = entry_mode(program[:line])

    # append the other half of the program to the insert_block
    for i in program[line:]:
        insert_block.append(i)

    # return the appended insert_block as the new program
    return insert_block


def save_program(program, name):
    # save the program to a plain text file with name "name"
    f = open(name, mode='w')
    for i in program:
        f.write(i + '\n')
    f.close()
    box.text_out('FILE SAVED AS ' + name)
    return


def load_program(name):
    # load a file into memory for use by the interpreter
    try:
        f = open(name, mode='r')
    except IOError:
        box.text_out('FILE NOT FOUND OR FAULT')
        return

    program = []

    for line in f:
        program.append(line.strip('\n'))

    f.close()
    return program


def run_program(program):
    pass


################################
# initialization and main loop
################################

box = bluebox.BlueBox(width=80)

main_prompt()