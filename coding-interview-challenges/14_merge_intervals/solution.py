"""
Merge Intervals: merge all overlapping intervals.
Time: O(n log n), Space: O(n) for output
"""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Sort by start; merge if current.start <= last.end."""
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    out: list[list[int]] = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out


if __name__ == "__main__":
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6],
        [8, 10],
        [15, 18],
    ]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([[1, 4], [0, 4]]) == [[0, 4]]
    print("All examples passed.")
