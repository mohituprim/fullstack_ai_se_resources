from typing import List

class Solution:
    def searchInRotatedSortedArray(self, nums:List[int], target:int)->int:
        n = len(nums)
        left = 0
        right = n-1

        while left<=right:
            mid = left+(right-left)//2

            if nums[mid]==target:
                return mid

            # check if left part is sorted
            if nums[left]<=nums[mid]:
                # check if target exist in first part
                if nums[left]<=target<nums[mid]:
                    right = mid-1
                else:
                    left = mid+1
            else:
                #  check if target exist in right part
                if nums[mid]<target <= nums[right]:
                    left = mid+1
                else:
                    right = mid-1
        return -1

if __name__ == "__main__":
    solution = Solution()
    print(solution.searchInRotatedSortedArray([4,5,6,7,0,1,2], 0))
