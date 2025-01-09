#include <stdio.h>

void check_brand(long long ccn);

int main(void) {
    check_brand(4003600000000014);
}

void check_brand(long long ccn) {
    if ((34e13 <= ccn && ccn < 35e18)) {
        printf("%lli\n", ccn);
    }else {
        printf("invalid\n");
    }
}