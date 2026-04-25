import sys

count = "".join(sys.argv[1:]).count('z')

if count > 0:
    print('z' * count)
else:
    print("none")