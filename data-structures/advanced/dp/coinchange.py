class Solution:
    def coinChange(self, coins, amount):

        steps = [float('inf')]*(amount+1)

        steps[0]=0

        for i in range(1, amount+1):
            for coin in coins:
                if coin<=i:
                    steps[i] = min(steps[i], steps[i-coin]+1)
        if steps[amount] == float('inf'):
            return -1

        return steps[amount]

if __name__ == "__main__":

    solution = Solution()
    print(solution.coinChange([1,2,5], 11))