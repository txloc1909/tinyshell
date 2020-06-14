#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

#define clrscr() printf("\e[1;1H\e[2J")

int main(int argc, char** argv) {
    int i;

    for(i = 0; i < 10; i++) {
        printf("%d\n", i);
        sleep(3);
        //clrscr();
    }
    
    return 0;
}
