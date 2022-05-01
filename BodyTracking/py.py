a = 11
def foo(x):
    print(x())
def bar():
    a = 44
    def z():
        return (a + 1)
    foo(z)
bar()