class Solution(object):
    def climbStairs(self, n):
        if n==1:
            return n
        steps = [1, 2]

        ways =  [float('inf')]*(n+1)
        ways[0] = 0
        ways[1] = 1
        ways[2] = 2

        for i in range(3, n+1):
            ways[i] = ways[i-1] + ways[i-2]

        if ways[n]==float('inf'):
            return -1
        return ways[n]


if __name__ == "__main__":

    solution = Solution()
    print(solution.climbStairs(3))