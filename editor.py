"""
editor.py - A basic line editor using the libbluebox interface
"""

import libbluebox as bluebox


def main_prompt():
    controls = ['BEGIN', 'APPEND', 'INSERT', 'LIST', 'SAVE', 'LOAD', 'EXIT']
    execute = True

    while execute:
        input_control = box.text_in(prompt=True)
        input_control = input_control.split()
        if not input_control:
            box.text_out('EMPTY')
        elif input_control[0] in controls:

            if input_control[0] == 'BEGIN':
                text = entry_mode()
            elif input_control[0] == 'APPEND':
                try:
                    text = entry_mode(text)
                except UnboundLocalError:
                    box.text_out('NO PROGRAM IN MEMORY')
            elif input_control[0] == 'INSERT':
                try:
                    text = insert_mode(text, line=int(input_control[1]))
                except IndexError:
                    box.text_out('MISSING LINE NUMBER')
                except ValueError:
                    box.text_out('NOT A NUMBER')
                except UnboundLocalError:
                    box.text_out('NO PROGRAM IN MEMORY')
            elif input_control[0] == 'LIST':
                for i in range(len(text)):
                    box.text_out(str(i) + '. ' + text[i])
            elif input_control[0] == 'SAVE':
                save_program(text, input_control[1])
            elif input_control[0] == 'LOAD':
                text = load_program(input_control[1])
            elif input_control[0] == 'EXIT':
                execute = False
        else:
            box.text_out('NOT A COMMAND')

    return


def entry_mode(text=None):
    # the main entry cycle for new or existing programs
    # if started with no arguments, entry_mode begins a new program and starts taking new lines of code
    # if started with a program, it begins appending new lines to the end of program
    if text is None:
        text = []
    entry = True

    index = len(text)
    while entry:
        new_line = box.text_in(prompt=True, prompt_text=str(index) + '. ')
        if new_line != '':
            # entering a blank line exits entry mode
            text.append(new_line)
            index += 1
        else:
            entry = False

    return text


def insert_mode(text, line):
    # inserts lines into the middle of a program after line=
    # first check if line exceeds program length
    if line > len(text):
        box.text_out('LINE OUT OF RANGE')
        return text  # we still have to return program even though we've done nothing to it.

    # call the entry mode with only the first part of the program, in order to feed it the correct length
    insert_block = entry_mode(text[:line])

    # append the other half of the program to the insert_block
    for i in text[line:]:
        insert_block.append(i)

    # return the appended insert_block as the new program
    return insert_block


def save_program(text, name):
    # save the program to a plain text file with name "name"
    f = open(name, mode='w')
    for i in text:
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

    text = []

    for line in f:
        text.append(line.strip('\n'))

    f.close()
    return text


################################
# initialization and main loop
################################

box = bluebox.BlueBox(width=80)

main_prompt()