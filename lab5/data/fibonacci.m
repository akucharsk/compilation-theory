% a = 0;
% b = 1;
% while (b < 1000) {
%     print b;
%     b += a;
%     a = b - a;
% }

% for i = 0:5 print i;

n = 2;
m = 3;

A = ones(n, m);
B = [[12, 15, 18], [12, 15, 18]];

print A;
print B;

C = B / A;

print C;