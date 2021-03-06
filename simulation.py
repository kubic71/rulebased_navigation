from maze import Maze
from rule_engine import RuleEngine, Rule, AlwaysCondition
from rules import UpdateMapWithSensorData, IsFreeSpaceForward, StepForward, RandomRotation
import time

random_walk_rules = [
    Rule(AlwaysCondition(), UpdateMapWithSensorData()),
    Rule(IsFreeSpaceForward(), StepForward()),
    Rule(AlwaysCondition(), RandomRotation())
]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=10, help="Height of the maze")
    parser.add_argument("--n", type=int, default=15, help="Width of the maze")
    parser.add_argument("--fill", type=float, default=0.1, help="Percentage of the maze filled with walls.")
    parser.add_argument("--n_steps", type=int, default=10, help="How many passes through the rule-set are made")

    parser.add_argument("--delay", type=float, default=0)

    parser.add_argument("--verbose", default=False, dest="verbose", action="store_true")

    args = parser.parse_args()
    maze = Maze(percent_fill=args.fill, size=(args.m, args.n))
    db = maze.db

    engine = RuleEngine(random_walk_rules, db=db, maze=maze, delay=args.delay, verbose=args.verbose)

    print(maze)
    print(maze.db)
    for i in range(args.n_steps):
        # engine.step() makes 1 pass through the rule-set
        # in one pass, more than 1 rule can be matched
        engine.step()

