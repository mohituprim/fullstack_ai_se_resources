class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        rows, cols = len(matrix), len(matrix[0])

        fr = False
        fc = False

        for i in range(rows):
            if matrix[i][0]==0:
                fr=True
                break
        
        for j in range(cols):
            if matrix[0][j]==0:
                fc=True
                break

        # visit remaining array and mark zero in first column or row
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][j]==0:
                    matrix[0][j]=0
                    matrix[i][0]=0

        # zero out marked rows and column
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][0]==0 or matrix[0][j]==0:
                    matrix[i][j]=0

        # zero out first row
        if fr:
            for i in range(rows):
                matrix[i][0]=0

        if fc:
            # zero out first column
            for j in range(cols):
                matrix[0][j]=0
