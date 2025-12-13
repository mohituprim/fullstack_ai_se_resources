from typing import List
class Solution:
    def binarySearch(self, nums:List[int], target:int)->int:
        n = len(nums)
        left = 0
        right = n-1

        while(left<=right):
            mid = left+(right-left)//2
            if nums[mid]==target:
                return mid
            elif nums[mid]>target:
                right = mid-1
            else:
                left = mid+1
        return -1

if __name__ == "__main__":
    solution = Solution()
    print(solution.binarySearch([-1,0,3,5,9,12], 12))

