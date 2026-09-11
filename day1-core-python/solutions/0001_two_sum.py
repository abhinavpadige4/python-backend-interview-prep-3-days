"""
Two Sum Problem Solution

Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

Approach: Hash Map (Dictionary)
- Iterate through the array once
- For each number, calculate its complement (target - current number)
- Check if the complement exists in our hash map
- If yes, return the current index and the complement's index
- If no, store the current number and its index in the hash map

Time Complexity: O(n) - We traverse the list once
Space Complexity: O(n) - We store up to n elements in the hash map

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
"""

from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Find two numbers that add up to target and return their indices.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        List containing the indices of the two numbers
    """
    # Hash map to store number -> index mapping
    num_map = {}
    
    # Iterate through the array
    for i, num in enumerate(nums):
        # Calculate the complement
        complement = target - num
        
        # Check if complement exists in our map
        if complement in num_map:
            # Found the pair!
            return [num_map[complement], i]
        
        # Store current number and its index
        num_map[num] = i
    
    # According to problem constraints, there's always exactly one solution
    return []

# Alternative approach: Brute Force (for comparison)
def two_sum_brute_force(nums: List[int], target: int) -> List[int]:
    """
    Brute force approach - O(n^2) time, O(1) space
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Test cases
if __name__ == "__main__":
    # Test case 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"Test 1: {two_sum(nums1, target1)}")  # Expected: [0, 1]
    
    # Test case 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"Test 2: {two_sum(nums2, target2)}")  # Expected: [1, 2]
    
    # Test case 3
    nums3 = [3, 3]
    target3 = 6
    print(f"Test 3: {two_sum(nums3, target3)}")  # Expected: [0, 1]
    
    # Verify brute force gives same results
    print(f"Brute Force Test 1: {two_sum_brute_force(nums1, target1)}")