"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import Any, Iterator, List


class Interface:
    """Represents a network interface (e.g. GigabitEthernet0/1)."""

    def __init__(self, name: str, status: str = "down") -> None:
        self.name = name
        self.status = status

    def __repr__(self) -> str:
        return f"Interface(name={self.name!r}, status={self.status!r})"  # why !r

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"


class InterfaceList:
    """A list of Interface objects that supports len() and indexing."""

    def __init__(self, interfaces: List[Interface]) -> None:
        self._interfaces = list(interfaces)

    def __len__(self) -> int:
        return len(self._interfaces)

# Based on these inputs:
#     lst = InterfaceList([gi, Interface("Gi0/2", "down")]) #gi is the first interface, "Gi0/2" is the second interface
#     print("len:", len(lst))                               #len(lst) returns the number of interfaces in the list
#     print("lst[0]:", lst[0])                              #lst[0] returns the first interface in the list
#     print("lst['Gi0/2']:", lst["Gi0/2"])                  #lst["Gi0/2"] returns the second interface in the list by name

# we should see these outputs:
#     len: 2
#     lst[0]: GigabitEthernet0/1 (up)
#     lst['Gi0/2']: Gi0/2 (down)


    # TODO: Implement __getitem__ so:
    #   - interface_list[0] returns the interface at index 0
    #   - interface_list['GigabitEthernet0/1'] returns the interface with that name
    #   If key is int: return self._interfaces[key]. If key is str: find by .name; else raise KeyError(key).


    def __getitem__(self, key: Any) -> Interface:
        if isinstance(key, int):            # if calling function specifies an int
            return self._interfaces[key]    # this returns the interface associated with that position (if they entered an integer, they are looking for the function to use that integer positionally to grab and return that interface)
        for iface in self._interfaces:      # otherwise, we know they provided an interface name and we are going to loop through the interfaces looking for a name that matches that key
            if iface.name == key:
                return iface                # return the interface
        raise KeyError(key)                 # we didn't find either.

    def __iter__(self) -> Iterator[Interface]:
        return iter(self._interfaces)


class InterfaceWithEq(Interface):
    """Interface with value equality: two interfaces are equal if name and status match."""

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Interface):        # so if the incoming variable is not an interface return not implemented
            return NotImplemented
        return self.name == other.name and self.status == other.status  #if it is an interface, check if the name and status are equal, only return true is they are both equal


if __name__ == "__main__":
    print("02b_objects_and_dunders – answer key (run exercises.py to practice)")
