import tkinter as tk
import heapq
import random

EMPTY, START, END, WALL = -1, -2, -3, -4

WIN_BG = "#181825"
GRID_BG = "#1e1e2e"
TEXT_FG = "#cdd6f4"
COLORS = {
    EMPTY: "#313244",
    START: "#89b4fa",
    END: "#fab387",
    WALL: "#11111b",
    "PATH": "#a6e3a1",
    "SEARCHED": "#585b70",
}

ROWS, COLUMNS, CELL_SIZE = 10, 10, 54
STEP_DELAY = 50
CELL_GAP = 3

board = [[random.randint(1, 5) for _ in range(COLUMNS)] for _ in range(ROWS)]
visited = set()
path = set()

start = None
end = None
has_searched = False
search_after_id = None

root = tk.Tk()
root.title("Dijkstra Random Weights")
root.configure(bg=WIN_BG)

container = tk.Frame(root, bg=WIN_BG, padx=20, pady=18)
container.pack()

canvas = tk.Canvas(
    container,
    width=COLUMNS * CELL_SIZE,
    height=ROWS * CELL_SIZE,
    bg=GRID_BG,
    highlightthickness=0,
    bd=0,
)
canvas.pack()


def draw_board():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLUMNS):
            val = board[r][c]

            if (r, c) in path:
                color = COLORS["PATH"]
            elif (r, c) in visited:
                color = COLORS["SEARCHED"]
            else:
                color = COLORS.get(val, "#45475a")

            x1, y1 = c * CELL_SIZE + CELL_GAP, r * CELL_SIZE + CELL_GAP
            x2, y2 = x1 + CELL_SIZE - 2 * CELL_GAP, y1 + CELL_SIZE - 2 * CELL_GAP

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

            if isinstance(val, int) and val > 0:
                text_color = "#1e1e2e" if (r, c) in path else "white"
                canvas.create_text(
                    x1 + CELL_SIZE // 2 - CELL_GAP,
                    y1 + CELL_SIZE // 2 - CELL_GAP,
                    text=str(val),
                    fill=text_color,
                    font=("Arial", 12, "bold"),
                )


def randomize_weights():
    if has_searched:
        return
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] not in (START, END, WALL):
                board[r][c] = random.randint(1, 5)
    draw_board()


def on_click(event):
    if has_searched:
        return
    global start, end
    c, r = event.x // CELL_SIZE, event.y // CELL_SIZE
    if not (0 <= r < ROWS and 0 <= c < COLUMNS):
        return

    if not start:
        board[r][c] = START
        start = (r, c)
    elif not end and (r, c) != start:
        board[r][c] = END
        end = (r, c)
    elif (r, c) != start and (r, c) != end:
        board[r][c] = WALL if board[r][c] != WALL else 1

    draw_board()


canvas.bind("<Button-1>", on_click)


def find_path():
    global has_searched, search_after_id
    if not start or not end or has_searched:
        return
    has_searched = True
    pq = [(0, start[0], start[1])]
    distances = {start: 0}
    came_from = {start: None}

    def step():
        global search_after_id
        if not pq:
            return
        dist, r, c = heapq.heappop(pq)
        curr = (r, c)

        if curr == end:
            node = came_from[end]
            while node and node != start:
                path.add(node)
                node = came_from[node]
            draw_board()
            return

        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < ROWS and 0 <= nc < COLUMNS and board[nr][nc] != WALL:
                weight = board[nr][nc] if board[nr][nc] > 0 else 1
                new_dist = dist + weight
                if (nr, nc) not in distances or new_dist < distances[(nr, nc)]:
                    distances[(nr, nc)] = new_dist
                    came_from[(nr, nc)] = curr
                    heapq.heappush(pq, (new_dist, nr, nc))

        if curr != start:
            visited.add(curr)
        draw_board()
        search_after_id = root.after(STEP_DELAY, step)

    step()


def reset():
    global start, end, board, has_searched, search_after_id, visited, path
    if search_after_id is not None:
        root.after_cancel(search_after_id)
        search_after_id = None
    board = [[random.randint(1, 5) for _ in range(COLUMNS)] for _ in range(ROWS)]
    visited = set()
    path = set()
    start, end, has_searched = None, None, False
    draw_board()


btn_frame = tk.Frame(container, bg=WIN_BG)
btn_frame.pack(fill="x", pady=10)
tk.Button(btn_frame, text="Randomize", command=randomize_weights).pack(
    side="left", fill="x", expand=True
)
tk.Button(btn_frame, text="Find Path", command=find_path).pack(
    side="left", fill="x", expand=True
)
tk.Button(btn_frame, text="Reset", command=reset).pack(
    side="left", fill="x", expand=True
)

draw_board()
root.mainloop()
