from rule_engine import Rule, Condition, Action
from db_helper import Node
import random


class IsFreeSpaceForward(Condition):
    def match(self, db):
        return db.rover_map[db.position + db.orientation].type == Node.SPACE

class StepForward(Action):
    def do(self, db):
        db.position += db.orientation
        
class RandomRotation(Action):
    def do(self, db):
        db.orientation = db.orientation.rotate(clockwise=bool(random.randint(0, 1)))
        

class UpdateMapWithSensorData(Action):

    def _do_for_one_sonar(self, db, sonar_dir, sonar_dist):
        for i in range(1, sonar_dist):
            cell_pos = sonar_dir*i + db.position

            # cell_pos is not yet discovered
            if db.rover_map[cell_pos].state == Node.UNKNOWN:
                db.rover_map[cell_pos] = Node.createSpace(cell_pos)
        
        # add the wall to the database as well (if it's not already there)
        wall_pos = sonar_dir*sonar_dist + db.position

        # wall not yet discovered
        if db.rover_map[wall_pos].state == Node.UNKNOWN:
            db.rover_map[wall_pos] = Node.createWall(wall_pos)


    def do(self, db):
        # Add Walls/Free space information to the db based on sensor data
        self._do_for_one_sonar(db, db.orientation, db.sonar.forward)
        self._do_for_one_sonar(db, db.orientation.rotate(clockwise=False), db.sonar.left)
        self._do_for_one_sonar(db, db.orientation.rotate(clockwise=True), db.sonar.right)
