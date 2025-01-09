#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool check_validity(string s);
char convert(char c, string key);

int main(int argc, string argv[])
{
    string key = argv[1];

    if (argc != 2) {
        printf("Usage: ./substitution key\n");
        return 1;
    }else if (!check_validity(key)) {
        printf("Key must contain 26 characters.\n");
        return 1;
    }



    string plain = get_string("plaintext:  ");
    int length = strlen(plain);
    printf("ciphertext: ");
    char cipher_char;


    for (int i = 0; length > i; i++) {
        cipher_char = convert(plain[i], key);
        printf("%c", cipher_char);
    }


    printf("\n");
    return 0;
}


bool check_validity(string s) {
    int length = strlen(s);
    int check = 0;
    int duplicate = 0;
    int buf[26];

    if (length != 26) {

        return false;
    }

    for (int i = 0; 26 > i; i++) {
        buf[i] = -1;
    }

    for (int i = 0; length > i; i++) {

        if (!isalpha(s[i])) {

            return false;
        }

        // 각 알파벳은 키에 '하나' 밖에 존재할 수 밖에 없기 때문에 26개의 키가 제대로 입력되었다면 버퍼의 형태는
        //  a,b,c .... 순서대로 0인덱스부터 있을것이다. 그러므로 같은 알파벳이 한번더 나오면 그자리엔 이미 1(이미 한번언급됨)이 있으므로 바로 false
        if (buf[tolower(s[i]) - 'a'] != -1) { // buf[(tolower(s[i]) - 97)]) 와 같음

            return false;
        }else {
            buf[tolower(s[i]) - 'a'] = 1;
        }
    }

    return true;
}

char convert(char c, string key) {
    int upper;
    int lower;
    char replace1;
    char replace2;

    if (c >= 65 && c <= 90) {
        upper = c - 65;
        if (islower(key[upper])) {
            replace1 = toupper(key[upper]);
        }else {
            replace1 = key[upper];
        }

        return replace1;
    }else if (c >= 97 && c <= 122) {
        lower = c - 97;

        if (islower(key[lower])) {
            replace2 = key[lower];
        }else {
            replace2 = key[lower] + 32;
        }
        return replace2;
    }else {
        return c;
    }
    return 0;
}

/* :( encrypts "This is CS50" as "Cbah ah KH50" using yukfrnlbavmwzteogxhcipjsqd as key
    output not valid ASCII text
:( encrypts "This is CS50" as "Cbah ah KH50" using YUKFRNLBAVMWZteogxhcipjsqd as key
    output not valid ASCII text

:( handles duplicate characters in key
    timed out while waiting for program to exit
:( handles multiple duplicate characters in key
    timed out while waiting for program to exit
*/