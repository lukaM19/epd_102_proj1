import math
import random


def get_coordinates(coords=None, n=10, width=100, height=100, seed=42):
    """Return the given list of (x, y) coordinates, or generate n random ones."""
    if coords is not None:
        return [(float(x), float(y)) for x, y in coords]
    rng = random.Random(seed)
    return [(rng.uniform(0, width), rng.uniform(0, height)) for _ in range(n)]


def read_coordinates_from_terminal():
    """Ask the user to type coordinates or generate random ones."""
    while True:
        choice = input("1) Enter coordinates  2) Generate random coordinates: ").strip()
        if choice in ("1", "2"):
            break
        print("Please enter 1 or 2.")

    if choice == "1":
        while True:
            text = input("Enter points as x,y separated by spaces (e.g. 0,0 3,4 6,1): ")
            try:
                coords = [tuple(pair.split(",")) for pair in text.split()]
                return get_coordinates(coords)
            except ValueError:
                print("Invalid format, try again.")

    while True:
        try:
            n = int(input("How many points? [10]: ") or 10)
            seed_text = input("Seed (blank for 42, 'none' for random): ").strip()
            if seed_text.lower() == "none":
                seed = None
            else:
                seed = int(seed_text or 42)
            return get_coordinates(n=n, seed=seed)
        except ValueError:
            print("Please enter whole numbers.")


def dist(a, b):
    """Euclidean distance between points a and b, each given as (x, y)."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def build_distances(coords):
    """Precompute distances between every pair of points.

    Keys are index pairs (i, j), so dists[(i, j)] is the distance from
    point i to point j. Both (i, j) and (j, i) are stored.
    """
    dists = {}
    for i in range(len(coords)):
        for j in range(i, len(coords)):
            d = dist(coords[i], coords[j])
            dists[(i, j)] = d
            dists[(j, i)] = d
    return dists

def solution(coords, dists):
    """Exact Held-Karp dynamic programming solution.

    Returns (route, length), where route is a list of point indices that
    starts and ends at point 0. Time O(n^2 * 2^n), memory O(n * 2^n).
    """
    n = len(coords)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0, 0], 0.0

    # Cities 1..n-1 are represented by bits 0..n-2 in a mask; city 0 is the start.
    m = n - 1
    full = (1 << m) - 1
    inf = float("inf")
    # cost[mask][j]: shortest path from city 0 visiting exactly the cities in
    # mask and ending at city j + 1. parent stores the previous city for backtracking.
    cost = [[inf] * m for _ in range(1 << m)]
    parent = [[-1] * m for _ in range(1 << m)]

    for j in range(m):
        cost[1 << j][j] = dists[(0, j + 1)]

    for mask in range(1, full + 1):
        for j in range(m):
            if not mask & (1 << j) or cost[mask][j] == inf:
                continue
            for k in range(m):
                if mask & (1 << k):
                    continue
                next_mask = mask | (1 << k)
                new_cost = cost[mask][j] + dists[(j + 1, k + 1)]
                if new_cost < cost[next_mask][k]:
                    cost[next_mask][k] = new_cost
                    parent[next_mask][k] = j

    best_length = inf
    last = -1
    for j in range(m):
        total = cost[full][j] + dists[(j + 1, 0)]
        if total < best_length:
            best_length = total
            last = j

    route = []
    mask = full
    while last != -1:
        route.append(last + 1)
        previous = parent[mask][last]
        mask ^= 1 << last
        last = previous
    route.reverse()
    return [0] + route + [0], best_length

def visualization(coords, route):
    pass

if __name__ == "__main__":
    points = read_coordinates_from_terminal()
    print(points)
    dists = build_distances(points)
    route, length = solution(points, dists)
    print("Route (point indices):", " -> ".join(map(str, route)))
    print("Route (coordinates):")
    for i in route:
        print(f"  {i}: ({points[i][0]:.2f}, {points[i][1]:.2f})")
    print(f"Total distance: {length:.2f}")
    # visualization(points, route)
