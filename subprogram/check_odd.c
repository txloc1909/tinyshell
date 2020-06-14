#include<stdio.h>
#include<math.h>

int is_odd(int n) {
    return n % 2;
}

int main() {
    int n;
    printf("Nhap n: ");
    scanf("%d", &n);
    if (is_odd(n))
        printf("%d is odd\n", n);
    else
        printf("%d is even\n", n);
    
    return 0;
}