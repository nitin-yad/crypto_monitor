# -*- coding: utf-8 -*-


def write_to_file(ids):
    f = open("test.txt", "a+")
    f.write(ids)
    f.close()


def read_file():
    f = open("test.txt", "r+")
    ids = []
    for line in f:
        ids = line.split(",")
    f.close()
    ids.remove('')
    return ids


if __name__ == "__main__":
    ids1 = [1, 2]
    write_to_file(','.join(map(str, ids1)))
    write_to_file(",")
    ids2 = [3, 4]
    write_to_file(','.join(map(str, ids2)))
    write_to_file(",")
    print(read_file())
