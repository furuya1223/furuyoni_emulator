def generator(func):
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        try:
            print(next(gen))
            while True:
                print(gen.send(input()))
        except (StopIteration, RuntimeError):
            return
    return wrapper
