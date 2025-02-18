#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool has_cycle(int winner, int loser);
bool has_cycle_recursive(int winner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {

                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }
    //printf ("Bro we are here:");

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; candidate_count > i; i++) {

        if (strcmp(candidates[i], name) == 0) {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    int count = 0;
    for (int i = 0; candidate_count > i; i++) {
        for (int j = i+1; candidate_count > j; j++) {
            preferences[ranks[i]][ranks[j]]++;
        }



    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    // We have Bob Char Alice
    // preferences[0][1] 이뜻은 Bob over Char (bob이 이김)
    // We will have 3 cases of preferences[i][j] this time(We can only have 3 pairs as maximum)
    for (int i = 0; candidate_count > i; i++) {
        for (int j = i+1; candidate_count > j; j++) {
            int candidate_i = preferences[i][j];
            int candidate_j = preferences[j][i];

            if (candidate_i != candidate_j) {
                pair p;
                if (candidate_i > candidate_j) {

                    p.winner = i;
                    p.loser = j;
                }else {

                    p.winner = j;
                    p.loser = i;
                }
                pairs[pair_count++] = p;
            }

        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    int empty[pair_count];
    for (int i = 0; pair_count > i; i++) {
        int w = pairs[i].winner;
        int l = pairs[i].loser;
        empty[i] = preferences[w][l];
    }

    int current = 0;
    int max = 0;
    pair current2;

    for (int i = 0; pair_count >i; i++) {
        current = i;
        max = i;
        for (int j = i+1; pair_count > j; j++) {
            if (empty[max] < empty[j]) {
                max = j;
            }
        }
        if (max != i) {
            current = empty[i];
            empty[i] = empty[max];
            empty[max] = current;

            current2 = pairs[i];
            pairs[i] = pairs[max];
            pairs[max] = current2;
        }
        printf("This is array: %i\n", empty[i]);
    }


    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++) {
        if (!has_cycle_recursive(pairs[i].winner, pairs[i].loser)) {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{

    for (int i = 0; MAX > i; i++) {
        int winner = 0;
        for (int j = 0; MAX > j; j++) {
            if (locked[i][j]) {
                winner = 1;
            }
            if (locked[j][i]) {
                winner = 0;
                break;
            }

        }
        if (winner == 1) {
            printf("%s\n", candidates[i]);
            return;
        }

    }
    return;
}

bool has_cycle(int winner, int loser) {
     while (winner != -1 && winner != loser) {
         bool found = false;

         for (int i = 0; i < candidate_count; i++) {
             if (locked[i][winner]) {
                 found = true;
                 winner = i;
             }
         }

         if (!found) {
             winner = -1;
         }
     }

     if (winner == loser) {
         return true;
     }
     return false;
}

bool has_cycle_recursive(int winner, int loser) {
    if (winner == loser) {
        return true;
    }

    for (int i = 0; i < candidate_count; i++) {
        if (locked[i][winner]) {
            return has_cycle_recursive(i, loser);
        }
    }
    return false;
}