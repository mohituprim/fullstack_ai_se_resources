class Solution:
    def maxArea(self, height)->int:
        left=0
        right=len(height)-1
        max=0
        while left<right:
            area = min(height[left], height[right])*(right-left)
            if area>max:
                max=area
            if height[left]<=height[right]:
                left +=1
            else:
                right -=1
        return max

if __name__ == "__main__":
    solution = Solution()
    print(solution.maxArea([1,8,6,2,5,4,8,3,7]))

# Time Complexity = O(n)
# Space Complexity = O(1)