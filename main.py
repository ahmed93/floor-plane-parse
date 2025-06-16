#!/usr/bin/env python3


def plan_parser(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    # loading the Room
    grid = []
    max_width = 0
    for line in lines:
        line = line.rstrip("\n")
        grid.append(list(line))
        max_width = max(max_width, len(line))

    for row in grid:
        while len(row) < max_width:
            row.append(" ")

    height = len(grid)
    width = max_width

    # Getting all rooms NAMES & The names Starting Position
    rooms = {}
    for row in range(height):
        for col in range(width):
            if grid[row][col] == "(":
                room_name = ""
                tmp_c = col + 1
                while tmp_c < width and grid[row][tmp_c] != ")":
                    room_name += grid[row][tmp_c]
                    tmp_c += 1

                if room_name:
                    rooms[room_name] = {
                        "start_row": row,
                        "start_col": col + 1,
                        "chairs": {"W": 0, "P": 0, "S": 0, "C": 0},
                    }

    # Going inside every Room to find the chairs
    for room_name, room_info in rooms.items():
        visited = [[False] * width for _ in range(height)]

        chairs_found = {"W": 0, "P": 0, "S": 0, "C": 0}

        def check_position(row, col):
            if row < 0 or row >= height or col < 0 or col >= width:
                return
            if visited[row][col]:
                return
            char = grid[row][col]
            if char in ["+", "-", "|", "/", "\\"]:
                return
            visited[row][col] = True
            if char in ["W", "P", "S", "C"]:
                chairs_found[char] += 1

            # Check Up
            check_position(row - 1, col)
            # Check Down
            check_position(row + 1, col)
            # Check Left
            check_position(row, col - 1)
            # Check Right
            check_position(row, col + 1)

        check_position(room_info["start_row"], room_info["start_col"])

        room_info["chairs"] = chairs_found

    # Cal. total Chairs
    total_chairs = {"W": 0, "P": 0, "S": 0, "C": 0}

    for room_info in rooms.values():
        for chair_type, count in room_info["chairs"].items():
            total_chairs[chair_type] += count

    # Getting data beautified for result
    output_lines = []
    output_lines.append("total:")
    output_lines.append(
        f"W: {total_chairs['W']}, P: {total_chairs['P']}, S: {total_chairs['S']}, C: {total_chairs['C']}"
    )

    sorted_room_names = sorted(rooms.keys())

    for room_name in sorted_room_names:
        chairs = rooms[room_name]["chairs"]
        output_lines.append(f"{room_name}:")
        output_lines.append(
            f"W: {chairs['W']}, P: {chairs['P']}, S: {chairs['S']}, C: {chairs['C']}"
        )

    return "\n".join(output_lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <rooms.txt>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        result = plan_parser(filename)
        print(result)
    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
