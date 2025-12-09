from typing import List
class Solution:
    def getLCS(self, nums:List[int])->int:
        lcs=0
        visitedMap = {}

        # populate visited map with False
        for num in nums:
            visitedMap[num] = False

        for num in nums:
            l=1
            seq = num+1
            # Check in formward directions
            while seq in visitedMap and visitedMap[seq] == False:
                l +=1
                visitedMap[seq]=True
                seq +=1

            seq = num-1
            # Check in backward directions
            while seq in visitedMap and visitedMap[seq] == False:
                l +=1
                visitedMap[seq]=True
                seq -=1

            lcs = max(l, lcs)

        return lcs

if __name__ == "__main__":
    solution = Solution()
    print(solution.getLCS([2, 3, 4, 15]))
    print(solution.getLCS([2, 3, 7, 3]))

# Time Complexity = O(n)
# Space Complexity = O(n)