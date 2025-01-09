#include <cs50.h>
#include <stdio.h>

bool check_validity(long long ccn);
void check_brand(long long ccn);
int check_len(long long ccn);

int main(void)
{

    long long number;
    long long credit_number;

    do {
        credit_number = get_long_long("Type your credit card num: ");  //credit card number(input); Function 1

    } while (credit_number < 0);


    if(check_validity(credit_number)) {  // function 2
        check_brand(credit_number);  // function 3
    }else {
        //printf("%i\n", check_validity(credit_number));
        printf("INVALID\n");
    }


}

bool check_validity(long long ccn) {
    int digitByTwo = 0;
    int sum = 0;
    int len = check_len(ccn);

    if ((len == 15) || (len == 13) || (len == 16)) {

        for (int i = 0; ccn != 0; ccn /= 10, i++) {
        // When it's odd digit, we need to multiply it by 2. But if the value i
        //4003600000000014

            if ((i % 2) != 0) {
                digitByTwo = 2 * (ccn % 10);
                sum += digitByTwo/10 + digitByTwo%10;

            }else {
                sum += ccn % 10;
            }
        }
    }

    /*for (int i = 0; ccn != 0; ccn /= 10, i++) {
        // When it's odd digit, we need to multiply it by 2. But if the value i
        //4003600000000014
        //4
        if ((i % 2) != 0) {
            digitByTwo = 2 * (ccn % 10);
            sum += digitByTwo/10 + digitByTwo%10;

        }else {
            sum += ccn % 10;
        }
    }*/

    //printf("%i\n", sum);
    return (sum%10) == 0;
}

void check_brand(long long ccn) {
    if ((34e13 <= ccn && ccn < 35e13) || (37e13 <= ccn && ccn < 38e13) ) {
        printf("AMEX\n");
    }else if ((51e14 <= ccn && ccn < 56e14)) {
        printf("MASTERCARD\n");
    }else if ((4e12 <= ccn && ccn < 5e12) || (4e15 <= ccn && ccn< 5e15)) {
        printf("VISA\n");
    }else {
        printf("INVALID\n");
    }
}

int check_len(long long ccn) {
    int i;
    for (i = 0; ccn != 0; ccn /= 10, i++);

    return i;


}


/* :( identifies 4111111111111113 as INVALID
    expected "INVALID\n", not "VISA\n"
:( identifies 4222222222223 as INVALID
    expected "INVALID\n", not "VISA\n"
    현재 2가지의 에러
*/