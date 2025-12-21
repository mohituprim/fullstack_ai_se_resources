class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:

        if len(nums) == 0:
            return 0

        n = len(nums)
        dp = [1]*n
        max_len = 1
        #  take two pointer

        for i in range(n):
            for j in range(i):
                # we need to check for ith position what could be the best combination with previous elements
                if nums[i]>nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
                max_len = max(max_len, dp[i])
        return max_len
                
        