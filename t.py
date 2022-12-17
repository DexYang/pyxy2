#!/usr/bin/env python
class A:
    def __init__(self) -> None:
        self.n = 0


    def g(self):
        self.n += 1
        return type(self)()


a = A()


b = a.g()

print(a.n)
print(b.n)