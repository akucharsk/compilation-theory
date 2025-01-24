pi = 0.0;
n = 1;
for i = 1:100000 {
    a = n - 4.0;
    b = n + 2;
    pi += 4.0 / a / b;
    n += 4;
}
print pi;
