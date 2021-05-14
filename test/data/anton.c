#include <stdio.h>

int main()
{
    long n, a, b, c, k, x; // c - производная, k - нужен для первого прохода цикла для производной
    scanf("%ld%ld%ld", &n, &x, &a);//считываем n, x, первый коэффициент
    k = n;
    c = 0;
    b = a;
    if (n == 0)
    {
        printf("%ld% 0", a);
        return 0;
    }
    while (n != 0)
    {
        if (n == 1) c = c + b;
        else
        {
            if (n == k) c = a*n*x;
            else c = (c + b*n)*x;
        }
        scanf("%ld", &b);
        a = x*a+b;
        n--;
    }
    printf("%ld %ld", a, c);
    return 0;
}
