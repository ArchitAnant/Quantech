#Write me code of how to add two numbers usign classes

class Add:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b
    
a = Add(2, 3)

print(a.add())

#Write me code of how to add two numbers usign functions

def add(a, b):
    