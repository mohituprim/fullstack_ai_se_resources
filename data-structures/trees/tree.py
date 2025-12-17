# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def invertBinaryTree(self, root):
        if not root:
            return None
        
        root.left, root.right = root.right, root.left
        self.invertBinaryTree(root.left)
        self.invertBinaryTree(root.right)
        return root
    
    def maxDepthRecursion(self, root:TreeNode)->int:
        if not root:
            return 0

        left = self.maxDepthRecursion(root.left)
        right = self.maxDepthRecursion(root.right)

        return 1+ max(left, right)
    
    def maxDepthBFS(self, root:TreeNode)->int:
        if not root:
            return 0
        depth = 0
        queue = [root]

        while queue:
            depth +=1
            level_size = len(queue)

            for i in range(len(queue)):
                node = queue.pop(0) #dequeu from the front
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return depth

    def maxDepthDFS(self, root:TreeNode)->int:
        if not root:
            return 0
        max_depth = 0
        stack = [(root, 1)]

        while stack:
            node, depth = stack.pop()

            if node:
                max_depth = max(max_depth, depth)
                if node.left:
                    stack.append((node.left, depth+1))
                if node.right:
                    stack.append((node.right, depth+1))
        return max_depth


    def isSameTree(self, p:TreeNode, q:TreeNode)->bool:
        if not p and not q:
            return True

        if not p or not q or p.val!=q.val:
            return False

        left = self.isSameTree(p.left, q.left)
        right = self.isSameTree(p.right, q.right)

        return left and right

    def isSubTree(self, root:TreeNode, subRoot:TreeNode)->bool:
        if subRoot is None:
            return True
        if root == None and subRoot!=None:
            return False

        if self.isSameTree(root, subRoot):
            return True
        
        left = self.isSubTree(root.left, subRoot)
        right = self.isSubTree(root.right, subRoot)

        return left or right

    def find_lca_bst(self, root, p, q):
        #  We need to use the bst property ... in bst all the nodes in left side are lesser than root
        #  all the values in right is greter than root
        #  when root is itself ancestor
        #  when p and q lies in different side
        #  when both values lies in left
        #  when both values lies in right
        
        while root:
            if root.val>p.val and root.val>q.val:
                root = root.left
            elif root.val<p.val and root.val<q.val:
                root = root.right
            else:
                return root

    def level_order_traversal(self, root):
        if not root:
            return []

        result = []
        queue = [root]

        while root:
            level_size=len(queue)
            level = []

            for _ in range(level_size):
                node = queue.pop(0)
                level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            resule.append(level)
        return result

    def inorder(self, root, to_list):
        if not root:
            return
        if root.left:
            self.inorder(root.left, to_list)
        to_list.append(root.val)

        if root.right:
            self.inorder(root.right, to_list)

        
    def validateBinarySearchTree(self, root):
        #  get the inorder traversal
        #  if sorted it is valid
        if not root:
            return False

        to_list = []
        self.inorder(root, to_list)

        is_bst = True

        prev = to_list[0]
        for i in range(1, len(to_list)):
            if to_list[i]<=prev:
                is_bst = False
            prev = to_list[i]

        return is_bst

    def kthSmallestInBST(self, root):
        if not root:
            return False

        to_list = []
        self.inorder(root, to_list)

        is_bst = True

        prev = to_list[0]
        for i in range(1, len(to_list)):
            if to_list[i]<=prev:
                is_bst = False
            prev = to_list[i]
        if is_bst:
            return to_list[k+1]

        return None

    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        # Create a map to efficiently find the index of any element in inorder list
        io_map = {}
        for i in range(len(inorder)):
            io_map[inorder[i]] = i

        # Call recursive helper function to build the tree
        return self.splitTree(preorder, io_map, 0, 0, len(inorder) - 1)

    def splitTree(self, preorder, io_map, rootIndex, left, right):
        # Base case: if the left index exceeds the right index, subtree is empty
        if left > right:
            return None

        # Create the root node with the current root element
        root = TreeNode(preorder[rootIndex])

        # Find the index of the root element in inorder list
        mid = io_map[preorder[rootIndex]]

        # Recursively build the left subtree
        if mid > left:
            root.left = self.splitTree(preorder, io_map, rootIndex + 1, left, mid - 1)

        # Recursively build the right subtree
        if mid < right:
            root.right = self.splitTree(preorder, io_map, rootIndex + mid - left + 1, mid + 1, right)

        return root


    def maxPathSum(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        max_sum = float('-inf')

        def dfs(node):
            nonlocal max_sum  # Required to modify outer scope variable
            if not node:
                return 0
            
            left_gain = max(dfs(node.left), 0)
            right_gain = max(dfs(node.right), 0)

            price_new_path = left_gain+right_gain+node.val
            max_sum = max(max_sum, price_new_path)

            return node.val + max(left_gain, right_gain)

        dfs(root)
        return max_sum
        
    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return ""
        result, queue = [], [root]

        while queue:
            node = queue.pop(0)
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append('N')

        return ",".join(result)

        

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None
        values = data.split(',')
        root = TreeNode(int(values[0]))
        queue = [root]
        i =1
        while queue:
            node = queue.pop(0)

            if values[i] != 'N':
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i +=1
            if values[i] != 'N':
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i +=1
        return root



if __name__ == "__main__":
    # [4,2,7,1,3,6,9]
    node1 = TreeNode(4)
    node2 = TreeNode(2)
    node3 = TreeNode(7)
    node4 = TreeNode(1)
    node5 = TreeNode(3)
    node6 = TreeNode(6)
    node7 = TreeNode(9)

    node1.left = node2
    node1.right = node3

    node2.left = node4
    node2.right = node5

    node3.left = node6
    node3.right = node7

    solution = Solution()
    print(solution.invertBinaryTree(node1).left.val)
    print(solution.maxDepthRecursion(node1))
    print(solution.maxDepthBFS(node1))
    print(solution.maxDepthDFS(node1))
    print(solution.isSameTree(node1, node1))
    print(solution.isSubTree(node1, node2))