class Solution:
    def getMinimumWindowSubstring(self, s:str, t:str)->str:
        # check if s or t is empty
        if not s or not t:
            return ""

        # create map for t and store the frequency
        tMap = {}
        for char in t:
            tMap[char] = tMap.get(char, 0)+1
        
        # varibales to track how many covered and unique charcter in t
        have = 0
        need = len(tMap)

        # Create window map to store the frequncy of charcters
        wMap ={}

        # Two pointers for sliding window
        start, end = 0,0

        # variables to hold the result
        min_length = float("inf")
        result = ""

        while end<len(s):
            char = s[end]

            # update wMap
            wMap[char] = wMap.get(char, 0)+1

            # frequency of char matched desired frequency, increment have

            if char in tMap and tMap[char]==wMap[char]:
                have +=1
            
            # Try to shrink the window
            while start <= end and have==need:
                char = s[start]

                #  Update the result if this window is smaller
                current_window = end-start+1
                if current_window < min_length:
                    min_length = current_window
                    result = s[start:end+1]

                # update the map and compare them
                wMap[char] -=1
                if char in tMap and wMap[char]<tMap[char]:
                    have -=1

                #  move the start pointer
                start +=1
            
            # move end pointer
            end +=1
        return result

if __name__ == "__main__":
    solution = Solution()
    print(solution.getMinimumWindowSubstring("ADOBECODEBANC", "ABC"))

# Time Complexity = O(S+T)
# Space Complexity = O(S+T)


