class Solution:
    def getLRCR(self, s:str, k:int)->int:
        #  dictionary to track count of repeated character
        count = {} 

        # start pointer, max_repeat, max_length initialization
        start, max_repeat, max_length = 0,0,0

        for end in range(len(s)):
            count[s[end]] = count.get(s[end], 0)+1

            # get max_repeat  - character with heighest frequency
            max_repeat = max(max_repeat, count[s[end]])

            # if character that need to be replaced exceeds k - shrink the window
            window = end-start+1

            if window-max_repeat>k:
                count[s[start]] -=1
                start +=1
            window = end-start+1
            max_length = max(window, max_length)
        return max_length

if __name__ == "__main__":
    solution = Solution()
    print(solution.getLRCR("AABABBA", 1))

# Time Complexity = O(n)
# Space Complexity = O(1)
        