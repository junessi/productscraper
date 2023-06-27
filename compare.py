import sys

filename_a = sys.argv[1]
filename_b = sys.argv[2]
lines_a = set()
lines_b = set()

with open(filename_a, 'r') as fa, open(filename_b, 'r') as fb:
    for l in fa.readlines():
        lines_a.add(l)

    for l in fb.readlines():
        try:
            lines_a.remove(l)
        except:
            lines_b.add(l)

i = 0
print('lines in a:')
for l in lines_a:
    print(l)
    i += 1
    if i == 10:
        break

i = 0
print('lines in b:')
for l in lines_b:
    print(l)
    i += 1
    if i == 10:
        break

