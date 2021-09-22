from db_helper import Database, Vector, SonarSensor
from directions import all_directions, directions_map

import random

# random.seed(42)

class Maze:
    def __init__(self, percent_fill=0.1, size=(30, 40)):
        m, n = size
        self.m, self.n = m, n

        # generate random maze by filling "percent_fill" portion of all squares
        all_pos = [(x, y) for x in range(m) for y in range(n)]
        random.shuffle(all_pos)

        self.walls = set(all_pos[: int(percent_fill * m * n)])

        # add walls around the valid maze positions
        self.walls = self.walls.union(
            set(
                [
                    (x, y)
                    for x in range(-1, m + 1)
                    for y in range(-1, n + 1)
                    if x < 0 or x >= m or y < 0 or y >= n
                ]
            )
        )
        self.free = set(
            [(x, y) for x in range(m) for y in range(n) if (x, y) not in self.walls]
        )

        self.db = self.place_rover_and_goal_randomly()
        self.add_sonar_callback(self.db)
    
    def add_sonar_callback(self, db):
        db.sonar = SonarSensor(self.left_sonar, self.forward_sonar, self.right_sonar)

    def _count_dist_to_wall(self, direction):
        current = self.db.position
        dist = 0

        while current.to_tuple() not in self.walls:
            dist += 1
            current += direction
        return dist


    # Get distances to the walls for left, forward and right sonar sensors
    def left_sonar(self):
        sonar_ray = self.db.orientation.rotate(clockwise=False)
        return self._count_dist_to_wall(sonar_ray)

    def forward_sonar(self):
        return self._count_dist_to_wall(self.db.orientation)

    def right_sonar(self):
        sonar_ray = self.db.orientation.rotate(clockwise=True)
        return self._count_dist_to_wall(sonar_ray)

    def sonar(self):
        return self.left_sonar(), self.forward_sonar(), self.right_sonar()
        

    def place_rover_and_goal_randomly(self):
        # place randomly the rover and the goal
        free_list = list(self.free)
        random.shuffle(free_list)

        rover_pos = Vector(*free_list[0])
        goal = Vector(*free_list[1])
        return Database(rover_pos, Vector.from_tuple(random.choice(all_directions)), goal)

    def __str__(self):
        s = ""
        for y in range(-1, self.n + 1):
            for x in range(-1, self.m + 1):
                v = (x, y)
                if v in self.walls:
                    s += "X "

                elif v == self.db.position.to_tuple():
                    s += directions_map[self.db.orientation.to_tuple()] + " "

                elif v == self.db.goal.to_tuple():
                    s += "@ "

                elif v in self.free:
                    s += "  "

                else:
                    raise Exception("bug:", v)
            s += "\n"
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    m = Maze(size=(10, 15))
    print(m)
    print(m.db)