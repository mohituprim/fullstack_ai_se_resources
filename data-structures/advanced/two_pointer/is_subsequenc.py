class Solution:
    def is_subsequence(self, s:str, t:str)->bool:
        itr1,itr2 = 0,0
        while itr1<len(s) and itr2<len(t):
            if s[itr1]==t[itr2]:
                itr1 +=1
                itr2 +=1
            else:
                itr2 +=1
        return itr1 == len(s)

if __name__ == "__main__":
    solution = Solution()
    print(solution.is_subsequence('ad', 'abd'))


# Time Complexity = O(n)
# Space Complexity = O(1) 