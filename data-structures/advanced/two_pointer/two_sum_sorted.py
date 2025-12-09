from typing import List

class Solution:
    def two_sum(self, numbers:List[int], target:int)->List[int]:
        left = 0;
        right = len(numbers)-1

        while left<right:
            if numbers[left]+numbers[right] > target:
                right -=1
            if numbers[left]+numbers[right] < target:
                left +=1
            if numbers[left]+numbers[right]==target:
                return [left+1, right+1]

        return []

if __name__ == "__main__":
    solution = Solution()
    print(solution.two_sum([1,2,3], 3))

# Time Complexity = O(n)
# Space Complexity = O(1)   