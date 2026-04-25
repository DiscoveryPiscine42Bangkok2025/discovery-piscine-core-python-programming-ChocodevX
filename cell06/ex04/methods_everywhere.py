import sys

if len(sys.argv) == 1:
    print("none")
    sys.exit()

for word in sys.argv[1:]:
    if len(word) < 8:
        print(word + "z" * (8 - len(word)))
    elif len(word) > 8:
        length = len(word) - 8
        print(word[:-length])