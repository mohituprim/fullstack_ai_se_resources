class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        xor=0
        n = len(nums)
        for i in range(n):
            xor = xor^i^nums[i]
        xor = xor^n
        return xor