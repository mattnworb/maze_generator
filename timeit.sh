#!/bin/bash
python -m timeit -s "from maze_generator import MazeWalker, Maze" "MazeWalker(Maze(60, 50)).solve()"
