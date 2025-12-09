class Solution:
    def getLongestSubstring(self, s:str)->int:
        start, end, max_length = 0,0,0
        current_window_size = 0

        # Create hash set to check the repeating charcter
        hashSet = set()

        while end<len(s):
            if s[end] not in hashSet:
                hashSet.add(s[end])
                current_window_size = end-start+1
                max_length = max(max_length, current_window_size)
                end +=1
            else:
                hashSet.remove(s[end])
                start +=1
        return max_length

if __name__ == "__main__":
    solution = Solution()
    print(solution.getLongestSubstring("bbbbb"))

# Time Complexity = O(n)
# Space Complexity = O(n)