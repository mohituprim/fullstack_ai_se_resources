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
            elif: root.val<p.val and root.val<q.val:
                root = root.right
            else:
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