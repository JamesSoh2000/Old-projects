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
// 2022/5/28 내가 오늘 테스트한 결과 hash table 의 크기를 늘려 넣을수 있는 곳을 더 여러개 만든다면 링크리스트를 이용했을 때 head가 커지지 않게 할수있음
// 현재 이 방법은 Hash table을 이용한 방법인데 Trie를 이용하면 속도면에선 훨씬 빠름
// N의 크기를 26에서 내가 임의로 100000로 바꿈.
// 추가로 hash function을 구글에서 빠른 hash function을 하나 찾아내어 그것으로 대체함. 아래 링크
// https://cs50.stackexchange.com/questions/19705/how-to-make-the-check-function-faster

const long long N = 100000;

// Hash table
node *table[N];

// Declare variables
unsigned int word_count = 0;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    hash_value = hash(word);
    node *head = table[hash_value];

    while (head != 0) {
        if (strcasecmp(head->word, word) == 0) {
            return true;
        }else {
            head = head->next;
        }

    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int hash = 0;
    for (int i=0, n=strlen(word); i<n; i++) {
        hash = (hash << 2) ^ word[i];
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
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
        hash_value = hash(n->word);
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
    if (word_count > 0) {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++) {
        node *head = table[i];
        node *temp = head;

        while (head != NULL) {
            temp = temp->next;
            free(head);
            head = temp;
        }

    }
    return true;
}
