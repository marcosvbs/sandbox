import tkinter as tk
from collections import deque

EMPTY, START, END, WALL, PATH, SEARCHED = range(6)

COLORS = {
    EMPTY: "white",
    START: "blue",
    END: "orange",
    WALL: "black",
    PATH: "green",
    SEARCHED: "gray",
}

ROWS, COLUMNS, CELL_SIZE = 10, 10, 50
STEP_DELAY = 30

board = [[EMPTY] * COLUMNS for _ in range(ROWS)]
start = None
end = None
has_searched = False
search_after_id = None

root = tk.Tk()
root.title("BFS Pathfinder")

canvas = tk.Canvas(root, width=500, height=500)
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


def draw_board():
    canvas.delete("all")
    for r in range(ROWS):
        for c in range(COLUMNS):
            x1, y1 = c * CELL_SIZE, r * CELL_SIZE
            canvas.create_rectangle(
                x1,
                y1,
                x1 + CELL_SIZE,
                y1 + CELL_SIZE,
                fill=COLORS[board[r][c]],
                outline="black",
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


tk.Button(root, text="Find Shortest Path", command=find_path).pack(fill="x")
tk.Button(root, text="Reset", command=reset).pack(fill="x")

draw_board()
root.mainloop()
