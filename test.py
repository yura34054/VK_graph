a = list(range(17))


def split_list(lst: list, n: int):
    
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


x = list(split_list(a, 5))

print(x)