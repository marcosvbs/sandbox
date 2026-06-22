# sandbox

A collection of small experiments. Built to learn, not to ship.

## Index

| Experiment | Description |
| --- | --- |
| [bfs_pathfinder](bfs_pathfinder/) | Visualize Breadth-First Search finding the shortest path on a grid. |

## Experiments

### bfs_pathfinder

A Tkinter GUI that visualizes Breadth-First Search finding the shortest path on a 10×10 grid.

**How it works**

- Click cells to set up the board:
  1. First click places the **start** (blue).
  2. Second click places the **end** (orange).
  3. Further clicks toggle **walls** (black).
- **Find Shortest Path** runs BFS with an animated search: explored cells turn gray, the final shortest path turns green. Result is printed to the console (`Found it!` / `No path found`).
- **Reset** clears the board.

**Run**

```bash
python bfs_pathfinder/bfs_pathfinder.py
```

Requires Python 3 with Tkinter — standard library only, no extra dependencies.

## Adding an experiment

1. Create a new directory for the experiment.
2. Add a row to the [Index](#index).
3. Add a `###` section under [Experiments](#experiments) describing what it does and how to run it.
