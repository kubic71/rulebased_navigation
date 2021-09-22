from directions import all_directions, directions_map, rotate

def indent(text, indentation="  "):
    # prepend indentation to each line of the text
    return "\n".join(list(map(lambda line: indentation + line, text.split("\n"))))


class DbObject:
    """Wrapper for nice hierachical printing of the database objects"""

    def __str__(self):
        s = ""
        for attr in dir(self):
            if not attr.startswith("_"):
                attr_obj = self.__getattribute__(attr)
                if isinstance(attr_obj, DbObject):
                    attr_str = f"{attr}:\n"
                    attr_str += indent(str(attr_obj))
                    attr_str += "\n"

                    s += attr_str

        return s
    
    def __repr__(self):
        return self.__str__()


class List(DbObject):
    def __init__(self, l: list):
        self._l = l
    
    def __str__(self):
        if len(self._l) == 0:
            return "[]"
        elif len(self._l) == 1:
            return "[\n  " + str(self._l[0]) + ",\n]"

        
        element_strings = []
        for el in self._l:
            element_strings.append(str(el))
        
        return "[\n" + indent(",\n".join(element_strings)) + "\n]"
    
    def __getattr__(self, attr):
        print(attr)
        if attr != "__str__":
            return getattr(self._l, attr)


class Vector(DbObject):
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    @classmethod
    def from_tuple(cls, vector_tuple):
        return Vector(vector_tuple[0], vector_tuple[1])
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, b):
        return Vector(self.x + b.x, self.y + b.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def rotate(self, clockwise=True):
        return Vector.from_tuple(rotate((self.x, self.y), clockwise=clockwise))
    
    def to_arrow(self):
        # only for 8 directions
        return directions_map[self.to_tuple()]
    
    def to_tuple(self):
        return (self.x, self.y)
    

class SonarSensor(DbObject):
    # SonarSensor DbObject is implicitly added to the database in Maze constructor
    def __init__(self, left, forward, right):
        # sonar callbacks injected by Maze
        self._left = left
        self._forward = forward
        self._right = right

    @property
    def left(self):
        return self._left()

    @property
    def forward(self):
        return self._forward()

    @property
    def right(self):
        return self._right()
    
    def __str__(self):
        return f"left: {self.left}\nforward:  {self.forward}\nright:  {self.right}"



class Database(DbObject):
    def __init__(self, init_position: Vector, orientation: Vector, goal: Vector):
        self.position = init_position
        self.orientation = orientation
        self.goal = goal

        # set of all database objects
        self.db = set()
    

if __name__ == "__main__":
    db = Database(Vector(1, 2), Vector(0, 1), Vector(20, 19))
    db.some_list = List([1,2,List([10, 11, 123]),4, [], 5])
    print(db)

    v = Vector(0, 1)
    for i in range(10):
        print(v, v.to_arrow())
        v = v.rotate(clockwise=True)

    print("-----------")
    for i in range(10):
        print(v, v.to_arrow())
        v = v.rotate(clockwise=False)