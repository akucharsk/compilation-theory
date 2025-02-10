pi = 0.0;
sgn = 1;
for i = 1:100000 {
    pi += sgn * 4.0 / (2 * i - 1);
    sgn *= -1;
}
print pi;
