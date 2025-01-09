// Implements a dictionary's functionality
// 먼저 시작하기에 앞선 이해! 이 문제는 ./speller dictionaries/small texts/cat.txt 이런 커맨드를 썻을 때 내가 미스스펠한 용어는 총 "A, is, not, a" 이렇게 4개가 나올건데 이렇게 나오는 이유는
// 내가 dictionaries/small 에 저장한 단어가 cat과 cata~ 뭔가로 시작하는 두 단어 밖에 없기 때문에 이런 결과가 나옴. 즉 딕셔너리에 있는 단어가 텍스트에 없으면 미스스펠한 단어들로 판단함.
#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Adding my own variables + unsigned int의 뜻이란 항상 positive인 숫자를 말함, 절대 negative가 될수없음.
unsigned int hash_value;
unsigned int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Loop through each line of the dictionary, and check if the word(string) is in dictionary. Lowercase, uppercase isn't matter it's all same.
    // However, u need to check that if foo is in dictionary, then check should return true given any capitalization thereof;
    // none of foo, foO, fOo, fOO, fOO, Foo, FoO, FOo, and FOO should be considered misspelled.
    // Also, even if foo is in dictionary, check should return false given foo's if foo's is not also in dictionary. 이뜻은 스페이스바로 구분해야함.

    unsigned int value;
    value = hash(word);

    node *n = table[value];


    // 0의미는 null이란 뜻임.

    while (n != 0) {
        if (strcasecmp(n->word, word) == 0) {
            return true;
        }else {
            n = n->next;
        }

    }


    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int sum = 0;
    int result = 0;
    for (int i = 0; strlen(word) > i; i++) {
        sum += toupper(word[i]);
    }
    result = sum % N;
    return result;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");

    if (file == NULL) {
        printf("Unable to open the file");
        return false;
    }

    char word[LENGTH+1];
    while (fscanf(file, "%s", word) != EOF) {
        node *n = malloc(sizeof(node));

        if (n == NULL) {
            return false;
        }

        strcpy(n->word, word);
        hash_value = hash(word);
        n->next = table[hash_value];
        table[hash_value] = n;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0) {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++) {

        node *head = table[i];
        node *cursor = head;




        while (cursor != NULL) {
            cursor = cursor->next;
            free(head);
            head = cursor;

        }
    }
    return true;
}
