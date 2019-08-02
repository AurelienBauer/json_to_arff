#!/usr/bin/python3
import sys, json, os, ntpath


def print_help():
    print("usage: <input file or path> <word to research>")


def parse_args():
    path = ""
    word = ""
    distance = 0

    next_value_is_hamming = False

    for arg in sys.argv[1:]:
        if arg[0] == "-":
            if len(arg) > 1 and arg[1] == 'h':
                print_help()
                exit(0)
            if arg == "--hamming":
                next_value_is_hamming = True
        elif next_value_is_hamming:
            distance = int(arg)
            next_value_is_hamming = False
        elif len(path) < 1:
            path = arg
        elif len(word) < 1:
            word = arg
        else:
            print_help()
            exit(-1)

    if len(path) < 1 or len(word) < 1:
        print_help()
        exit(-1)

    return path, word, distance


def rec_read_files(path, word, distance):
    for filename in os.listdir(path):
        filename = path + '/' + filename
        if filename.endswith('.json'):
            process(filename, word, distance)
        if os.path.isdir(filename):
            rec_read_files(filename, word, distance)


def open_file(filename):
    try:
        return open(filename, 'r')
    except IOError:
        print("Error: can\'t find file or read data")
        exit(-1)
    except Exception as e:
        print(e)
        print("Unexpected error :/")
        exit(-1)


def find_word_in_json(_json, word, distance):
    i = 0
    word = word.lower()
    hamming_dist = distance
    word_len = len(word)
    for section in _json:
        for key in _json[section]:
            if key["primaryCode"] > 0:
                if chr(key["primaryCode"]).lower() == word[i]:
                    i += 1
                elif hamming_dist > 0:
                    hamming_dist -= 1
                else:
                    i = 0
                    hamming_dist = distance
            if i >= word_len - distance:
                return True
    return False


def process(path, word, distance):
    fd = open_file(path)
    _json = extract_json_data(fd)
    if _json != -1 and find_word_in_json(_json, word, distance):
        print("Pattern found in file: " + fd.name)


def extract_json_data(fd):
    try:
        return json.loads(fd.read())
    except ValueError:
        print("An error occur during the file is convert in json\n" +
              "For the file :" + fd.name)
        return -1
    except Exception as e:
        print(e)
        print("Unexpected error :/")
        exit(-1)


def main():
    path, word, distance = parse_args()
    if os.path.isdir(path):
        rec_read_files(path, word, distance)
    else:
        process(path, word, distance)


if __name__ == "__main__":
    main()
