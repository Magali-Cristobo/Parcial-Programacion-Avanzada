
import random
import time
from typing import Any, Optional

# 1
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self, root):
        self.root = Node(root)

    def insert(self, value: Any) -> Node:
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return current.left
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return current.right
                current = current.right
            else:
                return current

    def search(self, value): 
        current = self.root
        while current is not None:
            if value == current.value:
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return None

# 3 con recursion
def height(node: Node) -> int:
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


# 3 de forma iterativa
def height2(root: Node) -> int:
    if root is None:
        return -1

    stack = [(root, 0)]
    max_height = 0

    while stack:
        node, current_height = stack.pop()
        max_height = max(max_height, current_height)

        if node.left:
            stack.append((node.left, current_height + 1))
        if node.right:
            stack.append((node.right, current_height + 1))

    return max_height

def printTree(node: Node, prefix: str = "", is_left: bool = True) -> None:
    if node is not None:
        print(prefix + ("├── " if is_left else "└── ") + str(node.value))
        printTree(node.left, prefix + ("│   " if is_left else "    "), True)
        printTree(node.right, prefix + ("│   " if is_left else "    "), False)

# 2 y 5
def generarDatos(size: int, ordered = False) -> BinaryTree:
    data = random.sample(range(1, size * 10 + 1), size)
    duplicate = random.choice(data)
    print("elemento repetido ", duplicate)
    insert_pos = random.randint(0, len(data))
    data.insert(insert_pos, duplicate)
    if ordered:
        data.sort()

    tree = BinaryTree(data[0])
    for number in data[1:]:
        tree.insert(number)

    return tree




def main() -> None:
    # bt = BinaryTree(7)
    # # bt.root.left = Node(5)
    # # bt.root.right = Node(8)
    # # bt.root.left.left = Node(4)
    # # bt.root.left.right = Node(6)
    # bt.insert(8)
    # bt.insert(5)
    # bst = generarDatos(20000)
    bst = generarDatos(20000, True)
    # printTree(bst.root)
    # altura = height2(bst.root)
    print("elemento encontrado ",bst.search(20001))
    # print(altura)

if __name__ == "__main__":
    main()
