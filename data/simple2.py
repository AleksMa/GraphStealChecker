import time


def main():
    m = 2
    n = 3
    uselessVar = True
    if uselessVar:
        time.time()
    k = m + n + (6 + 2 * 11) / 14 - 2
    j = 0
    while j < 10:
        if j > 3:
            print(m)
        else:
            print(k)
        j += 1


if __name__ == "__main__":
    main()
