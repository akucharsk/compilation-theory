

x = [ [1,2,3],
      [1,2,3,4,5],
      [1,2]
    ];

for i = 1:9 {
    for j =  3:8 {
        print i, j;
        break;
    }
    print i;
    print j;
    k = i;
    while (k > i) {
        if (k == 8) {
            a = 8;
            print a;
        }
        else if (k == 7) {
            b = 7;
            print b;
        }
        else {
            y = 5;
            print a, b;
            break;
        }
        print a;
        print x, y;
        break;
    }
}
print i;
break;
