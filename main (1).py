import tkinter as tk
import time
import random
from collections import deque
import heapq

# ──────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────
ROWS           = 10
COLS           = 10
CELL_SIZE      = 36
STEP_DELAY     = 0.15   # Slightly slower to see the 6-way logic clearly

# Diagonal move cost (√2) for UCS
DIAG_COST = 1.414

# ──────────────────────────────────────────
#  DESIGN & THEME
# ──────────────────────────────────────────
BG_MAIN     = "#1E1E24"
BG_PANEL    = "#2D2D35"
TEXT_MAIN   = "#E0E0E0"
TEXT_DIM    = "#AAAAAA"

COLOR = {
    "empty"        : "#2B2B30",
    "wall"         : "#121214",
    "start"        : "#00E676",
    "target"       : "#FF1744",
    "frontier"     : "#00B0FF",
    "explored"     : "#3F51B5",
    "path"         : "#FFC400",
    
    "fwd_frontier" : "#00B0FF",
    "bwd_frontier" : "#FF4081",
    "fwd_explored" : "#304FFE",
    "bwd_explored" : "#C51162",
    "meet"         : "#00E676",
}

# ──────────────────────────────────────────
#  STATIC GRID
# ──────────────────────────────────────────
BASE_GRID = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,0,1,0,0,0,0,1,0,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]

START  = (0, 0)
TARGET = (9, 9)

grid = [row[:] for row in BASE_GRID]

# ──────────────────────────────────────────
#  MOVEMENT ORDER (STRICT 6-WAY)
# ──────────────────────────────────────────
# The assignment requested strict Clockwise order:
# 1. Up, 2. Right, 3. Bottom, 4. Bottom-Right, 5. Left, 6. Top-Left
DIRECTIONS = [
    (-1,  0),  # 1. Up
    ( 0,  1),  # 2. Right
    ( 1,  0),  # 3. Bottom
    ( 1,  1),  # 4. Bottom-Right (Diagonal)
    ( 0, -1),  # 5. Left
    (-1, -1),  # 6. Top-Left (Diagonal)
]

# Set of diagonal moves for cost calculation
DIAG_PAIRS = {(1, 1), (-1, -1)}


# ──────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────

def reset_grid():
    global grid
    grid = [row[:] for row in BASE_GRID]

def get_neighbors(row, col):
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == 0:
            cost = DIAG_COST if (dr, dc) in DIAG_PAIRS else 1.0
            yield r, c, cost

# ──────────────────────────────────────────
#  DRAWING
# ──────────────────────────────────────────

def draw_grid(canvas, frontier=frozenset(), explored=frozenset(), path=frozenset(), status=""):
    canvas.delete("all")
    GAP = 2 
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * CELL_SIZE + GAP
            y1 = row * CELL_SIZE + GAP
            x2 = x1 + CELL_SIZE - GAP
            y2 = y1 + CELL_SIZE - GAP
            cell = (row, col)

            if cell == START:          color = COLOR["start"]
            elif cell == TARGET:       color = COLOR["target"]
            elif grid[row][col] == 1:  color = COLOR["wall"]
            elif cell in path:         color = COLOR["path"]
            elif cell in explored:     color = COLOR["explored"]
            elif cell in frontier:     color = COLOR["frontier"]
            else:                      color = COLOR["empty"]

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

            label, fg = "", "black"
            if cell == START:    label, fg = "S", "black"
            elif cell == TARGET: label, fg = "T", "white"
            
            if label:
                canvas.create_text(x1 + CELL_SIZE//2 - 2, y1 + CELL_SIZE//2 - 2,
                                   text=label, fill=fg, font=("Consolas", 14, "bold"))

    status_label.config(text=status)

def draw_grid_bidir(canvas, fwd_frontier=frozenset(), bwd_frontier=frozenset(),
                    fwd_explored=frozenset(), bwd_explored=frozenset(),
                    path=frozenset(), meet=None, status=""):
    canvas.delete("all")
    GAP = 2
    for row in range(ROWS):
        for col in range(COLS):
            x1 = col * CELL_SIZE + GAP
            y1 = row * CELL_SIZE + GAP
            x2 = x1 + CELL_SIZE - GAP
            y2 = y1 + CELL_SIZE - GAP
            cell = (row, col)

            if cell == START:          color = COLOR["start"]
            elif cell == TARGET:       color = COLOR["target"]
            elif grid[row][col] == 1:  color = COLOR["wall"]
            elif cell in path:         color = COLOR["path"]
            elif cell == meet:         color = COLOR["meet"]
            elif cell in fwd_explored and cell in bwd_explored: color = COLOR["meet"]
            elif cell in fwd_explored: color = COLOR["fwd_explored"]
            elif cell in bwd_explored: color = COLOR["bwd_explored"]
            elif cell in fwd_frontier: color = COLOR["fwd_frontier"]
            elif cell in bwd_frontier: color = COLOR["bwd_frontier"]
            else:                      color = COLOR["empty"]

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

            label, fg = "", "black"
            if cell == START:    label, fg = "S", "black"
            elif cell == TARGET: label, fg = "T", "white"

            if label:
                canvas.create_text(x1 + CELL_SIZE//2 - 2, y1 + CELL_SIZE//2 - 2,
                                   text=label, fill=fg, font=("Consolas", 14, "bold"))
    status_label.config(text=status)


# ──────────────────────────────────────────
#  ALGORITHMS
# ──────────────────────────────────────────

def bfs(canvas):
    def run_bfs(start_node=START):
        queue    = deque([[start_node]])
        explored = set()
        in_queue = {start_node}

        while queue:
            path    = queue.popleft()
            current = path[-1]
            in_queue.discard(current)

            if current in explored: continue
            explored.add(current)

            draw_grid(canvas, frontier=in_queue.copy(), explored=explored,
                      status=f"BFS – Exploring {current}")
            canvas.update()
            time.sleep(STEP_DELAY)

            if current == TARGET:
                draw_grid(canvas, path=set(path),
                          status=f"BFS DONE: Steps={len(path)}")
                canvas.update()
                return path

            row, col = current
            # BFS uses standard order
            for r, c, _ in get_neighbors(row, col):
                if (r, c) not in explored and (r, c) not in in_queue:
                    queue.append(path + [(r, c)])
                    in_queue.add((r, c))

        draw_grid(canvas, status="BFS FAILED")
        return None
    return run_bfs()


def dfs(canvas):
    def run_dfs(start_node=START):
        stack    = [[start_node]]
        explored = set()
        in_stack = {start_node}

        while stack:
            path    = stack.pop()
            current = path[-1]
            in_stack.discard(current)

            if current in explored: continue
            explored.add(current)

            draw_grid(canvas, frontier=in_stack.copy(), explored=explored,
                      status=f"DFS – Exploring {current}")
            canvas.update()
            time.sleep(STEP_DELAY)

            if current == TARGET:
                draw_grid(canvas, path=set(path),
                          status=f"DFS DONE: Steps={len(path)}")
                canvas.update()
                return path

            row, col = current
            # FIX: Reverse neighbors for DFS so Stack pops them in "correct" visual order
            neighbors = list(get_neighbors(row, col))
            for r, c, _ in reversed(neighbors):
                if (r, c) not in explored and (r, c) not in in_stack:
                    stack.append(path + [(r, c)])
                    in_stack.add((r, c))

        draw_grid(canvas, status="DFS FAILED")
        return None
    return run_dfs()


def dls(canvas, limit):
    def run_dls(start_node=START, lim=limit):
        stack    = [([start_node], 0)]
        explored = set()
        in_stack = {start_node}

        while stack:
            path, depth = stack.pop()
            current     = path[-1]
            in_stack.discard(current)

            if current in explored: continue
            explored.add(current)

            draw_grid(canvas, frontier=in_stack.copy(), explored=explored,
                      status=f"DLS – Depth {depth}/{lim}")
            canvas.update()
            time.sleep(STEP_DELAY)

            if current == TARGET:
                draw_grid(canvas, path=set(path),
                          status=f"DLS DONE: Depth {depth}")
                canvas.update()
                return path

            if depth >= lim: continue

            row, col = current
            # FIX: Reverse neighbors for DLS/DFS behavior
            neighbors = list(get_neighbors(row, col))
            for r, c, _ in reversed(neighbors):
                if (r, c) not in explored and (r, c) not in in_stack:
                    stack.append((path + [(r, c)], depth + 1))
                    in_stack.add((r, c))

        draw_grid(canvas, status=f"DLS FAILED (Limit {lim})")
        return None
    return run_dls()


def iddfs(canvas):
    max_lim  = ROWS * COLS
    for limit in range(max_lim + 1):
        draw_grid(canvas, status=f"IDDFS – Restarting (Limit {limit})")
        canvas.update()
        time.sleep(STEP_DELAY)

        stack    = [([START], 0)]
        explored = set()
        in_stack = {START}

        while stack:
            path, depth = stack.pop()
            current     = path[-1]
            in_stack.discard(current)

            if current in explored: continue
            explored.add(current)

            draw_grid(canvas, frontier=in_stack.copy(), explored=explored,
                      status=f"IDDFS (Lim {limit}) – Exploring {current}")
            canvas.update()
            time.sleep(STEP_DELAY)

            if current == TARGET:
                draw_grid(canvas, path=set(path),
                          status=f"IDDFS DONE: Limit {limit}, Steps {len(path)}")
                canvas.update()
                return path

            if depth < limit:
                row, col = current
                # FIX: Reverse neighbors
                neighbors = list(get_neighbors(row, col))
                for r, c, _ in reversed(neighbors):
                    if (r, c) not in explored and (r, c) not in in_stack:
                        stack.append((path + [(r, c)], depth + 1))
                        in_stack.add((r, c))
                        
        draw_grid(canvas, explored=explored, status=f"IDDFS Limit {limit} Exhausted")
        canvas.update()
        time.sleep(STEP_DELAY * 1.5)

    draw_grid(canvas, status="IDDFS FAILED")
    return None


def ucs(canvas):
    counter  = 0
    pq       = [(0.0, counter, [START])]
    explored = set()
    best_cost = {START: 0.0}

    while pq:
        cost, _, path = heapq.heappop(pq)
        current       = path[-1]

        if current in explored: continue
        explored.add(current)

        frontier = {entry[2][-1] for entry in pq}
        draw_grid(canvas, frontier=frontier, explored=explored,
                  status=f"UCS – Cost: {cost:.2f}")
        canvas.update()
        time.sleep(STEP_DELAY)

        if current == TARGET:
            draw_grid(canvas, path=set(path),
                      status=f"UCS DONE: Cost {cost:.2f}")
            canvas.update()
            return path

        row, col = current
        for r, c, move_cost in get_neighbors(row, col):
            if (r, c) not in explored:
                new_cost = cost + move_cost
                if new_cost < best_cost.get((r, c), float('inf')):
                    best_cost[(r, c)] = new_cost
                    counter += 1
                    heapq.heappush(pq, (new_cost, counter, path + [(r, c)]))

    draw_grid(canvas, status="UCS FAILED")
    return None


def bidirectional(canvas):
    fwd_queue    = deque([START])
    bwd_queue    = deque([TARGET])
    fwd_frontier = {START}
    bwd_frontier = {TARGET}
    fwd_explored = {START: None}
    bwd_explored = {TARGET: None}

    def reconstruct(meet_node):
        fwd_half = []
        node = meet_node
        while node is not None:
            fwd_half.append(node)
            node = fwd_explored.get(node)
        fwd_half.reverse()

        bwd_half = []
        node = bwd_explored.get(meet_node)
        while node is not None:
            bwd_half.append(node)
            node = bwd_explored.get(node)
        bwd_half.append(TARGET)
        return fwd_half + bwd_half

    meet_node = None

    while fwd_queue or bwd_queue:
        if fwd_queue:
            current = fwd_queue.popleft()
            fwd_frontier.discard(current)
            draw_grid_bidir(canvas, fwd_frontier=fwd_frontier.copy(), bwd_frontier=bwd_frontier.copy(),
                            fwd_explored=set(fwd_explored), bwd_explored=set(bwd_explored),
                            status=f"BiDir – FWD: {current}")
            canvas.update()
            time.sleep(STEP_DELAY)
            if current in bwd_explored:
                meet_node = current
                break
            for r, c, _ in get_neighbors(current[0], current[1]):
                if (r, c) not in fwd_explored and (r, c) not in fwd_frontier:
                    fwd_explored[(r, c)] = current
                    fwd_frontier.add((r, c))
                    fwd_queue.append((r, c))

        if bwd_queue:
            current = bwd_queue.popleft()
            bwd_frontier.discard(current)
            draw_grid_bidir(canvas, fwd_frontier=fwd_frontier.copy(), bwd_frontier=bwd_frontier.copy(),
                            fwd_explored=set(fwd_explored), bwd_explored=set(bwd_explored),
                            status=f"BiDir – BWD: {current}")
            canvas.update()
            time.sleep(STEP_DELAY)
            if current in fwd_explored:
                meet_node = current
                break
            for r, c, _ in get_neighbors(current[0], current[1]):
                if (r, c) not in bwd_explored and (r, c) not in bwd_frontier:
                    bwd_explored[(r, c)] = current
                    bwd_frontier.add((r, c))
                    bwd_queue.append((r, c))

    if meet_node:
        full_path = reconstruct(meet_node)
        draw_grid_bidir(canvas, fwd_explored=set(fwd_explored), bwd_explored=set(bwd_explored),
                        path=set(full_path), meet=meet_node, status=f"BiDir DONE: Meeting at {meet_node}")
        canvas.update()
        return full_path

    draw_grid_bidir(canvas, status="BiDir FAILED")
    return None


# ──────────────────────────────────────────
#  GUI SETUP
# ──────────────────────────────────────────

def run_algorithm():
    reset_grid()
    draw_grid(canvas, status="Initializing...")
    canvas.update()
    run_btn.config(state=tk.DISABLED, bg="#555555")
    root.update()

    algo = algo_var.get()
    try:
        if   algo == "BFS":   bfs(canvas)
        elif algo == "DFS":   dfs(canvas)
        elif algo == "UCS":   ucs(canvas)
        elif algo == "IDDFS": iddfs(canvas)
        elif algo == "Bidir": bidirectional(canvas)
        elif algo == "DLS":
            try:
                limit = int(depth_var.get())
                if limit < 0: raise ValueError
            except ValueError:
                status_label.config(text="Error: Invalid Depth")
                return
            dls(canvas, limit)
    finally:
        run_btn.config(state=tk.NORMAL, bg=COLOR["start"])

def build_legend(parent):
    legend_frame = tk.Frame(parent, bg=BG_PANEL, pady=10)
    legend_frame.pack(fill=tk.X, side=tk.BOTTOM)
    items = [("Start", COLOR["start"]), ("Target", COLOR["target"]),
             ("Wall", COLOR["wall"]), ("Path", COLOR["path"]),
             ("Frontier", COLOR["frontier"]), ("Explored", COLOR["explored"])]
    center_box = tk.Frame(legend_frame, bg=BG_PANEL)
    center_box.pack(anchor=tk.CENTER)
    for i, (text, col) in enumerate(items):
        tk.Label(center_box, bg=col, width=2, height=1).grid(row=0, column=i*2, padx=(10, 2))
        tk.Label(center_box, text=text, bg=BG_PANEL, fg=TEXT_DIM, font=("Segoe UI", 9)).grid(row=0, column=i*2+1)

root = tk.Tk()
root.title("GOOD PERFORMANCE TIME APP")
root.resizable(False, False)
root.configure(bg=BG_MAIN)

header_frame = tk.Frame(root, bg=BG_MAIN, pady=15)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="GOOD PERFORMANCE TIME APP", 
         font=("Segoe UI", 16, "bold"), fg=TEXT_MAIN, bg=BG_MAIN).pack()
status_label = tk.Label(header_frame, text="Ready", 
                        font=("Consolas", 11), fg=COLOR["frontier"], bg=BG_MAIN)
status_label.pack(pady=(5,0))

canvas_frame = tk.Frame(root, bg=BG_MAIN, padx=15, pady=5)
canvas_frame.pack()
canvas = tk.Canvas(canvas_frame, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE,
                   bg=BG_MAIN, bd=0, highlightthickness=0)
canvas.pack()

control_panel = tk.Frame(root, bg=BG_PANEL, pady=10, padx=10)
control_panel.pack(fill=tk.X, pady=(10, 0))
ctrl_inner = tk.Frame(control_panel, bg=BG_PANEL)
ctrl_inner.pack()

tk.Label(ctrl_inner, text="ALGORITHM:", bg=BG_PANEL, fg=TEXT_DIM, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(0,5))
algo_var = tk.StringVar(root)
algo_var.set("BFS")
algo_menu = tk.OptionMenu(ctrl_inner, algo_var, "BFS", "DFS", "UCS", "DLS", "IDDFS", "Bidir")
algo_menu.config(bg="#424242", fg="white", highlightthickness=0, borderwidth=0, width=8)
algo_menu["menu"].config(bg="#424242", fg="white")
algo_menu.grid(row=0, column=1, padx=(0, 20))

tk.Label(ctrl_inner, text="DLS LIMIT:", bg=BG_PANEL, fg=TEXT_DIM, font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=(0,5))
depth_var = tk.StringVar(root, value="15")
tk.Entry(ctrl_inner, textvariable=depth_var, width=4, bg="#424242", fg="white", 
         font=("Consolas", 11), relief=tk.FLAT, justify="center").grid(row=0, column=3, padx=(0, 20))

run_btn = tk.Button(ctrl_inner, text="EXECUTE", command=run_algorithm,
                    bg=COLOR["start"], fg="black", font=("Segoe UI", 10, "bold"),
                    relief=tk.FLAT, padx=20, pady=5, activebackground="#00C853")
run_btn.grid(row=0, column=4)

build_legend(root)
draw_grid(canvas, status="Select Algorithm and press EXECUTE")

root.mainloop()