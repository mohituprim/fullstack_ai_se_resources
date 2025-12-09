class Soultion:
    def maxProfit(self, prices)->int:
        max_profit =0
        current_profit=0
        buy_price = prices[0]

        for i in range(1, len(prices)):
            #  buy if price is lower
            if buy_price>prices[i]:
                buy_price = prices[i]
            #  sell if price it=s higher
            else:
                current_profit = prices[i]-buy_price
                max_profit = max(max_profit, current_profit)
        return max_profit

if __name__ == "__main__":
    solution = Soultion()
    print(solution.maxProfit([7,1,5,3,6,4]))

# Time Complexity = O(n)
# Space Complexity = O(1)
        