from typing import List
class Solution:
    def getMinimum(self, nums:List[int])->int:
        n = len(nums)
        left  = 0
        right = n-1
        while left<right:
            mid = left+(right-left)//2
            if nums[mid] > nums[right]:
                left = mid+1
            else:
                right = mid

        return nums[left]

if __name__ == "__main__":
    solution = Solution()
    print(solution.getMinimum([3,4,5,1,2]))