#include<stdio.h>
#include<unistd.h>

int main(int argc, char** argv) {
    sleep(10);
    fprintf(stdout, "\nbackground finished!\n");
    
    return 0;
}