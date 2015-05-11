from multi_map import multi_map


def add(a, b):
    return a + b


if __name__ == '__main__':
    print multi_map(add, [1, 2, 3, 4, 5], [6, 7, 8, 9, 10], threads=2)

