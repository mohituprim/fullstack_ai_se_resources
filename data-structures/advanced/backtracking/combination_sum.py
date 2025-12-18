from typing import List

class Solution:
    def get_combination_sum(self, candidates:List[int], target:int)->List[List[int]]:

        all_combination = []

        def dfs(index, current_combination, current_sum):
            nonlocal all_combination
            # fisrt check if it matches with target
            if current_sum==target:
                all_combination.append(current_combination)
                return

            # check if it exceeds or out of candiate
            if index>=len(candidates) or current_sum>7:
                return

            # check possibilities using current element
            dfs(index, current_combination+[candidates[index]], current_sum+candidates[index])
            # check with out current element
            dfs(index+1, current_combination, current_sum)

        dfs(0, [], 0)

        return all_combination

if __name__ == "__main__":

    solution = Solution()
    print(solution.get_combination_sum([2,3,6,7], 7))