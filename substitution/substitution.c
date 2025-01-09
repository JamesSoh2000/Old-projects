#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool check_validity(string s);
char convert(char c, string key);

int main(int argc, string argv[])
{
    // argc != 2, same alphabet in key, is everysingle letter of key is an alphabet? -- first cases to check
    // length of key is 26 -- 2cond case to check

    if (argc != 2) {
        printf("Usage: ./substitution key\n");
        return 1;
    }else if (!check_validity(argv[1])) {
        return 1;
    }

    // Now, it's time to convert each char of our plaintext after checking key's validity.
    //

    string key = argv[1];
    char char_key;
    string plain = get_string("plaintext:  ");
    int length = strlen(plain);
    printf("ciphertext: ");

    for (int i = 0; length > i; i++) {
        char_key = convert(plain[i], key);
        printf("%c", char_key);
    }

    printf("\n");
    return 0;
}

bool check_validity(string key) {
    int length = strlen(key);
    int buf[26];

    if (length != 26) {
        printf("Key must contain 26 characters.\n");
        return false;
    }

    for (int i = 0; 26 > i; i++) {
        if (!isalpha(key[i])) {
            printf("Key must contain 26 characters.\n");
            return false;
        }
        buf[i] = -1;
    }

    for (int i = 0; 26 > i; i++) {
        if (!isalpha(key[i])) {
            printf("Usage: ./substitution key\n");
            return false;
        }else if (buf[tolower(key[i]) - 'a' ] != -1) {
            printf("Usage: ./substitution key\n");
            return false;
        }else {
            buf[tolower(key[i]) - 'a' ] = 1;
        }

    }

    return true;

}

char convert(char c, string key) {
    char replace;

    if (c >= 97 && c <= 122) {
        replace = tolower(key[c - 'a']);
        return replace;
    }else if (c >= 65 && c <= 90) {
        replace = toupper(key[c - 'A']);
        return replace;
    }else {

        return c;
    }
    return 0;


}

/*:( encrypts "A" as "Z" using ZYXWVUTSRQPONMLKJIHGFEDCBA as key
    expected "ciphertext: Z\...", not "ciphertext: Z\..."
:( encrypts "a" as "z" using ZYXWVUTSRQPONMLKJIHGFEDCBA as key
    expected "ciphertext: z\...", not "ciphertext: Z\..."
:( encrypts "ABC" as "NJQ" using NJQSUYBRXMOPFTHZVAWCGILKED as key
    expected "ciphertext: NJ...", not "ciphertext: NJ..."
:( encrypts "XyZ" as "KeD" using NJQSUYBRXMOPFTHZVAWCGILKED as key
    expected "ciphertext: Ke...", not "ciphertext: KE..."
:( encrypts "This is CS50" as "Cbah ah KH50" using YUKFRNLBAVMWZTEOGXHCIPJSQD as key
    expected "ciphertext: Cb...", not "ciphertext: CB..."
:( encrypts "This is CS50" as "Cbah ah KH50" using yukfrnlbavmwzteogxhcipjsqd as key
    expected "ciphertext: Cb...", not "ciphertext: cb..."
:( encrypts "This is CS50" as "Cbah ah KH50" using YUKFRNLBAVMWZteogxhcipjsqd as key
    expected "ciphertext: Cb...", not "ciphertext: cB..."
:( encrypts all alphabetic characters using DWUSXNPQKEGCZFJBTLYROHIAVM as key
    expected "ciphertext: Rq...", not "ciphertext: RQ..."
:( does not encrypt non-alphabetical characters using DWUSXNPQKEGCZFJBTLYROHIAVM as key
    expected "ciphertext: Yq...", not "ciphertext: YQ..."
*/
