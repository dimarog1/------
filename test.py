from sys import stdin

a = [i.strip() for i in stdin]

for i in a:
    print(f'{i.split(" = ")[1]} = {i.split(" = ")[0]}')
