"""
Merge Intervals Problem Solution

Given an array of intervals where intervals[i] = [starti, endi], 
merge all overlapping intervals, and return an array of the non-overlapping 
intervals that cover all the intervals in the input.

Approach: Sorting + Merge
1. Sort intervals by their start time
2. Iterate through sorted intervals
3. If current interval overlaps with previous, merge them
4. Otherwise, add previous interval to result and start new interval

Time Complexity: O(n log n) - Due to sorting
Space Complexity: O(n) - For storing the result (excluding space for sorting)

Example:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
"""

from typing import List

def merge(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge overlapping intervals.
    
    Args:
        intervals: List of intervals where each interval is [start, end]
        
    Returns:
        List of merged non-overlapping intervals
    """
    # Edge case: empty or single interval
    if not intervals or len(intervals) == 1:
        return intervals
    
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    # Initialize result with first interval
    merged = [intervals[0]]
    
    # Iterate through remaining intervals
    for current in intervals[1:]:
        # Get the last interval in merged list
        last = merged[-1]
        
        # Check if current interval overlaps with last merged interval
        if current[0] <= last[1]:  # Overlapping intervals
            # Merge by extending the end to the maximum
            last[1] = max(last[1], current[1])
        else:
            # No overlap, add current interval to result
            merged.append(current)
    
    return merged

# Alternative approach: Without modifying original intervals
def merge_without_modification(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge intervals without modifying the original intervals list.
    """
    if not intervals:
        return []
    
    # Sort intervals by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = []
    for interval in sorted_intervals:
        # If merged is empty or no overlap
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval[:])  # Append copy to avoid modification
        else:
            # Overlap: merge with the last interval
            merged[-1][1] = max(merged[-1][1], interval[1])
    
    return merged

# Test cases
if __name__ == "__main__":
    # Test case 1
    intervals1 = [[1,3],[2,6],[8,10],[15,18]]
    print(f"Test 1: {merge(intervals1)}")  # Expected: [[1,6],[8,10],[15,18]]
    
    # Test case 2
    intervals2 = [[1,4],[4,5]]
    print(f"Test 2: {merge(intervals2)}")  # Expected: [[1,5]]
    
    # Test case 3: No overlap
    intervals3 = [[1,2],[3,4],[5,6]]
    print(f"Test 3: {merge(intervals3)}")  # Expected: [[1,2],[3,4],[5,6]]
    
    # Test case 4: Complete overlap
    intervals4 = [[1,4],[2,3]]
    print(f"Test 4: {merge(intervals4)}")  # Expected: [[1,4]]
    
    # Test case 5: Single interval
    intervals5 = [[1,2]]
    print(f"Test 5: {merge(intervals5)}")  # Expected: [[1,2]]
    
    # Test case 6: Empty list
    intervals6 = []
    print(f"Test 6: {merge(intervals6)}")  # Expected: []
    
    # Verify alternative approach
    print(f"Without modification Test 1: {merge_without_modification(intervals1)}")