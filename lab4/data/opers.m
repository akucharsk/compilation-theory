
x = 0;
y = zeros(5);
z = x + y;

x = eye(5);
y = eye(8);
z = x + y;

x = [ 1,2,3,4,5 ];
y = [ [1,2,3,4,5],
      [1,2,3,4,5] ];
z = x + y;

x = [ 1,2,3,4,5 ];
y = [1,2,3,4,5,6];
z = x + y;

x = zeros(5);
y = zeros(5,7);
z = x + y;

x = ones(3,5);
z = x[7,10];
v = x[2,3,4];

x = zeros(6, 7);
y = ones(7, 5);
z = x * y;

x = zeros(3, 5);
y = eye(3);
z = x * y;

a = eye(3, 3);