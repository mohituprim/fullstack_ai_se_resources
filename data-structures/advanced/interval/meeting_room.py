# Function to determine if a person can attend all meetings
def can_attend_meetings(intervals):
    # Step 1: Sort the intervals by start time
    intervals.sort()

    # Step 2: Check for any overlap between consecutive meetings
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False

    return True
