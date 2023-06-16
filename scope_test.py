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
window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))

w, h = pygame.display.get_surface().get_size()


white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 36)

class Widget():

    def __init__(self):
        self.x = 0
        self.y = 0

    def get_width(self):
        return 0
    
    def get_height(self):
        return 0
    
    def set_pos(self, x, y):
        pass

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def blit(self, window):
        print("aaaa")

class TextWidget(Widget):
    
    def __init__(self, text):
        super().__init__() #NOTE What is dinamic constructor?
        self.text_widget = font.render(text, True, black)

    def blit(self, window):
        window.blit(self.text_widget, (self.x,self.y))
    
    def get_width(self):
        dimention = self.text_widget.get_size()
        return dimention[0] 
    
    def get_height(self):
        dimention = self.text_widget.get_size()
        return dimention[1]

class BitmapWidget(Widget):

    def __init__(self, image):
        super().__init__()
        self.image = image
    
    def blit(self, window):
        print("bbb")


class VerticalLayoutContainer(Widget):

    def __init__(self, window, window_width, window_height):
        super().__init__()
        self.widgets = []
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.vertical_position_for_next_widged = 0
        self.full_height_of_desired_widgets_list = 0

    def add_widget(self, widget):
        self.widget_horizontal_aligment(widget.get_width())
        self.widget_vertical_aligment(widget.get_height())
        self.aligned_widget_coord = (self.widget_position_x,self.widget_position_y)
        widget.set_pos(self.aligned_widget_coord[0], self.aligned_widget_coord[1])
        self.vertical_position_for_next_widged = self.vertical_position_for_next_widged + widget.get_height()
        self.widgets.append(widget)

        self.vertical_aligning_of_desired_widgets_list()
        for w in self.widgets:
            w.set_pos(w.x, self.full_height_of_desired_widgets_list)
            self.full_height_of_desired_widgets_list = self.full_height_of_desired_widgets_list + w.get_height() + 10#empty_space
        self.full_height_of_desired_widgets_list = 0 

    def widget_horizontal_aligment(self, widget_width):
        self.widget_position_x = ((self.window_width - widget_width)//2)
    
    def widget_vertical_aligment(self, widget_height):
        self.widget_position_y = (((self.window_height - widget_height)//2) + self.vertical_position_for_next_widged)
    
    def vertical_aligning_of_desired_widgets_list(self):
        self.full_height_of_desired_widgets_list = ((self.window_height - self.vertical_position_for_next_widged)//2)
    
    def blit(self, window):
        #self.vertical_aligning_of_desired_widgets_list()
        for w in self.widgets:
            w.blit(window)#, self.full_height_of_desired_widgets_list)
            #self.full_height_of_desired_widgets_list = self.full_height_of_desired_widgets_list + w.get_height() + empty_space
        #self.full_height_of_desired_widgets_list = 0
        #self.vertical_position_for_next_widged = 0

class HorizontalLayoutContainer(Widget):

    def __init__(self, window, window_width, window_height):
        super().__init__()
        self.widgets = []
        self.window = window
        self.window_width = window_height
        self.window_height = window_width
        self.vertical_position_for_next_widged = 0
        self.full_height_of_desired_widgets_list = 0

    def add_widget(self, widget):
        self.widget_horizontal_aligment(widget.get_height())
        self.widget_vertical_aligment(widget.get_width())
        self.aligned_widget_coord = (self.widget_position_x,self.widget_position_y)
        widget.set_pos(self.aligned_widget_coord[1], self.aligned_widget_coord[0])
        self.vertical_position_for_next_widged = self.vertical_position_for_next_widged + widget.get_width()
        self.widgets.append(widget)

        self.vertical_aligning_of_desired_widgets_list()
        for w in self.widgets:
            w.set_pos(self.full_height_of_desired_widgets_list, w.y)
            self.full_height_of_desired_widgets_list = self.full_height_of_desired_widgets_list + w.get_width() + 10#empty_space
        self.full_height_of_desired_widgets_list = 0 

    def widget_horizontal_aligment(self, widget_width):
        self.widget_position_x = ((self.window_width - widget_width)//2)
    
    def widget_vertical_aligment(self, widget_height):
        self.widget_position_y = (((self.window_height - widget_height)//2) + self.vertical_position_for_next_widged)
    
    def vertical_aligning_of_desired_widgets_list(self):
        self.full_height_of_desired_widgets_list = ((self.window_height - self.vertical_position_for_next_widged)//2)
    
    def blit(self, window):
        #self.vertical_aligning_of_desired_widgets_list()
        for w in self.widgets:
            w.blit(window)#, self.full_height_of_desired_widgets_list)
            #self.full_height_of_desired_widgets_list = self.full_height_of_desired_widgets_list + w.get_height() + empty_space
        #self.full_height_of_desired_widgets_list = 0
        #self.vertical_position_for_next_widged = 0

# class HorizontalLayoutContainer(Widget):
    
#     def __init__(self, window, window_width, window_height):
#         self.widgets = []
#         self.window = window
#         self.window_width = window_width
#         self.window_height = window_height
#         self.horizontal_position_for_next_widged = 0
#         self.full_width_of_desired_widgets_list = 0

#     def add_widget(self, widget):
#         self.widget_horizontal_aligment(widget.get_width())
#         self.widget_vertical_aligment(widget.get_height())
#         self.aligned_widget_coord = (self.widget_position_x,self.widget_position_y)
#         widget.set_pos(self.aligned_widget_coord[0], self.aligned_widget_coord[1])
#         self.horizontal_position_for_next_widged = self.horizontal_position_for_next_widged + widget.get_width()
#         self.widgets.append(widget)

#         self.horizontal_aligning_of_desired_widgets_list()
#         for w in self.widgets:
#             w.set_pos(self.full_width_of_desired_widgets_list, w.y)
#             self.full_width_of_desired_widgets_list = self.full_width_of_desired_widgets_list + w.get_width() + 10#empty_space
#         self.full_width_of_desired_widgets_list = 0

#     def widget_horizontal_aligment(self, widget_width):
#         self.widget_position_x = (((self.window_width - widget_width)//2) + self.horizontal_position_for_next_widged)
    
#     def widget_vertical_aligment(self, widget_height):
#         self.widget_position_y = ((self.window_height - widget_height)//2)
    
#     def horizontal_aligning_of_desired_widgets_list(self):
#         self.full_width_of_desired_widgets_list = ((self.window_width - self.horizontal_position_for_next_widged)//2)

#     def blit(self, window):
#         for w in self.widgets:
#             w.blit(window)

vlc = VerticalLayoutContainer(window, window_width, window_height)

tx0 = TextWidget("Hello World")
tx1 = TextWidget("Random Number Generator")
tx2 = TextWidget("Hello World")
tx3 = TextWidget("Hello World")
tx4 = TextWidget("Hello World")
tx5 = TextWidget("Hello World")
tx6 = TextWidget("Hello World")

vlc.add_widget(tx0)
vlc.add_widget(tx1)
vlc.add_widget(tx2)
vlc.add_widget(tx3)
vlc.add_widget(tx4)
vlc.add_widget(tx5)
vlc.add_widget(tx6)

vlc2 = VerticalLayoutContainer(window, window_width, window_height)
tc1 = TextWidget("Hello World")
vlc2.add_widget(tc1)

hlc1 = HorizontalLayoutContainer(window, window_width, window_height)
hlc1.add_widget(TextWidget("a"))
hlc1.add_widget(TextWidget("b"))
hlc1.add_widget(vlc)
#hlc1.add_widget(vlc2)
#NOTE Inheretance, method overwriting
#NOTE Parent class is synonim for super class and a synonim for base class (all of these terms are qual)

vlc.add_widget(BitmapWidget(pygame.image.load('assets/painted/transparent/orc_4.png')))


line = font.render("____________________________________________________", True, black)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        window.fill(white)
        #vlc.blit(window)
        hlc1.blit(window)
        window.blit(line, (0,0))
        window.blit(line, (0,470))

    # Update the window
    pygame.display.flip()

# Quit Pygame
pygame.quit()

