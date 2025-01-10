A = eye(3);
B = ones(3);
print(A);
print(B);
C = A .+ B;
print C;

D = zeros(3, 4);
D[0, 2, 3] = 42;
% D[0][2] = 42;
D[a:b, c:d] = 7;
D[1:3, 2:4] = D[0, 1]; % opcjonalnie dla zainteresowanych
print D;
print D[2, 2];

E = -C;
F = E -C;
F = -D';

print F;
print E;
