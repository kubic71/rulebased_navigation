from directions import all_directions, directions_map, rotate
from collections import defaultdict

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

# Database List wrapper for pretty printing
class List(DbObject):
    def __init__(self, l: list):
        self._l = l
    
    def __str__(self):
        if len(self._l) == 0:
            return "[]"
        
        element_strings = []
        for el in self._l:
            element_strings.append(str(el))
        
        return "[\n" + indent(",\n".join(element_strings)) + "\n]"
    
    def __getattr__(self, attr):
        return getattr(self._l, attr)


# Database Dict wrapper for pretty printing
class Dict(DbObject):
    def __init__(self, d: dict):
        self._d = d


    
    def __str__(self):
        if len(self._d) == 0:
            return "{}"

        element_strings = []
        for key in self._d:
            element_strings.append(f"{key}: {self._d[key]}")
        
        return "{\n" + indent(",\n".join(element_strings)) + "\n}"


    def __setitem__(self, key, item):
        self._d[key] = item
    
    def __getattr__(self, attr):
        return getattr(self._d, attr)


# default-dict returning "unknown" nodes for non-existing records
class RoverMap(Dict):

    def __getitem__(self, pos):
        try:
            return self._d[pos]
        except KeyError:
            self._d[pos] = Node.createUnknown(pos)
            return self[pos]
    

    def __getattr__(self, attr):
        return getattr(self._d, attr)

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

    def __hash__(self):
        # We want to be able to store Vectors in dict and set
        return self.x*997 + self.y
    
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


class Node(DbObject):
    """We want to implement a variant of DFS
    Node in the search graph corresponds to a cell in the map 
    it's either:
        "unknown" - not in the discovered set of nodes
        "discovered" - in the discovered set of nodes, but we haven't yet visited the node
        "open" - it was discovered and we have visited the node, but we haven't yet searched all reachable paths for that node
        "closed" - it was discovered, opened and all the reachable paths have been searched""" 
    
    UNKNOWN = "UNKNOWN"
    DISCOVERED = "DISCOVERED"
    OPEN = "OPEN"
    CLOSED = "CLOSED"

    SPACE = "SPACE"
    WALL = "WALL"
    UNKNOWN_TYPE = "UNKNOWN_TYPE"


    def __init__(self, coord: Vector, state, type):
        self.coord = coord

        # we add the node to our knowledge base when we "see" it with the sonar
        self.state = state

        self.type = type
    
    def __str__(self):
        return f"state: {self.state}, type: {self.type}"
    

    @classmethod
    def createWall(cls, pos):
        # we cannot ever step on the wall-square, so we set its state to "CLOSED" rightaway
        return Node(pos, state=Node.CLOSED, type=Node.WALL)

    @classmethod
    def createSpace(cls, pos):
        return Node(pos, state=Node.DISCOVERED, type=Node.SPACE)
    
    @classmethod
    def createUnknown(cls, pos):
        return Node(pos, state=Node.UNKNOWN, type=Node.UNKNOWN_TYPE)


class Database(DbObject):
    def __init__(self, init_position: Vector, orientation: Vector, goal: Vector):
        # initially the rover has access only to its position, orientation and goal coordinates
        self.position = init_position
        self.orientation = orientation
        self.goal = goal

        # at the beginning the only information we have is that rover's initial position must not be a wall
        start_node = Node.createSpace(self.position)
        start_node.state = Node.OPEN

        # the map which rover construct's in his database as he goes through the maze
        self.rover_map = RoverMap({self.position: start_node})


        # sonar sensor is injected by Maze, to which rover doesn't have direct access
        # the sonar interface is the only way rover can gather information about the walls/free space
        self.sonar = None

        # set of all database objects
        self.db = set()
    

if __name__ == "__main__":
    unk = Node.createUnknown(Vector(1,2))
    sp = Node.createSpace(Vector(4,2))
    w = Node.createWall(Vector(5,2))
    print(unk)
    print(sp)
    print(w)

    m = RoverMap({})
    print(m)
    m[Vector(1,2)]
    print(m)

    db = Database(Vector(1, 2), Vector(0, 1), Vector(20, 19))
    db.some_list = List([1,2,List([10, 11, 123]),4, [], 5])
    db.some_dict = Dict({"a": 1, "b": 2, (1, 0): "value", Vector(1,2): "this is v"})
    print(db)