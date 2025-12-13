from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def getMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        while fast != None and fast.next != None:
            slow = slow.next
            fast = fast.next.next
            if(slow==fast):
                return None
        return slow

    # Time Complexity = O(n)
    # Space Complexity = O(1)

    def hasCycle(self, head:Optional[ListNode])->bool:
        slow, fast = head, head

        while fast!=None and fast.next !=None:
            slow = slow.next
            fast = fast.next.next
            if(slow==fast):
                return True
        return False

    # Time Complexity = O(n)
    # Space Complexity = O(1)

    def detectCycle(self, head):
        slow, fast = head, head
        while fast!=None and fast.next!=None:
            slow = slow.next
            fast = fast.next.next
            if slow==fast:
                while head != slow:
                    slow = slow.next
                    head = head.next
                return slow
        return None

    def reverseList(self, head):
        prev, curr = None, head

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        head = prev
        return head
    def reorderList(self, head):

        #  First find middle
        fast, slow = head, head
        while fast != None and fast.next != None:
            slow = slow.next
            fast = fast.next.next

        # revese second half list
        prev, curr = None, slow

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        # merge two halves

        first, second = head, prev
        while second.next:
            temp1, temp2 = first.next, second.next
            first.next = second
            second.next =temp1
            first, second = temp1, temp2   

    def removeNthFromEnd(self, head, n): Optional[ListNode]
        dummy = ListNode(0)
        dummy.next = head
        slw, fst = dummy, head
        for i in range(n):
            fst=fst.next
        while fst:
            slw = slw.next
            fst = fst.next

        slw.next = slw.next.next
        
        return dummy.next  

    def mergeKLists(self, lists):
        """
        :type lists: List[Optional[ListNode]]
        :rtype: Optional[ListNode]
        """
        if not lists:
            return None
        if len(lists)==1:
            return lists[0] 
        mid = len(lists)//2
        left = self.mergeKLists(lists[:mid])
        right = self.mergeKLists(lists[mid:])
        return self.mergeTwoLists(left, right)
        
    def mergeTwoLists(self, list1, list2):
        """
        :type list1: Optional[ListNode]
        :type list2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        dummy = ListNode()
        node = dummy

        while list1 and list2:
            if list1.val < list2.val:
                node.next = list1
                list1 = list1.next
            else:
                node.next = list2
                list2 = list2.next
            node = node.next
        if list1 is not None:
            node.next = list1
        else:
            node.next = list2
        return dummy.next

if __name__ == "__main__":
    node1 = ListNode(7)
    node2 = ListNode(11)
    node3 = ListNode(3)
    node4 = ListNode(2)
    node5 = ListNode(9)
    node6 = ListNode(9)

    # Built in id fucntion to get the memory address
    print(hex(id(node1))) 

    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node5
    node5.next = node6
    #  Uncomment to add loop
    node6.next = node3
    solution = Solution()

    result = solution.getMiddle(node1)
    if result is not None:
        print(result.val)
    print(solution.hasCycle(node1))
    print(solution.detectCycle(node1).val)
