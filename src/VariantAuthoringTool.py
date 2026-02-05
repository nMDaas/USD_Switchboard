class VariantAuthoringTool:
    """A simple class representing a dog."""
    # A class variable, shared by all instances
    species = "Canine"

    def __init__(self, name, age):
        """Initializes the name and age attributes."""
        # Instance variables, unique to each instance
        self.name = name
        self.age = age

    def bark(self):
        """Simulate a dog barking."""
        return f"{self.name} says woof!"

# Create two instances (objects) of the Dog class
dog1 = Dog("Buddy", 3)
dog2 = Dog("Lucy", 5)

# Access attributes of the objects
print(f"{dog1.name} is {dog1.age} years old.")
print(f"{dog2.name} is {dog2.age} years old.")

# Call a method on an object
print(dog1.bark())
print(dog2.bark())
