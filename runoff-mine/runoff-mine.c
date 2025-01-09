#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;
int test;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    test = candidate_count;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();

        if (won)
        {


            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);
        printf("The min value is: %i\n", min);
        // If tie, everyone wins
        if (tie)
        {

            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid
bool vote(int voter, int rank, string name)
{
    // voter, 랭크 , 입후보
    // in candidate[]. Let's assume we have "A","B","C" in order.

    int same = 0;

    for (int i = 0; candidate_count > i; i++) {
        if ((strcmp(name, candidates[i].name)) == 0 && same == 0) {
            same ++;
            preferences[voter][rank] = i;
            //candidates[i].votes += rank;
            return true;
        }
    }

    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // TODO
    // loop through each voters
    // find the RANK 1 candidate each voter choose
    // update the candidate's vote up! When u do it, check the candidate is whether eliminated or not.
    //

    for (int i  = 0; voter_count > i; i++) {
        int count = 0;
        while (candidates[preferences[i][count]].eliminated) {          // 5/5 2:49 기준 while 을 if로 바꿔보았음(원래 로직이면 와일이 맞는데 실험차)
            count++;
            // 새로운 수정!(틀릴수도있음 예의주시)
        }
        candidates[preferences[i][count]].votes += 1;
    }

    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // TODO

    for (int i = 0; candidate_count > i; i++) {
        if (voter_count/2 < candidates[i].votes) {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    // TODO
    // We can use mergesort for this, and just take the smallest num after sorting.
    // But i will just use linear search because it's only 9 candidates as maximum.
    // 3  2 1 5 -- 2 3 1 5 --
    int smallest = 0;
    int current = 0;
    int empty[candidate_count];
    int temp = 0;
    int temp1 = 0;
    int count = 0;
    int return_value = 0;

    // looping through each candidate's votes and record them into the empty array. When we see candidates who are eliminated, store them as -1.
    for (int i = 0; candidate_count > i; i++) {
        if (candidates[i].eliminated == false) {
            empty[i] = candidates[i].votes;
        }else if (candidates[i].eliminated) {
            empty[i] = -1;
        }

    }

    // Use Selection Sort to sort the array of each candidate's votes.
    for (int i = 0; candidate_count > i; i++) {
        smallest = i;
        for (int j = i; candidate_count > j ; j++) {
            if (empty[smallest] > empty[j]) {
                temp = smallest; // which is 0index
                current = temp;
                smallest = j; // which is 6th index

            }
        }
        if (i != smallest) {
            temp1 = empty[i];
            empty[i] = empty[smallest];

        }
        printf("The Array value: %i\n", empty[i]);
    }

    for (int i = 0; candidate_count > i; i++) {
        if (empty[i] > 0) {
            return empty[i];
        }
    }
    return empty[0];
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    // TODO
    int count = 0;
    for (int i = 0; candidate_count > i; i++) {
        if (candidates[i].votes > min && (candidates[i].eliminated == false)) {
            return false;
        }else {
            count++;
        }
    }

    int count2 = 1;
    // 5/4 20시 현재 여기서 새로 고치고있는중 --> 내가 보기엔 만약 표가 전부 같다면 다음 preference 를 고려해보아야함) ++ 5/5 현재 아래것을 debugging 중 (계속 같은 에러 ㅠㅠ)
    //if 표 개수가 같은 상황

    if (count == candidate_count) {
        // Right now, it's not passing here!

        for (int i = 1; candidate_count > i; i++) {
            //candidates[preferences[i][count]]
            for (int j = 0; voter_count > j; j++) {
                if (candidates[preferences[j][i]].eliminated == false) {
                    candidates[preferences[j][i]].votes += 1;
                }

            }

            for (int k = 0; candidate_count > k; k++) {
                if (candidates[k].eliminated == false) {
                    for (int j = k + 1; candidate_count > j; j++) {
                        if (candidates[k].votes != candidates[j].votes && candidates[j].eliminated == false) {

                            return false;
                        }
                    }
                }
            }



        }


        
    }



    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    // TODO

    for (int i = 0; candidate_count > i; i++) {
        if (candidates[i].votes == min) {
            candidates[i].eliminated = true;
        }
    }



    return;
}