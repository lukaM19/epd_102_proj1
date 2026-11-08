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


def solution(coords):
    pass


def visualization(coords, route):
    pass


if __name__ == "__main__":
    points = read_coordinates_from_terminal()
    print(points)
    route = solution(points)
    visualization(points, route)
