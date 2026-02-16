# How to Derive Parsing Patterns on Your Own

This lesson walks through **how to think** when you see a parsing problem (e.g. in an interview or on the job), so you can come up with the pattern yourself instead of guessing.

---

## 1. Read the problem and get a sample

- You’re usually asked to “parse X” or “extract Y from this output.”
- Get **real or sample output** in front of you. If the problem only describes it, ask: “Do you have a sample I can use?” or invent a minimal one.

Example prompt: *“Parse this log line and return timestamp, level, and message.”*

Sample line:
```
2025-02-05 14:30:00 ERROR Connection refused to 10.0.0.1
```

---

## 2. Name the shape of the data

In one sentence, describe **how** the data is laid out:

- “A single line with timestamp, then level, then the rest is the message.”
- “A table: header line, then rows with columns separated by whitespace.”
- “Key-value pairs, one per line, like `key value` or `key: value`.”
- “One block per section, with a header line and then indented or fixed-format lines.”

For the log line above: **one line, fixed order – timestamp, level, rest is message.**

---

## 3. Choose extraction method from the shape

Use this as a mental checklist:

- **Single line, fixed order** → split once (e.g. on first two spaces or on “ LEVEL ”), or one regex with groups.
- **Same pattern repeated (e.g. all IPs)** → `re.findall()` with one capturing group.
- **One value per line, key-value** → loop lines; for each line use regex or split to get key and value.
- **Table** → split into lines, skip header (or detect it), then split each line (by whitespace or regex) into columns.
- **Nested / block structure** → split into blocks (e.g. blank-line separated), then parse each block with the same logic.

For the log line: **single line, fixed order** → split on first two spaces, or regex with three groups.

---

## 4. Write the smallest pattern that works

- Don’t try to parse the whole output at once. Get **one field** right, then add the next.
- Prefer **one clear pattern** per “thing” (one per line, or one per row). Combine later.

Example for the log line:

- Field 1 – timestamp: “digits and dashes, then space, then digits and colons”  
  → `(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})`
- Field 2 – level: “word in caps”  
  → `(INFO|ERROR|WARN|DEBUG)`
- Field 3 – message: “everything after the level”  
  → `(.+)` or `(.*)` and strip

Full regex:  
`r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|ERROR|WARN|DEBUG) (.+)'`

Or with **named groups** (better for readability and maintenance):  
`r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>INFO|ERROR|WARN|DEBUG) (?P<message>.+)'`

---

## 5. Code the parser and handle edges

- Use the pattern in `re.match()` (line start) or `re.search()` (anywhere).
- Return a dict or dataclass with the groups.
- **Edge cases:**
  - Line doesn’t match → skip or return `None` / “UNKNOWN” for that line.
  - Missing optional field → `.get('key', 'Unknown')` or default in the regex.
  - Empty input → return `[]` or `{}` and exit early.

---

## 6. Practice on these shapes (interview-style)

So you can “come up with it on your own,” practice naming the shape and choosing the method for:

| Sample output type              | Shape name              | Method to use                    |
|---------------------------------|-------------------------|----------------------------------|
| `hostname R1` / `uptime 5 weeks`| Key-value per line      | Loop; regex or split per line    |
| `10.0.0.1 10.0.0.2 10.0.0.3`    | Repeated token          | `re.findall(r'…', text)`         |
| Table with header + rows        | Table                   | Split lines; skip header; split columns |
| `Interface Gi0/0 10.0.0.1 up`   | Fixed columns per line  | Split by whitespace; index columns     |
| JSON or XML                     | Structured              | `json.loads` / XML parser, not regex   |

Once you can **name the shape** and **choose the method**, writing the actual regex or split logic is the last step.

---

## 7. Summary: repeatable process

1. Get sample output.
2. Name the shape (line-based, table, key-value, repeated token, etc.).
3. Choose method from the shape (regex groups, findall, line loop + split, table split).
4. Write the smallest pattern for one field, then extend.
5. Add edge-case handling (no match, missing field, empty input).
6. Test on the given sample and one edge case.

Using this process in an interview shows you’re not just “writing regex” but **designing** a parser from the structure of the data.
