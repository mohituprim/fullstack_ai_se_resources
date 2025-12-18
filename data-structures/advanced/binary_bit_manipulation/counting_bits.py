class Solution:
    def countBits(self, n: int) -> List[int]:
        result = [0]*(n+1)
        if n==0:
            return result
        result[1]=1
        for i in range(2, n+1):
            if i%2 == 0:
                result[i]=result[i//2]
            else:
                # result[i]= result[i-1]+1
                result[i]= result[i//2]+1
        return result
