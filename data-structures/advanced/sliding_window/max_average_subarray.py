from typing import List
class MaxAverage:
    def getMaxAverage(self, nums:List[int], k:int)->float:
        current_sum = 0
        # Curresnt sum for first window
        for i in range(k):
            current_sum += nums[i]

        max_sum = current_sum

        start=0
        end=k
        while end<len(nums):
            #  remove first element of window
            current_sum -=nums[start]
            start +=1
            #  add new element in window
            current_sum +=nums[end]
            end +=1

            max_sum = max(max_sum, current_sum)

        return float(max_sum)/k

if __name__ == "__main__":
    solution = MaxAverage()
    print(solution.getMaxAverage([1,12,-5,-6,50,3], 4))

# Time Complexity = O(n)
# Space Complexity = O(1)