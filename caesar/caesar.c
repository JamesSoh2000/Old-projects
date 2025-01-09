#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool only_digits(string s);
char convert(char s, int key);

int main(int argc, string argv[])
{
    // if there is only one argc then pass
    // for looping the given palintext and change it by given 'k' value(my argument)
    // if it's not a single argument(ex: ./caesar 1 2 3) or string,etc... basically other than a single number, just print "Usage: ./caesar key" and return 1



    if (argc == 2 && only_digits(argv[1])) {

        int key = atoi(argv[1]);
        string plain = get_string("plaintext:  ");
        printf("ciphertext: ");
        int length = strlen(plain);

        for (int i = 0; length > i; i++) {

            printf("%c", convert(plain[i], key));
        }
    }else {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    printf("\n");
    return 0;
}

bool only_digits(string s) {
    int length = strlen(s);
    for (int i = 0; length > i; i++) {
        if (isdigit(s[i]) == 0) {
            return false;
        }
    }
    return true;
}

char convert(char s, int key) {
    int upper;
    
    int lower;


    // if it's upper
    if (s >= 65 && s <= 90) {
        upper = ((s - 65) + (key % 26)) % 26;
        upper += 65;
        return (char) upper;
    }else if (s >= 97 && s <= 122) {
        lower = ((s - 97) + (key % 26)) % 26;
        lower += 97;
        return (char) lower;
    }else {
        return s;
    }
    return 0;
}