#!/usr/bin/python3
import sys, json, os, ntpath

PARAMS_LIST = "abcdefgijklmnopqrstuv"

HEADER =    "% Generate by Json_to_arff script\n" \
            "% Author: Aurélien Bauer\n" \
            "% For an academic project at the University of Kent\n" \
            "@RELATION continuous_authentication\n\n"

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
    "s": {
        "name": "position",
        "type": "{ VerticalDominantOnlySit,"
                " VerticalDominantOnlyWalk,"
                " VerticalBothBandsSit,"
                " VerticalBothBandsWalk,"
                " VerticalIndexFingerOnlySit,"
                " VerticalIndexFingerOnlyWalk,"
                " HorizontalBothHandsSit,"
                " HorizontalBothHandsWalk,"
                "unknownPosition }"
    },
    "t": {
        "name": "UpUpTime",
        "type": "NUMERIC"
    },
    "u": {
        "name": "DownDownTime",
        "type": "NUMERIC"
    },
    "v": {
        "name": "LatencyTime",
        "type": "NUMERIC"
    }
}

UNKNOWN_POSITION = "unknownPosition"

position = {
    "GDYESVD": "VerticalDominantOnlySit",
    "UTRBWVD": "VerticalDominantOnlyWalk",
    "TRYGSVX": "VerticalBothBandsSit",
    "HTRGWVX": "VerticalBothBandsWalk",
    "BVOYSVI": "VerticalIndexFingerOnlySit",
    "ZXGHWVI": "VerticalIndexFingerOnlyWalk",
    "FGSWSHB":  "HorizontalBothHandsSit",
    "PDJTWHB": "HorizontalBothHandsWalk",
}


def print_help():
    print(" usage: json_to_arff.py [-abcdefgijklmnoprs] <input file path> <output file path>\n"
          " options [lmno] could be following by a number between 0 and 5, if no number are choosen the default value is 5.\n")
    for attr in attributes:
        print(attr + " = " + attributes[attr]['name'])


def parse_args():
    params = ""
    spe_params = list()
    in_file = ""
    out_file = ""

    for arg in sys.argv[1:]:
        if len(arg) >= 2 and arg[0] == "-" and arg[1] != "-":
            if len(arg) > 1 and arg[1] == 'h':
                print_help()
                exit(0)
            params += arg[1:]
        elif len(arg) >= 2 and arg[0] == "-" and arg [1] == "-":
            spe_params.append(arg)
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

    if not any((c in PARAMS_LIST)  for c in params):
        params += PARAMS_LIST
    return params, in_file, out_file, spe_params


def open_parse_file(in_file):
    try:
        file = open(in_file, 'r')
        _json = json.loads(file.read())
        return _json, path_leaf(file.name)
    except IOError:
        print("Error: can\'t find file or read data")
        exit(-1)
    except ValueError:
        print("An error occur during the file is convert in json : " + in_file)
        return -1, -1
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
            print("The File already exist: " + out_file + ".")
            os.remove(out_file)

        fd = open(out_file, 'w+')
        fd.write(HEADER)
        return fd
    except IOError as e:
        print(e)
        exit(-1)


def open_output_file(out_file):
    try:
        if os.path.isdir(out_file):
            if out_file[-1:] != "/":
                out_file += '/'
            out_file += "out.json.arff"

        if not (os.path.exists(out_file) and os.path.isfile(out_file)):
            return create_output_file(out_file, "out.json")

        return open(out_file, 'a+')
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
            if attributes[letter]['name'] in key:
                if len(key[attributes[letter]['name']][coord]) > i:
                    line += json.dumps(key[attributes[letter]['name']][coord][i]) + ","
                else:
                    line += str(-1) + ","
            i += 1
    return line


def format_hard_sensors_attributes(letter, next_letter, attributes_number):
    line = ""
    j = parse_number_in_params(next_letter)

    for coord in "XYZ":
        i = 0
        while i < j:
            line += transform_attributes_string(attributes[letter]['name'] + coord + str(i), attributes[letter]['type'])
            i += 1
            attributes_number += 1

    return line, attributes_number


def compute_upup(json_data):
    if json_data is not None and 'NoKeyPressDelay' in json_data:
        return str(json_data['NoKeyPressDelay'] + json_data ['KeyPressDelay'])
    return str(-1)


def compute_downdown(old_json_data, json_data):
    if old_json_data is not None and 'NoKeyPressDelay' in json_data:
        return str(old_json_data['KeyPressDelay'] + json_data ['NoKeyPressDelay'])
    return str(-1)


def compute_latency(old_json_data, json_data):
    if old_json_data is not None and 'NoKeyPressDelay' in json_data:
        return str(old_json_data['KeyPressDelay'] + json_data ['NoKeyPressDelay'] + + json_data ['KeyPressDelay'])
    return str(-1)


def write_data_default(letter, key):
    if attributes[letter]['name'] in key:
        return json.dumps(key[attributes[letter]['name']])
    else:
        return "-1"


def write_attributes_data(fd, json_data, params):
    i = 0
    attributes_number = 0
    if fd.tell() == len(HEADER)+1:
        for letter in params:
            if letter in PARAMS_LIST:
                if letter in "lmno":
                    next_letter = "" if len(params) <= (i+1) else params[i+1]
                    line, attributes_number = format_hard_sensors_attributes(letter, next_letter, attributes_number)
                else:
                    line = transform_attributes_string(attributes[letter]['name'], attributes[letter]['type'])
                    attributes_number += 1
                fd.write(line)
            i += 1

        fd.write("\n%Number of features: " + str(attributes_number) + "\n\n@DATA\n")

    for section in json_data:
        old_key = None
        for key in json_data[section]:
            line = ""
            i = 0
            for letter in params:
                if letter in PARAMS_LIST:
                    if letter in "lmno":
                        next_letter = "" if len(params) <= (i+1) else params[i + 1]
                        line += format_hard_sensors_data(letter, next_letter, key)
                    elif letter == "s":
                        if section in position:
                            line += position[section] + ","
                        else:
                            line += UNKNOWN_POSITION + ","
                    elif letter == "t":
                        line += compute_upup(key) + ","
                    elif letter == "u":
                        line += compute_downdown(old_key, key) + ","
                    elif letter == "v":
                        line += compute_latency(old_key, key) + ","
                    else:
                        line += write_data_default(letter, key) + ","
                i += 1
            fd.write(line[:-1] + '\n')
            old_key = key


def rec_read_files(params, in_file, out_file, spe_params):
    for filename in os.listdir(in_file):
        filename = in_file + '/' + filename
        if filename.endswith('.json'):
            process(params, filename, out_file, spe_params)
        if os.path.isdir(filename) and 'R' in params:
            rec_read_files(params, filename, out_file, spe_params)


def process(params, in_file, out_file, spe_params):
    json_data, in_file_name = open_parse_file(in_file)
    if not json_data == -1:
        if "--concat" in spe_params:
            out_file_fd = open_output_file(out_file)
        else:
            out_file_fd = create_output_file(out_file, in_file_name)
        write_attributes_data(out_file_fd, json_data, params)
        print("[Json To Arff] Processing complete for the files: input => " + in_file_name + ", output => " + out_file_fd.name)
        out_file_fd.close()


def main():
    params, in_file, out_file, spe_params = parse_args()
    if os.path.isdir(out_file):
        rec_read_files(params, in_file, out_file, spe_params)
    else:
        process(params, in_file, out_file, spe_params)


if __name__ == "__main__":
   main()