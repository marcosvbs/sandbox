import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from collections import deque

EMPTY, START, END, WALL, PATH, SEARCHED = range(6)

WIN_BG = "#181825"
GRID_BG = "#1e1e2e"
GRID_LINE = "#1e1e2e"
TEXT_FG = "#cdd6f4"
SUBTLE_FG = "#9399b2"

COLORS = {
    EMPTY: "#313244",
    START: "#89b4fa",
    END: "#fab387",
    WALL: "#11111b",
    PATH: "#a6e3a1",
    SEARCHED: "#585b70",
}

ROWS, COLUMNS, CELL_SIZE = 10, 10, 54
STEP_DELAY = 26
CELL_GAP = 3
CELL_RADIUS = 10

board = [[EMPTY] * COLUMNS for _ in range(ROWS)]
start = None
end = None
has_searched = False
search_after_id = None

root = tk.Tk()
root.title("BFS Pathfinder")
root.configure(bg=WIN_BG)
root.resizable(False, False)

container = tk.Frame(root, bg=WIN_BG, padx=20, pady=18)
container.pack()

title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
sub_font = tkfont.Font(family="Helvetica", size=10)
header = tk.Frame(container, bg=WIN_BG)
header.pack(fill="x", pady=(0, 12))
tk.Label(header, text="BFS Pathfinder", font=title_font, fg=TEXT_FG, bg=WIN_BG).pack(
    anchor="w"
)
tk.Label(
    header,
    text="Click: 1st = start, 2nd = end, rest = toggle walls. Then find the shortest path.",
    font=sub_font,
    fg=SUBTLE_FG,
    bg=WIN_BG,
).pack(anchor="w")

canvas = tk.Canvas(
    container,
    width=COLUMNS * CELL_SIZE,
    height=ROWS * CELL_SIZE,
    bg=GRID_BG,
    highlightthickness=0,
    bd=0,
)
canvas.pack()


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
        board[r][c] = WALL if board[r][c] == EMPTY else EMPTY

    draw_board()


canvas.bind("<Button-1>", on_click)


def _round_rect(x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r,
        y1,
        x2 - r,
        y1,
        x2,
        y1,
        x2,
        y1 + r,
        x2,
        y2 - r,
        x2,
        y2,
        x2 - r,
        y2,
        x1 + r,
        y2,
        x1,
        y2,
        x1,
        y2 - r,
        x1,
        y1 + r,
        x1,
        y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def draw_board():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLUMNS):
            x1 = c * CELL_SIZE + CELL_GAP
            y1 = r * CELL_SIZE + CELL_GAP
            x2 = x1 + CELL_SIZE - 2 * CELL_GAP
            y2 = y1 + CELL_SIZE - 2 * CELL_GAP
            _round_rect(
                x1,
                y1,
                x2,
                y2,
                CELL_RADIUS,
                fill=COLORS[board[r][c]],
                outline=GRID_LINE,
                width=1,
            )


def neighbours(r, c):
    result = []
    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
        if 0 <= nr < ROWS and 0 <= nc < COLUMNS:
            result.append((nr, nc))
    return result


def find_path():
    global has_searched, search_after_id
    if start is None or end is None:
        return

    has_searched = True

    queue = deque([start])
    came_from = {start: None}

    def step():
        global search_after_id

        if not queue:
            search_after_id = None
            print("No path found")
            return

        current = queue.popleft()

        if current == end:
            node = came_from[end]
            while node is not None and node != start:
                board[node[0]][node[1]] = PATH
                node = came_from[node]
            draw_board()
            search_after_id = None
            print("Found it!")
            return

        if current != start:
            board[current[0]][current[1]] = SEARCHED

        for nb in neighbours(*current):
            if nb not in came_from and board[nb[0]][nb[1]] != WALL:
                came_from[nb] = current
                queue.append(nb)

        draw_board()
        search_after_id = root.after(STEP_DELAY, step)

    step()


def reset():
    global start, end, board, has_searched, search_after_id
    if search_after_id is not None:
        root.after_cancel(search_after_id)
        search_after_id = None
    board = [[EMPTY] * COLUMNS for _ in range(ROWS)]
    start, end = None, None
    has_searched = False
    draw_board()


legend = tk.Frame(container, bg=WIN_BG)
legend.pack(fill="x", pady=(12, 12))
legend_font = tkfont.Font(family="Helvetica", size=9)
for label, color in (
    ("Start", COLORS[START]),
    ("End", COLORS[END]),
    ("Wall", COLORS[WALL]),
    ("Searched", COLORS[SEARCHED]),
    ("Path", COLORS[PATH]),
):
    item = tk.Frame(legend, bg=WIN_BG)
    item.pack(side="left", padx=(0, 14))
    tk.Label(item, bg=color, width=2, height=1, bd=0, relief="flat").pack(
        side="left", padx=(0, 5)
    )
    tk.Label(item, text=label, font=legend_font, fg=SUBTLE_FG, bg=WIN_BG).pack(
        side="left"
    )

style = ttk.Style()
style.theme_use("clam")
btn_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
style.configure(
    "Primary.TButton",
    font=btn_font,
    foreground="#11111b",
    background="#89b4fa",
    borderwidth=0,
    focuscolor="#89b4fa",
    padding=(12, 10),
)
style.map("Primary.TButton", background=[("active", "#74a0f0"), ("pressed", "#6690e6")])
style.configure(
    "Neutral.TButton",
    font=btn_font,
    foreground=TEXT_FG,
    background="#45475a",
    borderwidth=0,
    focuscolor="#45475a",
    padding=(12, 10),
)
style.map("Neutral.TButton", background=[("active", "#585b70"), ("pressed", "#3a3c4e")])

buttons = tk.Frame(container, bg=WIN_BG)
buttons.pack(fill="x")
ttk.Button(
    buttons, text="Find Shortest Path", command=find_path, style="Primary.TButton"
).pack(side="left", expand=True, fill="x", padx=(0, 5))
ttk.Button(buttons, text="Reset", command=reset, style="Neutral.TButton").pack(
    side="left", expand=True, fill="x", padx=(5, 0)
)

draw_board()
root.mainloop()
