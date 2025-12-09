class Solution:
    def threeSum(self, nums):
        #  First check if nums is valid array
        if nums is None or len(nums)<3:
            return []
        #  Sort the given array
        nums.sort()

        # crate set to store the result
        result = set()

        #  pick one element and use left and right pointer
        for i in range(len(nums)):
            left = i+1;
            right = len(nums)-1
            while left<right:
                target = nums[i]+nums[left]+nums[right]
                if target ==0:
                    result.add((nums[i], nums[left], nums[right]))
                    left+=1
                    right-=1
                elif target<0:
                    left +=1
                elif target>0:
                    right -=1
        return list(map(list, result))
if __name__ == "__main__":
    solution = Solution()
    print(solution.threeSum([-1,0,1,2,-1,-4]))

# Time Complexity = O(n*n)
# Space Complexity = O(1)