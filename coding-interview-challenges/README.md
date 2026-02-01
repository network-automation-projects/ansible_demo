# Coding Interview Challenges

20 of the most commonly asked coding interview problems, with problem statements, Python solutions, and runnable examples. Use this folder to review and re-run solutions before interviews.

**Python 3.9+.** Style: Black, type hints, docstrings with time/space complexity.

For **practical scripting tasks** (no CS prerequisites), see [Practical / scripting challenges](#practical--scripting-challenges).

## Index

| # | Problem | Category | Difficulty | Path |
|---|---------|----------|------------|------|
| 1 | Two Sum | Array / Hash | Easy | [01_two_sum/](01_two_sum/) |
| 2 | Valid Parentheses | Stack | Easy | [02_valid_parentheses/](02_valid_parentheses/) |
| 3 | Merge Two Sorted Lists | Linked List | Easy | [03_merge_two_sorted_lists/](03_merge_two_sorted_lists/) |
| 4 | Best Time to Buy and Sell Stock | Array / DP | Easy | [04_best_time_buy_sell_stock/](04_best_time_buy_sell_stock/) |
| 5 | Valid Palindrome | String / Two pointers | Easy | [05_valid_palindrome/](05_valid_palindrome/) |
| 6 | Valid Anagram | String / Hash | Easy | [06_valid_anagram/](06_valid_anagram/) |
| 7 | Binary Search | Binary Search | Easy | [07_binary_search/](07_binary_search/) |
| 8 | Maximum Subarray (Kadane) | Array / DP | Medium | [08_maximum_subarray/](08_maximum_subarray/) |
| 9 | Reverse Linked List | Linked List | Easy | [09_reverse_linked_list/](09_reverse_linked_list/) |
| 10 | Contains Duplicate | Array / Hash | Easy | [10_contains_duplicate/](10_contains_duplicate/) |
| 11 | Missing Number | Array / Math | Easy | [11_missing_number/](11_missing_number/) |
| 12 | Longest Substring Without Repeating Characters | String / Sliding window | Medium | [12_longest_substring_no_repeat/](12_longest_substring_no_repeat/) |
| 13 | 3Sum | Array / Two pointers | Medium | [13_3sum/](13_3sum/) |
| 14 | Merge Intervals | Intervals | Medium | [14_merge_intervals/](14_merge_intervals/) |
| 15 | Number of Islands | Graph / DFS-BFS | Medium | [15_number_of_islands/](15_number_of_islands/) |
| 16 | Product of Array Except Self | Array | Medium | [16_product_of_array_except_self/](16_product_of_array_except_self/) |
| 17 | Maximum Depth of Binary Tree | Tree | Easy | [17_maximum_depth_binary_tree/](17_maximum_depth_binary_tree/) |
| 18 | Climbing Stairs | DP | Easy | [18_climbing_stairs/](18_climbing_stairs/) |
| 19 | Reverse Integer | Math | Medium | [19_reverse_integer/](19_reverse_integer/) |
| 20 | Invert Binary Tree | Tree | Easy | [20_invert_binary_tree/](20_invert_binary_tree/) |

## How to use

1. Open a challenge folder (e.g. `01_two_sum/`).
2. Read `README.md` for the problem statement, examples, and constraints.
3. Implement the solution in `exercise.py` (stub with signature and tests provided; run `python exercise.py` to check).
4. Optionally compare with `solution.py` after.
5. Repeat for each challenge as needed.

No external dependencies required for the algorithms (stdlib only).

## Automation-style practice

For **network reliability / automation** interviews (e.g. one code challenge focused on scripting):

- **[automation_practice/](automation_practice/)** – Read a device list from file (txt or JSON), filter by role, call a fake "API" for status, build a report. Uses: `open`, `json`, dicts/lists, error handling. Do `exercise.py` first (fill in TODOs), then compare with `solution.py`.

## Practical / scripting challenges

These are for **practical / automation-style** interviews. No computer-science prerequisites—just file I/O, parsing, dicts/lists, and error handling. Same format: read the README, implement `exercise.py`, then compare with `solution.py`.

| Challenge | Description | Path |
|-----------|-------------|------|
| Device list + API report | Read devices from file, filter by role, fake API, build report. | [automation_practice/](automation_practice/) |
| Log parser | Read a log file, extract level/timestamp/message, filter by level, count errors. | [practical_log_parser/](practical_log_parser/) |
| Env parser | Parse a `.env`-style file into a dict; skip comments and blanks; handle bad lines. | [practical_env_parser/](practical_env_parser/) |
| CSV transform | Read CSV, filter rows, add computed column, write new CSV. | [practical_csv_transform/](practical_csv_transform/) |
| Config merge | Read two key=value configs; merge (second file wins) or diff keys. | [practical_config_merge/](practical_config_merge/) |
| Retry with backoff | Wrap a flaky function in retry logic with exponential backoff. | [practical_retry_backoff/](practical_retry_backoff/) |
| NRE core patterns | Dict grouping, validation, set diff, config drift, batch partial failure. | [nre_core_patterns/](nre_core_patterns/) |
| Ansible playbook driver | Run ansible-playbook from Python, parse play recap. | [ansible_playbook_driver/](ansible_playbook_driver/) |
| Ansible playbook parser | Load playbook/inventory YAML, list plays, tasks, hosts. | [ansible_playbook_parser/](ansible_playbook_parser/) |
| Jira search parser | Parse Jira search response JSON; group by status/assignee; sum story points. | [jira_search_parser/](jira_search_parser/) |
| Jira sprint report | Produce sprint summary: velocity, by-status counts, total points. | [jira_sprint_report/](jira_sprint_report/) |
| Prometheus metrics exposition | Expose Counter/Gauge/Histogram, generate /metrics, parse exposition format. | [prometheus_metrics_exposition/](prometheus_metrics_exposition/) |
| Prometheus query client | Query /api/v1/query, parse JSON result (metric name, labels, value). | [prometheus_query_client/](prometheus_query_client/) |
| Grafana dashboard PromQL parser | Extract panel titles and PromQL expressions from dashboard JSON. | [grafana_dashboard_promql/](grafana_dashboard_promql/) |
