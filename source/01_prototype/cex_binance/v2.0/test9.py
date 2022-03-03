a = ["1one", "2two", "3three", "4four", "5five", "6six"]
b = []
for i in range(len(a)):

    if ("4" in a[i]) is True:

        b.append(i)

print(b)
print(a[5].replace("six", "9"))