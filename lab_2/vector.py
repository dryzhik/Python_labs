from math import sqrt


class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        add_res_x = self.x + other.x
        add_res_y = self.y + other.y
        return Vector(add_res_x, add_res_y)

    def __sub__(self, other):
        sub_res_x = self.x - other.x
        sub_res_y = self.y - other.y
        return Vector(sub_res_x, sub_res_y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return not (self.__eq__(other))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            mul_res_x = self.x * other
            mul_res_y = self.y * other
            return Vector(mul_res_x, mul_res_y)
        elif isinstance(other, Vector):
            scalar_mul_res = self.x * other.x + self.y + other.y
            return scalar_mul_res
        else:
            raise ValueError("Unknown type of multiplier")

    def __rmul__(self, other):
        rmul_res_x = self.x * other
        rmul_res_y = self.y * other
        return Vector(rmul_res_x, rmul_res_y)

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __str__(self):
        return "<{}; {}>".format(self.x, self.y)

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    vec1 = Vector(1, 2)
    vec2 = Vector(3, 4)
    print(vec1)
    print(vec2)
    print("Сложение: " + str(vec1 + vec2))
    print("Вычитание: " + str(vec2 - vec1))
    print("Сравнение (равно): " + str(vec1 == vec2))
    print("Сравнение (не равно): " + str(vec1 != vec2))
    print("Умножение на число справа: " + str(vec1 * 10))
    print("Умножение на число слева: " + str(10.0 * vec1))
    print("Скалярное произведение: " + str(vec1 * vec2))
    print("Длина (модуль) вектора: " + str(abs(vec2)))
