class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        for i in range(n//2):
            for j in range(i, n-i-1):
                temp = matrix[i][j]
                # bottom left to top left
                matrix[i][j] = matrix[n-j-1][i]
                # bottom right to bottom left
                matrix[n-j-1][i] = matrix[n-i-1][n-j-1]
                # top right to bottom right
                matrix[n-i-1][n-j-1] = matrix[j][n-i-1]
                #  copy temp to top right
                matrix[j][n-i-1] = temp
