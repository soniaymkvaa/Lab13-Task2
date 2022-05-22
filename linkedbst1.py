"""
File: linkedbst.py
Author: Ken Lambert
"""

import math
import random
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log2
import time
import sys

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None


    def find_no_rec(self,item):
        node = self._root
        while node != None:
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

        return False

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add_no_recursion(self, item):

        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return

        curr_node = self._root
        while True:
            if item < curr_node.data:
                if curr_node.left == None:
                    curr_node.left = BSTNode(item)
                    return
                else:
                    curr_node = curr_node.left
            elif curr_node.right == None:
                curr_node.right = BSTNode(item)
                return
            else:
                curr_node = curr_node.right


    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1

            left_child = top.left
            right_child = top.right
            cur_height = max(height1(left_child), height1(right_child))+1
            return cur_height

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height()== math.ceil(log2(self._size+1)) -1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        items = []
        for sth in self:
            items.append(sth)
        index_1 = items.index(low)
        index_2 = items.index(high)
        return items[index_1:index_2]


    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def small_rebalance(arr):
            if len(arr) == 1:
                return BSTNode(arr[0])
            if len(arr) < 1:
                return None
            mid_ind = len(arr)//2
            root = BSTNode(arr[mid_ind])
            root.left = small_rebalance(arr[0:mid_ind])
            root.right = small_rebalance(arr[mid_ind+1:])
            return root

        arr_sorted = list(self.inorder())
        root_balanced = small_rebalance(arr_sorted)
        self._root = root_balanced


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        curr = self._root

        while curr is not None:
            if item < curr.data:
                item_last = curr.data
                curr = curr.left
            else:
                curr =curr.right

        try:
            if item_last is not None and item_last>item:
                return item_last
            else:
                return None
        except UnboundLocalError:
            return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        curr = self._root

        while curr is not None:
            if item > curr.data:
                item_last = curr.data
                curr = curr.right
            else:
                curr =curr.left

        try:
            if item_last is not None and item_last<item:
                return item_last
            else:
                return None
        except UnboundLocalError:
            return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, "r") as file:
            words = [line.replace("\n","") for line in file]
        # print(words)

        # random words in sorted list
        curr_time = time.time()
        for _ in range(10000):
            word = random.choice(words)
            words.index((word))
        end_time = time.time()
        print("10000 words in sorted list(seconds):", end_time-curr_time)

        tree = LinkedBST()
        for word in words:
            tree.add_no_recursion(word)

        start_time = time.time()
        for _ in range(10000):
            word = random.choice(words)
            tree.find_no_rec(word)
        end_time = time.time()
        print("10000 words in tree from sorted list:", end_time-start_time)

        random.shuffle(words)
        tree = LinkedBST()
        for word in words:
            tree.add(word)
            # print(word)

        start_time = time.time()
        for _ in range(10000):
            word = random.choice(words)
            tree.find(word)
        end_time = time.time()
        print("10000 words in tree from random list:", end_time-start_time)

        tree.rebalance()
        start_time = time.time()
        for _ in range(10000):
            word = random.choice(words)
            tree.find(word)
        end_time = time.time()
        print("10000 words in balanced tree:", end_time - start_time)


if __name__ == "__main__":
    random.seed(1337)
    b = LinkedBST()
    b.demo_bst('words.txt')
    # for i in range(30):
    #     b.add(random.randint(1,100))
    # print(b)
#     print(b.is_balanced())
#     b.rebalance()
#     print(b.is_balanced())
#     print(b)
#     print(b.successor(5))
#     print(b.successor(55))
#     print(b.predecessor(65))
#     print(b.predecessor(47))
#     print(b.predecessor(5))
#     print(b.predecessor(100))
#     print(b.successor(100))
#     print(b.predecessor(9))
