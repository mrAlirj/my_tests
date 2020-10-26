n = list(map(int ,input().split()))
i = (n[0])
j = (n[1])

for row in range(i*3):#0,1
    if i <= row < 2*i:
        for col in range(j*3):#0,1,2
            if j <= col < 2*j:
                print('X' , end='')
            else:
                print('.', end='')
    else:
        for col in range(j*3):#0,1,2
            if j <= col < 2*j:
                print('.' , end='')
            else:
                print('X', end='')

    print()