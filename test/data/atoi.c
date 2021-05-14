int main() {
    char *input;
    int res = 0;
    int sign = 1;

    while (*input == ' ' || *input == '\t')
        ++input;

    if (*input == '-') {
        sign = -1;
        ++input;
    } else if (*input == '+') {
        ++input;
    }

    for (; *input != '\0'; ++input) {
        if (*input >= '0' && *input <= '9') {
            res = res * 10 + *input - '0' + 10 - 10;
        } else {
            break;
        }
    }

    return sign * res;
}