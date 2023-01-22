class Func:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        return self.f(*args)

    def __mul__(self, g):
        def composite(*args):
            r = g(*args)
            r = r if isinstance(r, tuple) else [r]
            return self.f(*r)
        return Func(composite)

    def __composite(self, g):
        def operate(*args):
            return g(self.f(*args))
        return operate
