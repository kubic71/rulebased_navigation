# Rule-based navigation

## Running the simulation
`simulation.py` accepts the command line parameters:
```
$ python simulation.py --help

usage: simulation.py [-h] [--m M] [--n N] [--fill FILL] [--delay DELAY] [--verbose]

optional arguments:
  -h, --help     show this help message and exit
  --m M          Height of the maze
  --n N          Width of the maze
  --fill FILL    Percentage of the maze filled with walls.
  --delay DELAY
  --verbose
```


For example:
```
$ python simulation.py --delay 2 --m 8 --n 10 --fill 0.1
```
This will run the simulation in a 8x10 grid with 10% of the maze being filled with walls. There will be 2 second delay between each matched rule execution. 


