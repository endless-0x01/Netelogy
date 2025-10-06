from unittest import result


class Stack:

    def __init__(self) -> None:
        self.data = []

    def is_empty(self) -> bool:
        return len(self.data) == 0

    def push(self, object):
        self.data.append(object)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack empty")
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.data[-1]

    def size(self):
        return len(self.data)


def is_balanced(brackets_string):
    stack = Stack()

    brackets_map = {")": "(", "]": "[", "}": "{"}

    for char in brackets_string:
        if char in "([{":
            stack.push(char)
        elif char in ")]}":
            if stack.is_empty():
                return "Несбалансированно"
            last_opening = stack.pop()
            if brackets_map[char] != last_opening:
                return "Несбалансированно"

    if stack.is_empty():
        return "Сбалансированно"
    else:
        return "Несбалансированно"


def main():
    test_cases = [
        "(((([{}]))))",
        "[([])((([[[]]])))]{()}",
        "{{[()]}}",
        "}{}",
        "{{[(])]}}",
        "[[{())}]",
    ]

    for test in test_cases:
        result = is_balanced(test)
        print(f"'{test}' → {result}")

if __name__ == '__main__':
    main()