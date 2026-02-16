# Answer: Why Status and Protocol Are Wrong for "administratively down"

## Root Cause

The parser uses **fixed column indices** after splitting the line on whitespace with `line.split()`. The IOS table has variable-width columns: "Status" can be one word (`up` / `down`) or two words (`administratively down`). For lines with "administratively down", there are two tokens for status, so the next token (the real protocol) is at index 6, not 5. Using `parts[4]` and `parts[5]` gives status=`administratively`, protocol=`down` — so status is wrong (truncated) and the second "down" (protocol) is correct only by accident for that line; for Vlan1 the same bug gives the same wrong status.

## Why It Manifests

Example line:
```
GigabitEthernet0/2     unassigned      YES unset  administratively down down
```
Split on whitespace:
- parts[0]=Interface, [1]=IP, [2]=OK?, [3]=Method, [4]=Status_first_word, [5]=Status_second_word, [6]=Protocol
So parts[4]="administratively", parts[5]="down" (second word of status), parts[6]="down" (protocol). The code assigns status=parts[4], protocol=parts[5], so protocol gets the status's second word instead of the actual protocol column.

## Code Fix

Use the fact that **status** is either one token (`up`/`down`) or two (`administratively down`), and **protocol** is always the last token. So: protocol = parts[-1]; then status = either "administratively down" if the last two tokens before protocol are "administratively" and "down", or else the single token before protocol.

A simple approach:

```python
        if len(parts) < 5:
            continue
        interface = parts[0]
        ip = parts[1]
        protocol = parts[-1]
        if len(parts) >= 6 and parts[-3] == "administratively" and parts[-2] == "down":
            status = "administratively down"
        else:
            status = parts[-2]
```

Alternatively, use a regex to capture the last two columns (status and protocol) where status may be one or two words, or parse by known column positions if the table format is fixed.

## How to Spot Similar Bugs

- **Fixed indices after split():** Any table where a column can contain spaces (e.g. "administratively down", "not set") will break. Prefer last/first token logic or regex for variable-width columns.
- **Assume one word per column:** Check sample data for multi-word values. If the device output can vary (different IOS versions), test with multiple fixtures.
- **Header vs data:** Ensure you skip the header and any separator lines; validate that the number of tokens per line matches expectations for each row type.

## Best Practices

1. **Parse from the end for variable-width columns:** Taking protocol as `parts[-1]` and status as one or two tokens before that avoids assuming a fixed number of columns before status.
2. **Use regex when structure is clear:** e.g. `r'(\S+)\s+(\S+)\s+.*\s+(\S+(?:\s+\S+)?)\s+(\S+)$'` to capture interface, IP, status (one or two words), protocol. Named groups improve readability.
3. **Handle edge cases:** Empty lines, different header formats, "unassigned" vs IP. Use a small set of fixture files that cover "up", "down", and "administratively down".
4. **Structured output:** Prefer NAPALM/getters or TextFSM when available so the device returns structured data instead of hand-parsing CLI tables.
