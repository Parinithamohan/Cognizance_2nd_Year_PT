#include <assert.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* readline();
char* ltrim(char*);
char* rtrim(char*);

int parse_int(char*);

// Array containing words for numbers 1 to 29
const char* words[] = {
    "o' clock", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "quarter", "sixteen", "seventeen", "eighteen", "nineteen",
    "twenty", "twenty one", "twenty two", "twenty three", "twenty four", "twenty five", "twenty six", "twenty seven", "twenty eight", "twenty nine", "half"
};

char* timeInWords(int h, int m) {
    // Allocate memory for result string
    char* result = malloc(100 * sizeof(char));

    if (m == 0) {
        // Exact hour
        snprintf(result, 100, "%s %s", words[h], words[0]);
    } else if (m == 15) {
        // Quarter past
        snprintf(result, 100, "quarter past %s", words[h]);
    } else if (m == 30) {
        // Half past
        snprintf(result, 100, "half past %s", words[h]);
    } else if (m == 45) {
        // Quarter to next hour
        snprintf(result, 100, "quarter to %s", words[(h % 12) + 1]);
    } else if (m < 30) {
        // Minutes past the hour
        snprintf(result, 100, "%s minute%s past %s", words[m], m == 1 ? "" : "s", words[h]);
    } else {
        // Minutes to the next hour
        snprintf(result, 100, "%s minute%s to %s", words[60 - m], (60 - m) == 1 ? "" : "s", words[(h % 12) + 1]);
    }

    return result;
}

int main() {
    FILE* fptr = fopen(getenv("OUTPUT_PATH"), "w");

    int h = parse_int(ltrim(rtrim(readline())));
    int m = parse_int(ltrim(rtrim(readline())));

    char* result = timeInWords(h, m);

    fprintf(fptr, "%s\n", result);

    fclose(fptr);
    free(result); // Free allocated memory
    return 0;
}

char* readline() {
    size_t alloc_length = 1024;
    size_t data_length = 0;

    char* data = malloc(alloc_length);

    while (true) {
        char* cursor = data + data_length;
        char* line = fgets(cursor, alloc_length - data_length, stdin);

        if (!line) {
            break;
        }

        data_length += strlen(cursor);

        if (data_length < alloc_length - 1 || data[data_length - 1] == '\n') {
            break;
        }

        alloc_length <<= 1;

        data = realloc(data, alloc_length);

        if (!data) {
            data = '\0';
            break;
        }
    }

    if (data[data_length - 1] == '\n') {
        data[data_length - 1] = '\0';
    }

    return data;
}

char* ltrim(char* str) {
    if (!str) {
        return '\0';
    }

    if (!*str) {
        return str;
    }

    while (*str != '\0' && isspace(*str)) {
        str++;
    }

    return str;
}

char* rtrim(char* str) {
    if (!str) {
        return '\0';
    }

    if (!*str) {
        return str;
    }

    char* end = str + strlen(str) - 1;

    while (end >= str && isspace(*end)) {
        end--;
    }

    *(end + 1) = '\0';

    return str;
}

int parse_int(char* str) {
    char* endptr;
    int value = strtol(str, &endptr, 10);

    if (endptr == str || *endptr != '\0') {
        exit(EXIT_FAILURE);
    }

    return value;
}