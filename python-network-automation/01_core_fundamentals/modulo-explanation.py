'''Why device_id % num_workers == worker_id?
This is deterministic sharding: dividing devices among workers so that:
Each device is handled by exactly one worker.
The assignment is repeatable (same device → same worker every time).
No shared state or coordination is needed.
How modulo does that
device_id % num_workers is in the range 0 .. num_workers - 1, so it acts like a “bucket” index.
You want worker worker_id to own the bucket where that index equals worker_id.
So the condition is: “this device’s bucket is my worker id” →
device_id % num_workers == worker_id.
Example (num_workers = 4):
device_id	device_id % 4	owner worker_id
0	0	0
1	1	1
2	2	2
3	3	3
4	0	0
5	1	1
6	2	2
7	3	3
So worker 0 gets 0, 4, 8, …; worker 1 gets 1, 5, 9, …; etc. That’s what the docstring means by “Worker 0 gets devices 0, num_workers, 2num_workers, …”.
Task in plain words
The task is: decide whether this worker should process this device in a sharded setup. The rule is: “this worker processes the device if the device’s id, when divided by the number of workers, leaves a remainder equal to this worker’s id.” That’s exactly device_id % num_workers == worker_id.
Suggested prompt changes
You asked to change the prompts so the task is clearer. Here’s concrete text you can use (I’m in Ask mode so I can’t edit the file for you; you can paste these in or switch to Agent mode and ask me to apply them).
1. Docstring – first paragraph (what the function is for):
Replace the current opening with something like:
Return True if this worker should process this device when work is split acrossnum_workers (deterministic sharding). Each device is assigned to exactly oneworker by the rule: device_id % num_workers gives a bucket 0..num_workers-1;this worker should process the device only when that bucket equals worker_id.
2. “Returns” section:
Replace the one-line Returns with:
Returns:    True if this worker owns this device under the modulo rule above; otherwise False.
3. TODO comment:
Replace the TODO with something that states the task, not the answer:
# TODO: Return True when this worker_id is the one that "owns" device_id#       (same rule as device_id % num_workers == worker_id).
Or, if you want to avoid giving the formula away:
# TODO: Return True iff this device is assigned to this worker when#       devices are split by remainder of device_id divided by num_workers.
Summary: device_id % num_workers == worker_id is the condition for “this worker should process this device” in a deterministic, modulo-based shard. The suggested prompt changes describe that task (who owns which device) so the exercise is clear; the implementation is still the same one expression. If you want these edits applied directly in exercises.py, switch to Agent mode and ask to update the docstring and TODO for device_belongs_to_worker.'''



def device_belongs_to_worker(
    device_id: int, worker_id: int, num_workers: int
) -> bool:
    """
    Return True if this worker should process this device (deterministic sharding).

    Worker 0 gets devices 0, num_workers, 2*num_workers, ...
    Worker 1 gets 1, num_workers+1, ...
    No coordination or shared state needed.

    Args:
        device_id: Integer device id (e.g. from enumerate or DB id)
        worker_id: This worker's id (0 to num_workers - 1)
        num_workers: Total number of workers

    Returns:
        True if device_id % num_workers == worker_id

    Example:
        >>> device_belongs_to_worker(6, 2, 4)
        True
        >>> device_belongs_to_worker(5, 2, 4)
        False
    """
    # TODO: Fill in the blank - use device_id % num_workers == worker_id
    return False  # replace with modulo expression

