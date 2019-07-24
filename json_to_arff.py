#!/usr/bin/python3
import sys, json, os, ntpath

PARAMS_LIST = "abcdefgijklmnop"

attributes = {
    "a": {
        "name": "primaryCode",
        "type": "NUMERIC"
    },
    "b": {
        "name": "XOnPress",
        "type": "NUMERIC"
    },
    "c": {
        "name": "XOnRelease",
        "type": "NUMERIC"
    },
    "d": {
        "name": "YOnPress",
        "type": "NUMERIC"
    },
    "e": {
        "name": "YOnRelease",
        "type": "NUMERIC"
    },
    "f": {
        "name": "NoKeyPressDelay",
        "type": "NUMERIC"
    },
    "g": {
        "name": "KeyPressDelay",
        "type": "NUMERIC"
    },
    "i": {
        "name": "PressureOnPress",
        "type": "NUMERIC"
    },
    "j": {
        "name": "PressureOnRelease",
        "type": "NUMERIC"
    },
    "k": {
        "name": "vectorCoord",
        "type": "STRING"
    },
    "l": {
        "name": "RotationVectorOnPress",
        "type": "NUMERIC"
    },
    "m": {
        "name": "RotationVectorOnRelease",
        "type": "NUMERIC"
    },
    "n": {
        "name": "LinearAccelerationOnPress",
        "type": "NUMERIC"
    },
    "o": {
        "name": "LinearAccelerationOnRelease",
        "type": "NUMERIC"
    },
    "p": {
        "name": "keyLabel",
        "type": "STRING"
    },
    "q": {
        "name": "vectorCoordX",
        "type": "NUMERIC"
    },
    "r": {
        "name": "vectorCoordY",
        "type": "NUMERIC"
    },
}


def print_help():
    print(" usage: json_to_arff.py [-abcdefgijklmnop] <input file path> <output file path>\n"
          " options [lmno] could be following by a number between 0 and 5, if no number are choosen the default value is 5.\n")
    for attr in attributes:
        print(attr + " = " + attributes[attr]['name'])


def parse_args():
    params = ""
    in_file = ""
    out_file = ""

    for arg in sys.argv[1:]:
        if arg[0] == "-":
            if len(arg) > 1 and arg[1] == 'h':
                print_help()
                exit(0)
            params += arg[1:]
        elif len(in_file) < 1:
            in_file = arg
        elif len(out_file) < 1:
            out_file = arg
        else:
            print_help()
            exit(-1)

    if len(in_file) < 1 or len(out_file) < 1:
        print_help()
        exit(-1)

    if len(params) < 1:
        params = PARAMS_LIST
    return params, in_file, out_file


def open_parse_file(in_file):
    try:
        file = open(in_file, 'r')
        _json = json.loads(file.read())
        return _json, path_leaf(file.name)
    except IOError:
        print("Error: can\'t find file or read data")
        exit(-1)
    except ValueError:
        print("An error occur during the file is convert in json")
        exit(-1)
    except Exception as e:
        print (e)
        print("Unexpected error :/")
        exit(-1)


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def create_output_file(out_file, in_file_name):
    try:
        if os.path.isdir(out_file):
            if out_file[-1:] != "/":
                out_file += '/'
            out_file += in_file_name + ".arff"

        if os.path.exists(out_file) and os.path.isfile(out_file):
            print("File already exist and it was removed.")
            os.remove(out_file)

        fd = open(out_file, 'w+')
        fd.write(   "% Generate by Json_to_arff script\n" +
                    "% Author: Aurélien Bauer\n" +
                    "% For an academic project at the University of Kent\n"+
                    "@RELATION continuous_authentication\n\n")
        return fd
    except IOError as e:
        print(e)
        exit(-1)


def parse_number_in_params(next_letter):
    if next_letter.isdigit():
        nbr = int(next_letter)
        return 5 if nbr > 5 else nbr
    return 5


def transform_attributes_string(name, type):
    return "@ATTRIBUTE " + name + ' ' + type + "\n"


def format_hard_sensors_data(letter, next_letter, key):
    line = ""
    j = parse_number_in_params(next_letter)

    for coord in "xyz":
        i = 0
        while i < j:
            line += json.dumps(key[attributes[letter]['name']][coord][i]) + ","
            i += 1
    return line


def format_hard_sensors_attributes(letter, next_letter):
    line = ""
    j = parse_number_in_params(next_letter)

    for coord in "XYZ":
        i = 0
        while i < j:
            line += transform_attributes_string(attributes[letter]['name'] + coord + str(i), attributes[letter]['type'])
            i += 1

    return line


def write_attributes_data(fd, json_data, params):
    i = 0
    for letter in params:
        if letter in PARAMS_LIST:
            if letter in "lmno":
                next_letter = "" if len(params) <= (i+1) else params[i+1]
                line = format_hard_sensors_attributes(letter, next_letter)
            else:
                line = transform_attributes_string(attributes[letter]['name'], attributes[letter]['type'])
            fd.write(line)
        i += 1

    fd.write("\n@DATA\n")

    for section in json_data:
        for key in json_data[section]:
            line = ""
            i = 0
            for letter in params:
                if letter in PARAMS_LIST:
                    if letter in "lmno":
                        next_letter = "" if len(params) <= (i+1) else params[i + 1]
                        line += format_hard_sensors_data(letter, next_letter, key)
                    else:
                        line += json.dumps(key[attributes[letter]['name']]) + ","
                i += 1
            fd.write(line[:-1] + '\n')


def main():
    params, in_file, out_file = parse_args()
    json_data, in_file_name = open_parse_file(in_file)
    out_file_fd = create_output_file(out_file, in_file_name)
    write_attributes_data(out_file_fd, json_data, params)
    print("Arff file has been generated: " + out_file_fd.name)


if __name__ == "__main__":
   main()