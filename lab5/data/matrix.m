A = eye(3);
B = ones(3);
print "A";
print(A);
print "B";
print(B);
C = A .+ B;
print C;

D = zeros(3, 4);
D[0, 2] = 42;
% D[0][2] = 42;
% D[a:b, c:d] = 7;
% D[1:3, 2:4] = D[0, 1]; # opcjonalnie dla zainteresowanych
print "D";
print D;
print "D[2, 2]";
print D[2, 2];

E = -C;
F = E -C;
F = -D';

print "-D transpose";
print F;
print "-C";
print E;

G = [[1, 1, 2, 1], [2, 1, 2, 1], [2, 2, 1, 1]];
print "G matrix";
print G;
print "C matrix";
print C;
print "C * G matrix";
print C * G;
print "D double transpose";
print D'';