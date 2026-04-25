import sys

if len(sys.argv) == 1:
    print("nope")
    sys.exit()

for word in sys.argv[1:]:
    if 'ism' not in word:
        print(word + "ism")