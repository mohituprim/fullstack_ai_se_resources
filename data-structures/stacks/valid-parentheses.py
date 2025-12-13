class Solution:
    def isValid(self, s:str)->bool:
        stack = []

        # bracket map
        bracketMap = {")":"(", "}":"{", "]":"["}
        #  loop over input
        for character in s:
            #  chekcking for close bracket (if character is closed bracket)
            #  for close bracket we need to pop from stack if matching open bracket is present
            if character in bracketMap:
                if stack and stack[-1]==bracketMap[character]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(character)
        # if stack is empty .. we have valid input
        return not stack

if __name__ == "__main__":
    solution = Solution()
    print(solution.isValid("()[]{}"))
    print(solution.isValid("([]{}"))

# Time Complexity = O(n)
# Space Complexity = O(n)
