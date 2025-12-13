from typing import List
class Solution:
    def dailyTemp(self, temperatures)->List[int]:
        n = len(temperatures)
        stack = []
        gap = [0]*n

        for i in range(n-1, -1, -1):
            # pop all the element which lesser
            while stack and temperatures[i]>=temperatures[stack[-1]]:
                stack.pop()
            # greater one left in stack now
            if stack:
                gap[i] = stack[-1]-i
            
            stack.append(i)
        return gap

if __name__ == "__main__":
    solution = Solution()
    print(solution.dailyTemp([73,74,75,71,69,72,76,73]))
