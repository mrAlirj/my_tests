string = input('')

for i in range(len(string)):
    l = string[i]
    for j in range(i):
        a = string[j]
        # a = string.replace(string[j],string[i])
        print(j)
