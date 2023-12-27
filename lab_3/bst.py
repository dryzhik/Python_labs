class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if key < root.val:
                root.left = self._insert(root.left, key)
            elif key > root.val:
                root.right = self._insert(root.right, key)
        return root

    def __iter__(self):
        return self._inorder_generator(self.root)

    def _inorder_generator(self, node):
        if node:
            yield from self._inorder_generator(node.left)
            yield node.val
            yield from self._inorder_generator(node.right)


if __name__ == "__main__":
    bst = BinarySearchTree()
    values = [1, 1, 1, 2, 56, 789, 32, 643, 66, 3, 66, 6, 6, 6, 6, 7]

    for value in values:
        bst.insert(value)

    for element in bst:
        print(element)
