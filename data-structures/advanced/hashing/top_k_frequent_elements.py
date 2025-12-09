from typing import List

class Solution:
    def get_top_k_frequent_elements(self, nums: List[int], k:int)->List[int]:
        # Initalize frequency map and bucket
        freqMap = {}
        bucket = [[] for _ in range(len(nums)+1)]

        # Fill frequency map
        for num in nums:
            if num in freqMap:
                freqMap[num] +=1
            else:
                freqMap[num] =1

        # Fill bucket to get the top k elements
        for key, freq in freqMap.items():
           bucket[freq].append(key)

        result =[]

        # Traverse bucket in reverse order 
        for i in reversed(range(len(bucket))):
            if bucket[i]:
                for value in bucket[i]:
                    if len(result)<k:
                        result.append(value)
                    else:
                        return result
        return result

if __name__ == "__main__":
    solution = Solution()
    print(solution.get_top_k_frequent_elements([1,1,1,2,2,3,3,3], 2))


# Time Complexity = O(n)
# Space Complexity = O(n) 