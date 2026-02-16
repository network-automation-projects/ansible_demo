# Module 06b: Pattern Detection Tools

**Goal:** Learn how to **choose and derive** parsing patterns on your own so you can handle code challenges and real device output without memorizing tools.

## Learning Objectives

- Decide when to use **regex**, **line/column parsing**, or **template-based** approaches
- Follow a repeatable process to design a pattern from sample output
- Handle edge cases (missing data, malformed lines, multiple formats)
- Know where **TextFSM**, **TTP**, and **Genie** fit (and when to reach for them)

## Prerequisites

- Module 06: Configuration Management (regex basics, `re.findall`, `re.search`)
- Module 01: Core Fundamentals (strings, loops, dicts)

## How to Come Up With Patterns on Your Own

### Step 1: Inspect the output shape

Before writing any pattern, look at the **actual output**:

- **Key-value lines** (e.g. `hostname R1`, `uptime is 5 weeks`) → capture with regex groups or `split()`
- **Tables** (header + rows with columns) → split by whitespace or fixed columns; skip header
- **Blocks** (sections separated by blank lines or headers) → split into blocks, then parse each
- **Mixed** → combine: e.g. parse key-value for metadata, then table for interfaces

### Step 2: Choose your approach

| Output type              | Good approach              | Why |
|--------------------------|----------------------------|-----|
| Single values (IP, version) | Regex with groups          | One-off; `re.search(r'Version (\S+)', text)` |
| Repeated tokens (all IPs)   | `re.findall()`             | Extract every match |
| Line-based key-value        | Loop + `re.match` or `split()` | One pattern per line |
| Table (show ip int brief)   | Split lines, then split columns (or regex per row) | Predictable columns |
| Complex / multi-vendor      | Template (TextFSM, TTP) or structured API | Reusable, maintainable |

### Step 3: Write the minimal pattern

- Start with a **small sample** (3–5 lines or one block).
- Get **one** field working, then add the next.
- Use **named groups** when helpful: `(?P<version>\S+)` so intent is clear.
- Prefer **non-greedy** where needed: `.*?` instead of `.*` to avoid over-matching.

### Step 4: Handle edge cases

- Missing field → use `m.group('name', 'Unknown')` or `.get(key, 'Unknown')`
- Malformed line → skip or append to an `errors` list; don’t crash
- Empty input → return `[]` or `{}` early
- Multiple formats (e.g. different IOS versions) → try one pattern, fall back to another, or normalize in one regex

## Tools Beyond Standard Library

- **TextFSM** – Template file per command; Netmiko can use it via `use_textfsm=True` with **ntc-templates**.
- **TTP** – YAML templates for parsing; good for custom or multi-vendor output.
- **Genie (pyats)** – Cisco-focused; parses many `show` commands into Python dicts.
- **NAPALM** – For supported getters, returns structured data; no parsing needed.

In an interview, you’ll usually use **regex + line/column parsing** (stdlib only). Knowing when you’d use templates or APIs shows you understand the tradeoffs.

## Files in This Module

- **README.md** (this file) – Learning objectives and decision framework
- **LESSON_derive_patterns.md** – Detailed “derive it yourself” workflow with examples
- **examples.py** – Worked examples with step-by-step thought process
- **exercises.py** – Interview-style parsing tasks (fill in or implement)
- **exercises_answers.py** – Reference solutions

## Interview Tips

1. **Clarify input:** “Single device output or multiple? Any guaranteed format?”
2. **State your approach:** “This looks like key-value lines, so I’ll loop and use a regex per line.”
3. **Start simple:** One field first, then expand.
4. **Mention edge cases:** “I’ll return a default for missing hostname and skip malformed lines.”
5. **Test with the sample:** Run your code against the given snippet before saying “done.”

## Concepts Covered

- `re.search`, `re.findall`, `re.match` with groups and named groups
- Line-by-line parsing with `split()` and `strip()`
- Table parsing (header skip, column split)
- Defensive parsing (skip bad lines, defaults for missing fields)

## Use Cases

- Parsing `show version`, `show ip interface brief`, log files
- Extracting IPs, interface names, versions from unstructured text
- Code challenge / take-home style tasks
