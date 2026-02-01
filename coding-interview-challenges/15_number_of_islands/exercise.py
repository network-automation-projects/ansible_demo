"""
Number of Islands: count connected components of '1' in 2D grid.
Time: O(m*n), Space: O(m*n) for recursion
"""


def num_islands(grid: list[list[str]]) -> int:
    """DFS from each unvisited '1'; sink the island (mark as '0')."""
    raise NotImplementedError("Implement me")


if __name__ == "__main__":
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert num_islands(grid1) == 1

    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands(grid2) == 3
    print("All examples passed.")
