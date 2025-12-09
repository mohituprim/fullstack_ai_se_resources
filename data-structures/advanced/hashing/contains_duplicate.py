from typing import List 
class Solution:
    def containsDuplicate(self, list:List[int])->bool:
        seen = {}
        seen[list[0]]=list[0]
        for i in range(1, len(list)):
            if list[i] in seen:
                return True
            seen[list[i]]=list[i]
        return False

if __name__ == "__main__":
    solution = Solution()
    print(solution.containsDuplicate([2, 3, 7, 15]))
    print(solution.containsDuplicate([2, 3, 7, 3]))

# Time Complexity = O(n)
# Space Complexity = O(n)