# Algorithm Visualization Lab

A modular Python-based visualization framework for exploring classical algorithms, cellular automata, fractals, and procedural generation systems.

This project focuses on clarity, correctness, and architectural separation between algorithm logic and rendering.

## Overview

Algorithm Visualization Lab provides interactive visual demonstrations of:

- Graph traversal and shortest path algorithms
- Comparison-based sorting algorithms
- Backtracking and constraint-solving systems
- Fractal geometry
- Cellular automata
- Procedural pattern generation
- Grid-based simulations

The goal is to improve conceptual understanding through deterministic and step-wise visual execution.

## Steps to run

1. Install the dependencies

```bash
uv sync
```

2. Run the app

```bash
uv run visualizations
```

## Implemented Systems

### Graph & Pathfinding

- A\* Search
- Dijkstra’s Algorithm
- Breadth-First Search (BFS)
- Depth-First Search (DFS)

### Sorting

- Bubble Sort
- Selection Sort
- Insertion Sort

### Constraint Solvers

- N-Queens
- Sudoku Solver

### Fractals

- Hilbert Curve

### Cellular Automata

- Conway’s Game of Life
- Wolfram Elementary Automata

### Procedural Generation

- Wave Function Collapse

### Computational Geometry

- Marching Squares

### Simulation

- Sand Particle Simulation

## Architecture

- Separation of algorithm logic from rendering layer
- Modular directory structure
- Reusable grid and animation framework
- Deterministic simulation stepping
- Object-oriented design

## Tech Stack

- **Python** – Core algorithm implementations
- **Pygame** – Real-time rendering and interaction
- **UV** – Dependency and environment management

## Goals

- Strengthen intuition for classical algorithms
- Visualize algorithmic state transitions
- Explore emergent behavior systems
- Build a reusable visualization framework
