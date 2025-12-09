from collections import defaultdict
from typing import List

class Solution:
    def find_group_anagram(self, strs:List[str] )->List[List[str]]:
        anagram_map = defaultdict(list)

        print(anagram_map)
        for word in strs:
            count = [0]*26
            for char in word:
                count[ord(char)-ord('a')] +=1

            print(count)
            print(tuple(count))
            anagram_map[tuple(count)].append(word)

        return list(anagram_map.values())

    
if __name__ == "__main__":
    solution = Solution()
    print(solution.find_group_anagram(["eat","tea","tan","ate","nat","bat"]))