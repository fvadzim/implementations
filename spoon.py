"""Module realizes interpreter of basic esoteric language called
   BrainFuck. Also provides with the converter from Spoon esoteric
   language to BF.
"""
import argparse
import sys

INT_MAX = 2147483648
INT_MIN = -2147483649


class EsotericLanguageConverter:
    """
        Converter interface with
        methods to be implemented.
    """
    @staticmethod
    def convert_to_brain_fuck(_input):
        """:param _input: string representing the code in esoteric language
            :return: code in BrainFuck language
        """
        raise NotImplementedError


class SpoonConverter(EsotericLanguageConverter):
    """
        Converter from Spoon to BrainFuck
    """
    @staticmethod
    def convert_to_brain_fuck(_input):
        """
            :param _input: code in Spoon
            :return: BrainFuck code
        """
        start = 0
        convert_dict = {
            "1": "+",
            "000": "-",
            "010": ">",
            "011": "<",
            "00100": "[",
            "0011": "]",
            "001010": ".",
            "0010110": ","
        }
        brain_fuck_input = ''
        while start < len(_input):
            is_command_found = False
            for key in convert_dict:
                if _input[start: start + len(key)] == key:
                    start += len(key)
                    brain_fuck_input += convert_dict[key]
                    is_command_found = True
            if not is_command_found:
                raise SyntaxError("Unexpected commands found")
        return brain_fuck_input


class EsotericParser:
    """
        Parser interface with
        methods to be implemented.
    """
    @staticmethod
    def get_command_list(code):
        """:param code: string representing the code in esoteric language
           :return: list of commands
        """
        raise NotImplementedError


class SpoonParser(EsotericParser):
    """
        Parser of Spoon code
    """
    @staticmethod
    def get_command_list(code):
        possible_commands = [
            "1", "000", "010", "011",
            "00100", "0011", "001010", "0010110"]

        if any(symbol not in ('0', '1', '\n', ' ') for symbol in code):
            raise SyntaxError(
                "Spoon code should consist of binary symbols only")
        spoon_commands = []
        spoon_sub_code = code.split()
        for sub_code in spoon_sub_code:
            start = 0
            while start < len(sub_code):
                is_command_found = False
                for possible_command in possible_commands:
                    if sub_code[start: start + len(possible_command)] \
                            == possible_command:
                        spoon_commands += possible_command
                        start += len(possible_command)
                        is_command_found = True
                if not is_command_found:
                    raise SyntaxError("Unexpected commands found")
        return spoon_commands


class BrainLuck:
    """Implements BrainFuck interpreter
    """
    def __init__(self):
        self.cells = [0] * 60000
        self.while_pointers = []
        self.command_index = 0
        self.data_index = 30000
        self.commands = None
        self.last_commands = None

    def go_to_next_cell(self):
        """increases index of data cell
            :return: None
        """
        self.data_index += 1

    def go_to_prev_cell(self):
        """decreases index of data cell
            :return: None
        """
        self.data_index -= 1

    def increase_cell(self):
        """increases index of data cell
            :return: None
        """
        self.cells[self.data_index] = (
            self.cells[self.data_index] + 1) % INT_MAX

    def decrease_cell(self):
        """decreases index of data cell
            :return: None
        """
        self.cells[self.data_index] = (
            self.cells[self.data_index] - 1)
        if self.cells[self.data_index] < 0:
            self.cells[self.data_index] %= INT_MIN

    def get_char(self):
        """reads one char from stream i/o
            :return: None
        """
        _input = sys.stdin.read(1)
        if _input:
            self.cells[self.data_index] = ord(_input)
        else:
            self.cells[self.data_index] = 0

    def put_char(self):
        """prints current data cell to stream i/o
            :return: None
        """
        sys.stdout.write(chr(self.cells[self.data_index]))

    def start_cycle(self):
        """
            starts cycle from "[" if value of current data cell is positive
            else jumps to paired "]" according to the nesting
            :return: None
        """
        if self.cells[self.data_index] == 0:
            self.command_index = self.while_pointers[self.command_index]

    def decrease_cycle(self):
        """
            ends cycle started from paired "] if data cell is 0
            else jumps to paired "]" according to the nesting
            :return: None
        """
        if self.cells[self.data_index] != 0:
            self.command_index = self.while_pointers[self.command_index]

    def interpret(self, commands):
        """
            Performs code in BrainFuck. Prints to Stream I/O.
            Reads from Stream I/O.
            :param commands - code in BrainFuck.
            :return: None
        """
        if not isinstance(commands, str):
            raise ValueError(
                "commands argument must be of type str")
        self.last_commands = self.commands = (
            commands if commands else self.last_commands)
        self.while_pointers = [0] * len(commands)

        stack = []

        for index, token in enumerate(commands):
            if token == "[":
                stack.append(index)
            elif token == "]":
                self.while_pointers[stack[-1]] = index
                self.while_pointers[index] = stack.pop()

        while self.command_index < len(commands):
            self.command_dict[commands[self.command_index]](self)
            self.command_index += 1

        self.commands = None
        self.command_index = 0
        self.data_index = 0

    def repeat_last_command(self):
        """If someone wants to repeat last command =)
            :return: None
        """
        self.interpret(self.last_commands)

    command_dict = {
        ">": go_to_next_cell,
        "<": go_to_prev_cell,
        "+": increase_cell,
        "-": decrease_cell,
        ".": put_char,
        ",": get_char,
        "[": start_cycle,
        "]": decrease_cycle
    }


def main():
    """
        Allows using module as script
        python3 spoon.py path_to_spoon_code
        :return: None
    """
    file_names_parser = argparse.ArgumentParser(description='''
            Get input and output file's  names''')
    file_names_parser.add_argument('spoon_file',
                                   help='path to spoon_file')
    parser_args = file_names_parser.parse_args()

    spoon = BrainLuck()
    _input = open(parser_args.spoon_file).read()
    converted_commands = SpoonConverter.convert_to_brain_fuck(
        ''.join(SpoonParser.get_command_list(_input)))
    spoon.interpret(converted_commands)


if __name__ == "__main__":
    main()
