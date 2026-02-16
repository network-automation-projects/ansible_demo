"""
Python Network Automation - Objects and Dunders Exercises
=========================================================

Fill-in-the-blank exercises for learning Python special methods (dunders)
in the context of network automation.
"""

from typing import Any, Iterator, List


# ============================================================================
# EXERCISE 1: __repr__ and __str__
# ============================================================================

"""
Tutorial: __repr__ and __str__
------------------------------

__repr__(self) -> str: Called by repr(obj) and in the debugger/REPL.
  Aim for unambiguous, ideally something that looks like a constructor call.

__str__(self) -> str: Called by str(obj) and print(obj).
  Aim for human-friendly output.

In network automation:
- __repr__ helps when logging or debugging: you see Device(host='r1') not <Device ...>.
- __str__ is good for reports and user-facing messages.
"""


class Interface:
    """Represents a network interface (e.g. GigabitEthernet0/1)."""

    def __init__(self, name: str, status: str = "down") -> None:
        self.name = name
        self.status = status

    # TODO: Implement __repr__ so it returns a string like:
    #       Interface(name='GigabitEthernet0/1', status='up')
    def __repr__(self) -> str:
        return #

    # TODO: Implement __str__ so it returns a short human-readable string like:
    #       "GigabitEthernet0/1 (up)"
    def __str__(self) -> str:
        return #


# ============================================================================
# EXERCISE 2: __len__ and __getitem__
# ============================================================================

"""
Tutorial: __len__ and __getitem__
---------------------------------

__len__(self) -> int: Called by len(obj). Return the "length" of the object.

__getitem__(self, key): Called by obj[key]. Return the item at key; raise
  KeyError or IndexError if not found.

In network automation:
- A device list wrapper can support len(inventory) and inventory[0] or inventory['r1'].
"""


class InterfaceList:
    """A list of Interface objects that supports len() and indexing."""

    def __init__(self, interfaces: List[Interface]) -> None:
        self._interfaces = list(interfaces)

    # TODO: Implement __len__ so len(interface_list) returns the number of interfaces.
    

    # TODO: Implement __getitem__ so:
    #   - interface_list[0] returns the interface at index 0
    #   - interface_list['GigabitEthernet0/1'] returns the interface with that name
    #   If key is int: return self._interfaces[key]. If key is str: find by .name; else raise KeyError(key).
    
       

    # TODO (Exercise 4): Implement __iter__ so "for iface in interface_list" works.
    


# ============================================================================
# EXERCISE 3: __eq__
# ============================================================================

"""
Tutorial: __eq__
----------------

__eq__(self, other) -> bool: Called by obj == other.
  Return True if self and other are "equal" by value.
  If you don't support the comparison, return NotImplemented (let Python try other.__eq__).

In network automation:
- Two interfaces are equal if name and status match.
- Enables deduplication and "if interface in seen" checks.
"""


# Re-use Interface from Exercise 1; add __eq__ here for practice.
# (In a real codebase you'd add __eq__ on the same class.)

class InterfaceWithEq(Interface):
    """Interface with value equality: two interfaces are equal if name and status match."""

    # TODO: Implement __eq__ so two InterfaceWithEq instances are equal when
    #       self.name == other.name and self.status == other.status.
    #       If other is not an InterfaceWithEq (or Interface), return NotImplemented.
    def __eq__(self, other: Any) -> bool:
        
        return 


# ============================================================================
# EXERCISE 4: __iter__ (optional)
# ============================================================================

"""
Tutorial: __iter__
------------------

__iter__(self): Called by iter(obj) and by 'for x in obj'.
  Return an iterator (e.g. iter(self._list)) so that for x in obj works.

In network automation:
- for interface in interface_list: ...
"""


# We added __iter__ to InterfaceList above so "for iface in interface_list" works.


# ============================================================================
# Run demos (uncomment to test)
# ============================================================================

if __name__ == "__main__":
    # Exercise 1
    gi = Interface("GigabitEthernet0/1", "up")
    print("repr:", repr(gi))
    print("str:", str(gi))

    # Exercise 2
    lst = InterfaceList([gi, Interface("Gi0/2", "down")])
    print("len:", len(lst))
    print("lst[0]:", lst[0])
    print("lst['Gi0/2']:", lst["Gi0/2"])

    # Exercise 3
    a = InterfaceWithEq("Gi0/1", "up")
    b = InterfaceWithEq("Gi0/1", "up")
    c = InterfaceWithEq("Gi0/1", "down")
    print("a == b:", a == b)
    print("a == c:", a == c)

    # Exercise 4: iteration
    print("for iface in lst:")
    for iface in lst:
        print(" ", iface)
