class Animal:

    # attribute and method of the parent class
    name = ""
    
    def eat(self):
        print("I eat")

# inherit from Animal
class Dog(Animal):

    # new method in subclass
    def eat(self):
        super().eat()
        # access name attribute of superclass using self
        print("bones")

# create an object of the subclass
labrador = Dog()

# access superclass attribute and method 
labrador.name = "Rohu"
labrador.eat()

# call subclass method 
#labrador.display()

#To try NOTE
#vertical lay out container
#1st. make a widget class that has a blit funtion without implementation
#2nd. make a vertical layout container, which inherits from a widget, it has a function to add more widgets to it
#and it overrides blit funtion of the widget. In this blit funtion it calls blit functions of all the widgets inside of this container.
#3rd. in the add function, draw coordinates of the widget being added will have to be recalculated.
#4th. all widgets in the container layout will have to centered vertically and horizontaly. 
#about inheretance: https://www.programiz.com/python-programming/inheritance