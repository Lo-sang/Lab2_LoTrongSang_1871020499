from typing import Tuple, List
import heapq
import numpy as np
import matplotlib.pyplot as plt

Point = Tuple[int, int]

# Chi phí đi vào từng loại ô
MOVE_COST = {
    0: 1,   # đường thường
    2: 3,   # bùn
    3: 5    # đá
}


def manhattan(current: Point, target: Point) -> int:
    """Tính khoảng cách Manhattan từ ô hiện tại tới đích."""
    return abs(current[0] - target[0]) + abs(current[1] - target[1])


def terrain_cost(value: int) -> int:
    """Lấy chi phí tương ứng với loại địa hình."""
    return MOVE_COST.get(value, 999999)


def get_neighbors(warehouse: np.ndarray, cell: Point) -> List[Point]:
    """Trả về các ô kề có thể đi được theo 4 hướng."""
    row, col = cell
    max_row, max_col = warehouse.shape

    directions = [
        (-1, 0),  # lên
        (1, 0),   # xuống
        (0, -1),  # trái
        (0, 1)    # phải
    ]

    result = []

    for dr, dc in directions:
        nr = row + dr
        nc = col + dc

        inside_map = 0 <= nr < max_row and 0 <= nc < max_col
        if inside_map and warehouse[nr][nc] != 1:
            result.append((nr, nc))

    return result


def build_path(parent: dict, start: Point, goal: Point) -> List[Point]:
    """Dựng lại đường đi từ goal về start."""
    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path


def astar_search(warehouse: np.ndarray, start: Point, goal: Point) -> List[Point]:
    """
    Tìm đường đi có tổng chi phí nhỏ nhất bằng thuật toán A*.
    """
    open_queue = []
    heapq.heappush(open_queue, (0, start))

    parent = {}
    g_score = {start: 0}
    visited = set()

    while open_queue:
        _, current = heapq.heappop(open_queue)

        if current in visited:
            continue

        if current == goal:
            return build_path(parent, start, goal)

        visited.add(current)

        for next_cell in get_neighbors(warehouse, current):
            if next_cell in visited:
                continue

            r, c = next_cell
            new_cost = g_score[current] + terrain_cost(warehouse[r][c])

            if next_cell not in g_score or new_cost < g_score[next_cell]:
                g_score[next_cell] = new_cost
                parent[next_cell] = current

                f_score = new_cost + manhattan(next_cell, goal)
                heapq.heappush(open_queue, (f_score, next_cell))

    return []


def path_cost(warehouse: np.ndarray, path: List[Point]) -> int:
    """Tính tổng chi phí của đường đi."""
    total = 0

    for r, c in path[1:]:
        total += terrain_cost(warehouse[r][c])

    return total


def print_map(warehouse: np.ndarray, path: List[Point], start: Point, goal: Point) -> None:
    """In bản đồ ra màn hình console."""
    display = warehouse.astype(str)

    for r, c in path:
        display[r][c] = "*"

    display[start[0]][start[1]] = "S"
    display[goal[0]][goal[1]] = "G"

    print("\n===== BAN DO KHO HANG =====")
    for row in display:
        print(" ".join(row))


def draw_result(warehouse: np.ndarray, path: List[Point], start: Point, goal: Point) -> None:
    """Vẽ bản đồ và đường đi bằng matplotlib."""
    plt.figure(figsize=(7, 7))
    plt.imshow(warehouse, cmap="gray_r")

    if path:
        x = [p[1] for p in path]
        y = [p[0] for p in path]
        plt.plot(x, y, marker="o", linewidth=2, label="Duong di")

    plt.scatter(start[1], start[0], marker="s", s=120, label="Start")
    plt.scatter(goal[1], goal[0], marker="s", s=120, label="Goal")

    plt.title("Tim duong cho robot bang thuat toan A*")
    plt.legend()
    plt.grid(True)
    plt.show()


def create_warehouse() -> np.ndarray:
    """Tạo bản đồ kho hàng riêng."""
    warehouse = np.zeros((20, 20), dtype=int)

    # Vật cản
    warehouse[4:16, 8] = 1
    warehouse[10, 3:13] = 1
    warehouse[2:9, 15] = 1

    # Bùn lầy
    warehouse[3:7, 4] = 2
    warehouse[12:18, 6] = 2
    warehouse[6, 10:14] = 2

    # Đá
    warehouse[14, 10:17] = 3
    warehouse[7:12, 17] = 3
    warehouse[16:19, 12] = 3

    return warehouse


def main():
    warehouse = create_warehouse()

    start = (1, 1)
    goal = (18, 18)

    path = astar_search(warehouse, start, goal)

    if not path:
        print("Khong tim thay duong di phu hop!")
        return

    total = path_cost(warehouse, path)

    print("Da tim thay duong di bang A*")
    print("So o di qua:", len(path))
    print("Tong chi phi:", total)
    print("Duong di:", path)

    print_map(warehouse, path, start, goal)
    draw_result(warehouse, path, start, goal)


if __name__ == "__main__":
    main()