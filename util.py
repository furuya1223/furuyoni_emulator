def generator(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        try:
            print(next(gen))
            gen.send(input())
        except StopIteration:
            return
    return wrapper
