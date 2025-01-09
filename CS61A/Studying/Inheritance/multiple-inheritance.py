class Pet():
    sex = 'male'
    def __init__(self, name, owner):
        self.is_alive = True # It's alive!!!
        self.name = name
        self.owner = owner
    def eat(self, thing):
        print(self.name + " ate a " + str(thing) + "!")
    def talk(self):
        print(self.name)

class Dog(Pet):
    def talk(self):
        print(self.name + ' says woof!')


class Cat(Pet):

    def __init__(self, name, owner, lives=9):
        Pet.__init__(self, name, owner)
        self.lives = lives

    def __str__(self):
        return f'This is {self.name}!'
    def __repr__(self):
        return f'Cat({self.name}, {self.owner})'
    def talk(self):
        print(self.name + ' says Meow!')
        print(self)
        print(self.sex)




sf = lambda: 'sfsf'
p = Pet('Magic', 'Khoi')

b= Cat('Magic', 'Khoi')
print(repr(b))

print(sf())