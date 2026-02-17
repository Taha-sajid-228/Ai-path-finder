🧠 Assignment 01
GOOD PERFORMANCE TIME APP

Name: Muhammad Taha Sajid
Roll No: 24F-0760

🚀 Project Report: GOOD PERFORMANCE TIME APP
📌 1. Introduction

The GOOD PERFORMANCE TIME APP is an interactive visualization tool designed to demonstrate the behavior of fundamental Uninformed Search Algorithms in Artificial Intelligence.

Pathfinding is a core AI problem where an agent must move from a Start State to a Goal State while avoiding obstacles.

This project implements six search strategies inside a 10×10 grid environment.
The application uses Python’s Tkinter GUI to animate the search process step-by-step, allowing users to observe:

🔵 Frontier (nodes to be visited)

🟣 Explored Set (visited nodes)

🟡 Final Optimal Path

🎯 2. Problem Statement & Environment

The objective is to navigate an agent from:

Start Node (S) → (0,0)

Target Node (T) → (9,9)

inside a static grid containing obstacles.

⚙️ Environment Configuration

Grid Size: 10 × 10

Movement: 8-Directional

Up, Down, Left, Right

4 Diagonals

💰 Cost Model

Orthogonal moves → 1.0

Diagonal moves → √2 ≈ 1.414

⛔ Constraints

The agent cannot pass through black wall nodes.

🧩 3. Implemented Algorithms
3.1 Breadth-First Search (BFS)

Mechanism:
Explores neighbors level by level using FIFO order.

Data Structure: collections.deque

✅ Pros

Complete

Optimal (minimum number of steps)

❌ Cons

High memory consumption

Does not consider weighted costs (treats diagonals same as orthogonal)

3.2 Depth-First Search (DFS)

Mechanism:
Explores deeply along a branch before backtracking.

Data Structure: Python list (Stack)

✅ Pros

Low memory requirement

❌ Cons

Not Optimal

Not always Complete (handled using explored set in this implementation)

3.3 Uniform-Cost Search (UCS)

Mechanism:
Expands the node with the lowest path cost g(n).

Equivalent to Dijkstra’s Algorithm.

Data Structure: heapq (Priority Queue)

✅ Pros

Complete

Optimal (considers diagonal cost 1.414)

❌ Cons

Slower than BFS in some cases

Higher memory usage

3.4 Depth-Limited Search (DLS)

Mechanism:
DFS with a fixed depth limit.

User Input: Depth limit (e.g., 15)

✅ Pros

Prevents infinite deep exploration

❌ Cons

Incomplete if target depth > limit

3.5 Iterative Deepening DFS (IDDFS)

Mechanism:
Runs DLS repeatedly with increasing limits (0, 1, 2, ...)

✅ Pros

Complete

Optimal (in step cost)

Low memory usage

❌ Cons

Re-explores nodes multiple times (acceptable overhead)

3.6 Bidirectional Search

Mechanism:
Runs two BFS searches simultaneously:

Forward from Start

Backward from Target

Stops when both frontiers meet.

✅ Pros

Extremely Fast

Time complexity: O(b^(d/2))

❌ Cons

More complex implementation

Requires known goal state

📊 4. Comparative Analysis
Algorithm	Complete	Optimal	Time Complexity	Space Complexity
BFS	Yes	Yes (steps)	High	High
DFS	No	No	Low	Low
UCS	Yes	Yes (cost)	Medium	High
IDDFS	Yes	Yes (steps)	Medium	Low
Bidirectional	Yes	Yes (steps)	Very Low	High
🔎 Key Findings

Fastest Algorithm:
Bidirectional Search converged fastest because it searches from both sides.

Most Accurate Path:
UCS produced the most precise path due to weighted diagonal cost (1.414).

Most Erratic Behavior:
DFS generated winding, non-optimal paths.

🎨 5. GUI Implementation Details

The interface uses a modern theme for clear visualization.

📚 Libraries Used

tkinter → GUI

time → Animation

collections → Queue

heapq → Priority Queue

🎨 Visual Legend
Color	Meaning
Cyan	Frontier
Indigo	Explored Nodes
Gold	Final Path
Green	Start / Meeting Point
Red	Target
Black	Wall
🧪 6. Test Cases (Visual Proof)

📌 (Insert screenshots of your running application here in your GitHub repo)

Scenario A: Breadth-First Search (BFS)

Expands uniformly.

Finds minimum step solution.

📷 Insert Screenshot Here

Scenario B: Depth-First Search (DFS)

Explores deeply before backtracking.

Produces sub-optimal winding path.

📷 Insert Screenshot Here

Scenario C: Bidirectional Search

Two frontiers expand simultaneously.

Meets in the middle.

Fastest convergence.

📷 Insert Screenshot Here

🏁 7. Conclusion

The GOOD PERFORMANCE TIME APP successfully demonstrates the trade-offs between uninformed search algorithms.

BFS & UCS → Guarantee optimality

Bidirectional → Best speed performance

DFS → Memory efficient but unreliable

IDDFS → Balanced approach

This project highlights that algorithm choice depends on:

⚡ Speed

💾 Memory

📏 Path Optimality

▶️ How to Run
python your_filename.py


Make sure Python 3 is installed.

👨‍💻 Author

Muhammad Taha Sajid
Roll No: 24F-0760