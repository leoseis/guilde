
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"



result = Animal('Jack')
breed = Dog("Cain")

print(result.name)
print(result.speak())
breed.speak()