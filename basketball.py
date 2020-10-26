n = int(input())

#TODO score of shoots
p1 = 1
p2 = 3
p3 = 5

#sum of succes shoots
sp1 = p1 + p2
sp2 = p1 + p3
sp3 = p2 + p3
sp4 = p1 + p2 + p3

#conditions
if (n == sp1):
    p1 = str('Yes')
    p2 = str('Yes')
    p3 = str('No')
elif (n == p1):
    p1 = str('Yes')
    p2 = str('No')
    p3 = str('No')

elif (n == sp2):
    p1 = str('Yes')
    p2 = str('No')
    p3 = str('Yes')
elif (n == p2):
    p1 = str('No')
    p2 = str('Yes')
    p3 = str('No')

elif (n == sp3):
    p1 = str('No')
    p2 = str('Yes')
    p3 = str('Yes')
elif (n == p3):
    p1 = str('No')
    p2 = str('No')
    p3 = str('Yes')

elif (n == sp4):
    p1 = str('Yes')
    p2 = str('Yes')
    p3 = str('Yes')
else:
    p1 = str('No')
    p2 = str('No')
    p3 = str('No')



print(p1)
print(p2)
print(p3)