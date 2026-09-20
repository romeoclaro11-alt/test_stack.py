"""ITECC04 Laboratory 4, Part A2: the linked-list-based stack.

Same public interface as ArrayStack. Different storage, same contract. That
is the point of the exercise: code that uses a stack should not be able to
tell which one it was handed.

The HEAD of the list is the top. Pushing means making a new node whose next
is the old top. Popping means moving the head forward one node. Neither walks
the list, so both are O(1), the same as the array version.

You wrote Node in Chapter 3. This one is given so you can spend the time on
the stack itself.
"""


class Node:
    """Written for you."""
    __slots__ = ("value", "next")
    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt

class LinkedStack:
    def __init__(self):
        """Step 1. An empty stack has no top node and holds no items."""
        self._top = None
        self._size = 0

    def push(self, item):
        """Step 2. New node on the front, then update the count."""
        self._top = Node(item, self._top)
        self._size += 1

    def pop(self):
        """Step 3. Remove and return the value at the top."""
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.value

    def peek(self):
        """Step 4. Return the top value without unlinking anything."""
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self._top.value

    def is_empty(self):
        """Step 5. True when there is no top node."""
        return self._top is None

    def size(self):
        """Step 6. Return the running count, not a walk of the list."""
        return self._size

    def __len__(self):
        """Written for you."""
        return self.size()
