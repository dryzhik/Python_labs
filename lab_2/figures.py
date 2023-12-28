from abc import ABC, abstractmethod
from math import sqrt, pi


class Figure(ABC):
    _type = "Figure"

    def type(self):
        return self._type

    @abstractmethod
    def square(self):
        pass


class Triangle(Figure):

    def __init__(self, side1, side2, side3):
        self._type = "Triangle"
        
        if side1 < 0 or side2 < 0 or side3 < 0:
            raise Exception("Sides must be positive")
        if (side1 + side2) < side3 or (side2 + side3) < side1 or (side1 + side3) < side2:
            raise Exception("Such triangle doesn't exist")

        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        super().__init__()

    def square(self):
        p = (self.side1 + self.side2 + self.side3) * 0.5
        s = sqrt(p * (p - self.side1) * (p - self.side2) * (p - self.side3))
        return s


class Rectangle(Figure):

    def __init__(self, height, width):
        self._type = "Rectangle"
        
        if height < 0 or width < 0:
            raise Exception("Sides must be positive")

        self.height = height
        self.width = width
        super().__init__()

    def square(self):
        s = self.width * self.width
        return s


class Circle(Figure):

    def __init__(self, radius):
        self._type = "Circle"
        
        if radius < 0:
            raise Exception("Radius must be positive")

        self.radius = radius
        super().__init__()

    def square(self):
        s = pi * self.radius ** 2
        return s


if __name__ == "__main__":
    rectangle = Rectangle(1, 2)
    print(rectangle.type())
    print("Площадь: " + str(rectangle.square()))
    print("--------------------------------------")
    triangle = Triangle(3, 4, 5)
    print(triangle.type())
    print("Площадь: " + str(triangle.square()))
    print("--------------------------------------")
    circle = Circle(6)
    print(circle.type())
    print("Площадь: " + str(circle.square()))
