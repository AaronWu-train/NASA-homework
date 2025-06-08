#include <bits/stdc++.h>
using namespace std;
char key[9]      = "nAs42O2S";
char pattern[40] = {'&',  '\x16', 'B',    '\x06', 'I',  '\'',   'e',  'c',
                    '1',  'y',    '&',    '`',    'm',  '\x18', '[',  '\a',
                    '&',  '\x1E', '\x01', '\a',   'd',  '|',    '`',  ' ',
                    '\v', '\x1E', '\x16', 'z',    '\v', '~',    '|',  '\x16',
                    ']',  '3',    '\x1A', 'Z',    'u',  '2',    '\0', '\0'};
int  flag_len    = 38;
int  key_len     = 8;

int main() {
    for (int i = 0; i < flag_len; ++i) {
        pattern[i] ^= key[i % key_len];
    }
    printf("%s\n", pattern);
}