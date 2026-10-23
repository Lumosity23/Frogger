from math import cos, hypot, sin


class Vector2:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    @property
    def xy(self) -> tuple[float, float]:
        """Returns the vector as a tuple"""
        return (self.x, self.y)

    @xy.setter
    def xy(self, value: tuple[float, float]):
        """Unpack from a tuple"""
        self.x, self.y = value

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> Vector2:
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: float) -> Vector2:
        return Vector2(self.x / other, self.y / other)

    def length(self) -> float:
        """Returns the length of the vector"""
        return hypot(self.x, self.y)

    def distance_to(self, vector: Vector2) -> float:
        """Returns the distance to another vector"""
        return (vector - self).length()

    def normalize(self):
        """Returns the normalized vector"""
        return self / self.length()

    def rotate(self, theta: float):
        """Rotate the vector with a angle"""
        x, y = self.xy
        self.x = x * cos(theta) - y * sin(theta)
        self.y = x * sin(theta) + y * cos(theta)

    def pos_for_screen(self, screen_size: tuple[int, int]) -> tuple[float, float]:
        """Return the position absolute for the screen"""
        return self.x + screen_size[0] / 2, self.y + screen_size[1] / 2
