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
