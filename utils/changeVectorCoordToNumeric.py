#!/usr/bin/python3
import sys, json, os


def print_help():
    print()


def parse_args():
    path = ""

    for arg in sys.argv[1:]:
        if arg[0] == "-":
            if len(arg) > 1 and arg[1] == 'h':
                print_help()
                exit(0)
        elif len(path) < 1:
            path = arg
        else:
            print_help()
            exit(-1)

    if len(path) < 1:
        print_help()
        exit(-1)

    return path


def open_file(filename):
    try:
        return open(filename, 'r+')
    except IOError:
        print("Error: can\'t find file or read data")
        exit(-1)
    except Exception as e:
        print (e)
        print("Unexpected error :/")
        exit(-1)


def extract_json_data(fd):
    try:
        return json.loads(fd.read())
    except ValueError:
        print("An error occur during the file is convert in json\n" +
              "For the file :" + fd.name)
        return -1
    except Exception as e:
        print (e)
        print("Unexpected error :/")
        exit(-1)


def isVectorCoordIn(section):
    if isinstance(section, dict):
        for key in section:
            if isinstance(key, str) and key == 'vectorCoord':
                return True
    return False


def extract_numeric_value(string_vector):
    x, y = string_vector.split(';')
    return int(x.split('=')[1]), int(y.split('=')[1])


def rec_parse_json(json):
    for section in json:
        if isVectorCoordIn(section):
            string_vector = section['vectorCoord']
            vector_x, vector_y = extract_numeric_value(string_vector)
            section['vectorCoordX'] = vector_x
            section['vectorCoordY'] = vector_y
        else:
            if not isinstance(section, dict):
                rec_parse_json(json[section])
    return json


def process(file):
    fd = open_file(file)
    _json = extract_json_data(fd)
    if not _json == -1:
        _json = rec_parse_json(_json)
        fd.seek(0)
        fd.truncate()
        fd.write(json.dumps(_json))
        fd.close()
    return


def  rec_read_files(path):
    for filename in os.listdir(path):
        filename = path + '/' + filename
        if filename.endswith('.json'):
            process(filename)
        if (os.path.isdir(filename)):
            rec_read_files(filename)


def main():
    print("Convertion start")
    path = parse_args()
    if os.path.isdir(path):
        rec_read_files(path)
    elif path.endswith('.json'):
        process(path)
    else:
        print('No valid files has been found')
        exit(-1)

if __name__ == "__main__":
    main()