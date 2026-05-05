from typing import List, Tuple, Dict
import numpy as np
import heapq
import matplotlib.pyplot as plt


Position = Tuple[int, int]


def create_node(position: Position, g: float, h: float, parent=None) -> Dict:
    return {
        "position": position,
        "g": g,
        "h": h,
        "f": g + h,
        "parent": parent
    }


def calculate_heuristic(pos1: Position, pos2: Position) -> float:
    """
    Dùng khoảng cách Manhattan vì robot chỉ đi 4 hướng:
    lên, xuống, trái, phải.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def get_cell_cost(cell_value: int) -> int:
    """
    Quy định chi phí đi vào từng loại ô:
    0: ô trống, chi phí 1
    2: bùn lầy, chi phí 3
    3: đá, chi phí 5
    1: vật cản, không đi được
    """
    if cell_value == 0:
        return 1
    elif cell_value == 2:
        return 3
    elif cell_value == 3:
        return 5
    else:
        return 999999


def get_valid_neighbors(grid: np.ndarray, position: Position) -> List[Position]:
    x, y = position
    rows, cols = grid.shape

    # Chỉ đi 4 hướng, không đi chéo
    possible_moves = [
        (x - 1, y),  # lên
        (x + 1, y),  # xuống
        (x, y - 1),  # trái
        (x, y + 1)   # phải
    ]

    valid_neighbors = []

    for nx, ny in possible_moves:
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] != 1:  # khác 1 nghĩa là không phải vật cản
                valid_neighbors.append((nx, ny))

    return valid_neighbors


def reconstruct_path(goal_node: Dict) -> List[Position]:
    path = []
    current = goal_node

    while current is not None:
        path.append(current["position"])
        current = current["parent"]

    return path[::-1]


def find_path(grid: np.ndarray, start: Position, goal: Position) -> List[Position]:
    start_node = create_node(
        position=start,
        g=0,
        h=calculate_heuristic(start, goal),
        parent=None
    )

    open_list = []
    heapq.heappush(open_list, (start_node["f"], start))

    open_dict = {start: start_node}
    closed_set = set()

    while open_list:
        _, current_pos = heapq.heappop(open_list)

        if current_pos in closed_set:
            continue

        current_node = open_dict[current_pos]

        if current_pos == goal:
            return reconstruct_path(current_node)

        closed_set.add(current_pos)

        for neighbor_pos in get_valid_neighbors(grid, current_pos):
            if neighbor_pos in closed_set:
                continue

            nx, ny = neighbor_pos
            move_cost = get_cell_cost(grid[nx][ny])

            tentative_g = current_node["g"] + move_cost

            if neighbor_pos not in open_dict or tentative_g < open_dict[neighbor_pos]["g"]:
                neighbor_node = create_node(
                    position=neighbor_pos,
                    g=tentative_g,
                    h=calculate_heuristic(neighbor_pos, goal),
                    parent=current_node
                )

                open_dict[neighbor_pos] = neighbor_node
                heapq.heappush(open_list, (neighbor_node["f"], neighbor_pos))

    return []


def calculate_total_cost(grid: np.ndarray, path: List[Position]) -> int:
    if not path:
        return 0

    total_cost = 0

    # Bỏ qua ô start, chỉ tính chi phí khi đi vào các ô sau
    for x, y in path[1:]:
        total_cost += get_cell_cost(grid[x][y])

    return total_cost


def visualize_path(grid: np.ndarray, path: List[Position]) -> None:
    grid_copy = np.copy(grid).astype(str)

    for x, y in path:
        grid_copy[x][y] = "*"

    if path:
        sx, sy = path[0]
        gx, gy = path[-1]
        grid_copy[sx][sy] = "S"
        grid_copy[gx][gy] = "G"

    print("\nBản đồ đường đi:")
    for row in grid_copy:
        print(" ".join(row))


def plot_grid(grid: np.ndarray, path: List[Position]) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))

    ax.imshow(grid, cmap="Greys", interpolation="none")

    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]

        ax.plot(path_x, path_y, marker="o", linewidth=2, label="Path")

        start = path[0]
        goal = path[-1]

        ax.plot(start[1], start[0], marker="s", markersize=10, label="Start")
        ax.plot(goal[1], goal[0], marker="s", markersize=10, label="Goal")

    ax.set_title("Duong di toi uu bang thuat toan A*")
    ax.legend()
    ax.grid(True)
    plt.show()


def main():
    # Tạo lưới 20x20
    grid = np.zeros((20, 20), dtype=int)

    # Thêm vật cản
    grid[5:15, 10] = 1
    grid[5, 5:15] = 1

    # Thêm bùn lầy
    grid[3:8, 3] = 2
    grid[10:15, 7] = 2
    grid[12, 12:17] = 2

    # Thêm đá
    grid[8:12, 13] = 3
    grid[15, 4:10] = 3
    grid[16:19, 15] = 3

    start_pos = (2, 2)
    goal_pos = (18, 18)

    path = find_path(grid, start_pos, goal_pos)

    if path:
        total_cost = calculate_total_cost(grid, path)

        print("Tìm thấy đường đi!")
        print("Số ô trong đường đi:", len(path))
        print("Tổng chi phí:", total_cost)
        print("Đường đi:", path)

        visualize_path(grid, path)
        plot_grid(grid, path)
    else:
        print("Không tìm thấy đường đi!")


if __name__ == "__main__":
    main()