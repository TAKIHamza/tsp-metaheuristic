# Travelling Salesman Problem – Metaheuristic Approach

This project studies the **Travelling Salesman Problem (TSP)** using a combination of a **greedy heuristic** and a **metaheuristic optimization method**.

The goal is to compare the performance of a simple constructive heuristic with a more advanced optimization technique in order to improve the quality of the obtained solutions.

---

## Project Overview

The Travelling Salesman Problem is one of the most famous problems in **combinatorial optimization** and **operations research**.

Given a set of cities and the distances between them, the objective is to find the shortest possible route that:

- visits each city exactly once
- returns to the starting city
- minimizes the total travel distance

Since the problem is **NP-hard**, exact methods become impractical for large instances. Therefore, heuristic and metaheuristic approaches are often used.

This project implements:

- **Greedy heuristic (Nearest Neighbor)**
- **Simulated Annealing metaheuristic**
- **2-opt neighborhood for solution improvement**

---

## Algorithms Implemented

### 1. Greedy Heuristic – Nearest Neighbor

This algorithm constructs an initial solution by repeatedly selecting the **closest unvisited city**.

Advantages:
- Very fast
- Simple to implement

Limitation:
- Often produces suboptimal solutions

---

### 2. Simulated Annealing

Simulated Annealing is a **metaheuristic inspired by the annealing process in metallurgy**.

The algorithm improves the initial solution by exploring neighboring solutions and occasionally accepting worse solutions to escape local minima.

Key parameters studied:

- Initial temperature
- Cooling factor
- Number of iterations per temperature level

---

### 3. 2-opt Neighborhood

The **2-opt operator** is used to generate neighboring solutions by removing two edges and reconnecting the tour differently.

This helps reduce crossing edges and improve the tour length.

---

---

## Dataset

The experiments are conducted using several instances from the **TSPLIB benchmark dataset**, including:

- berlin52
- eil51
- eil76
- kroA100
- bier127
- ch150
- a280

These datasets are widely used to evaluate TSP algorithms.

---

## Experimental Results

The project compares:

- solution cost
- execution time
- improvement percentage

Graphs are generated to analyze:

- Greedy vs Simulated Annealing performance
- influence of parameters such as temperature and iteration count

---

## How to Run the Project

Clone the repository:

```bash
git clone https://github.com/TAKIHamza/tsp-metaheuristic.git

Go to the project directory:
```bash
cd tsp-metaheuristic


Install dependencies:
```bash
pip install -r requirements.txt


Run the program:
```bash
python main.py

Author

Hamza TAKI
Master IARO – Operations Research and Artificial Intelligence
