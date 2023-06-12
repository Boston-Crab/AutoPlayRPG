# class Animal:

#     # attribute and method of the parent class
#     name = ""
    
#     def eat(self):
#         print("I eat")

# # inherit from Animal
# class Dog(Animal):

#     # new method in subclass
#     def eat(self):
#         super().eat()
#         # access name attribute of superclass using self
#         print("bones")

# # create an object of the subclass
# labrador = Dog()

# # access superclass attribute and method 
# labrador.name = "Rohu"
# labrador.eat()

# call subclass method 
#labrador.display()

#To try NOTE
#vertical lay out container
#1st. make a widget class that has a blit funtion without implementation
#2nd. make a vertical layout container, which inherits from a widget, it has a function to add more widgets to it
#and it overrides blit function of the widget. In this blit funtion it calls blit functions of all the widgets inside of this container.
#3rd. in the add function, draw coordinates of the widget being added will have to be recalculated.
#4th. all widgets in the container layout will have to centered vertically and horizontaly. 
#about inheretance: https://www.programiz.com/python-programming/inheritance


import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_x = 500
window_y = 500
window = pygame.display.set_mode((window_x, window_y))

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 36)


text_surface = font.render("Hello, World!", True, black)
text_size = text_surface.get_size()

# Set the position to blit the text
text_position = (((window_x - text_size[0])//2), 100)

class Widget():

    def widget_blit():
        print("aaaa")

class VerticalLayoutContainer:

    def __init__(self, window, window_x, window_y):
        self.widgets = []
        self.window = window
        self.window_x = window_x
        self.window_y = window_y
        self.y_distance_between_widgets = 0

    def create_and_add_widget(self, text):
        widget = font.render(text, True, black)
        text_size = widget.get_size()
        print(text_size)
        self.aligning_widgets(self.window_x, self.window_y, text_size[0], text_size[1])
        ready_widget = [widget, self.aligned_widget_coord]
        self.widgets.append(ready_widget)

    def widget_horizontal_aligment(self, window_x, text_x):
        self.widget_position_x = ((window_x - text_x)//2)
    
    def widget_vertical_aligment(self, window_y, text_y):
        self.widget_position_y = (((window_y - text_y)//2) + self.y_distance_between_widgets)
        self.y_distance_between_widgets = self.y_distance_between_widgets + 30

    def aligning_widgets(self, window_x, window_y, text_x, text_y):
        self.widget_horizontal_aligment(window_x, text_x)
        self.widget_vertical_aligment(window_y, text_y)
        self.aligned_widget_coord = (self.widget_position_x,self.widget_position_y)
    
    def widgets_blit(self):
        for i in self.widgets:
            self.window.blit(i[0],i[1])

vlc = VerticalLayoutContainer(window, window_x, window_y)
vlc.create_and_add_widget("Hello World")
vlc.create_and_add_widget("Lobby")
vlc.create_and_add_widget("Random Number Generator")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        window.fill(white)
        vlc.widgets_blit()

    # Update the window
    pygame.display.flip()

# Quit Pygame
pygame.quit()