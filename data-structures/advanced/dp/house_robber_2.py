class Solution:
    def max_loot(self, houses):
        if not houses:
            return 0
        if len(houses)==1:
            return nums[0]

        total_loot = [0]*len(houses)
        total_loot[0] = houses[0]
        total_loot[1] = max(houses[0], houses[1])

        for i in range(2, len(houses)):
            total_loot[i] = max(total_loot[i-2]+houses[i], total_loot[i-1])

        return total_loot[len(houses)-1]

    def max_loot_circular(self, houses):
        if not houses:
            return 0
        if len(houses)==1:
            return houses[0]
        skip_first = houses[:-1]
        skip_last = houses[1:]

        return max(self.max_loot(skip_first), self.max_loot(skip_last))

if __name__ == "__main__":

    solution = Solution()
    print(solution.max_loot_circular([3,6,2,1,5,1,2,9]))