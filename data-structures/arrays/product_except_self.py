from typing import List
class Solution:
    def productExceptSelf(self, nums:List[int])->List[int]:
        # Initialize left and right product array
        leftProduct = [1]*len(nums)
        rightProduct = [1]*len(nums)

        #  Fill left product
        for i in range(1, len(nums)):
            leftProduct[i] = leftProduct[i-1]*nums[i-1]

        #  Fill right product - Start with n-2 till -1 and decrease it by -1
        for i in range(len(nums)-2, -1, -1):
            rightProduct[i] = rightProduct[i+1]*nums[i+1]

        result = [1]*len(nums)

        for i in range(len(nums)):
            result[i] = leftProduct[i]*rightProduct[i]
        return result

if __name__ == "__main__":
    solution = Solution()
    print(solution.productExceptSelf([1, 2, 3, 4]))

# Time Complexity = O(n)
# Space Complexity = O(n)