from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_map = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []

    def twoSum2(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        # Store the index of the first number
        seen[nums[0]] = 0
        for i in range(1, len(nums)):
            if target - nums[i] in seen:
                return [seen[target - nums[i]], i] # Return the index of the first number and the current number
            seen[target - nums[i]] = i # Store the index of the complement of the current number
        return []

if __name__ == "__main__":
    solution = Solution()
    print(solution.twoSum([2, 7, 11, 15], 9))
    print(solution.twoSum2([2, 7, 11, 15], 9))

# Time Complexity = O(n)
# Space Complexity = O(n)