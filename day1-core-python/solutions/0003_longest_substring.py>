"""
Longest Substring Without Repeating Characters Problem Solution

Given a string s, find the length of the longest substring without repeating characters.

Approach: Sliding Window with Hash Map
- Use two pointers (left and right) to represent the current window
- Use a hash map to store the most recent index of each character
- Expand the window by moving right pointer
- When a duplicate is found, move left pointer to max(left, last_seen[char] + 1)
- Update the maximum length found

Time Complexity: O(n) - Each character is visited at most twice
Space Complexity: O(min(m, n)) - Size of the hash map (charset size)

Example:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
"""

def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring without repeating characters.
    
    Args:
        s: Input string
        
    Returns:
        Length of the longest substring without repeating characters
    """
    # Hash map to store the most recent index of each character
    char_index_map = {}
    
    # Left pointer of the sliding window
    left = 0
    
    # Maximum length found
    max_length = 0
    
    # Iterate through the string with right pointer
    for right in range(len(s)):
        current_char = s[right]
        
        # If character is already in the current window, move left pointer
        if current_char in char_index_map and char_index_map[current_char] >= left:
            # Move left pointer to the position after the last occurrence
            left = char_index_map[current_char] + 1
        
        # Update the character's most recent index
        char_index_map[current_char] = right
        
        # Update maximum length
        current_length = right - left + 1
        max_length = max(max_length, current_length)
    
    return max_length

# Alternative approach: Sliding Window with Set
def length_of_longest_substring_set(s: str) -> int:
    """
    Alternative approach using a set to track characters in current window.
    """
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Remove characters from left until we can add s[right]
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Test cases
if __name__ == "__main__":
    # Test case 1
    s1 = "abcabcbb"
    print(f"Test 1: '{s1}' -> {length_of_longest_substring(s1)}")  # Expected: 3
    
    # Test case 2
    s2 = "bbbbb"
    print(f"Test 2: '{s2}' -> {length_of_longest_substring(s2)}")  # Expected: 1
    
    # Test case 3
    s3 = "pwwkew"
    print(f"Test 3: '{s3}' -> {length_of_longest_substring(s3)}")  # Expected: 3
    
    # Test case 4: Empty string
    s4 = ""
    print(f"Test 4: '{s4}' -> {length_of_longest_substring(s4)}")  # Expected: 0
    
    # Test case 5: Single character
    s5 = "a"
    print(f"Test 5: '{s5}' -> {length_of_longest_substring(s5)}")  # Expected: 1
    
    # Verify alternative approach
    print(f"Set approach Test 1: {length_of_longest_substring_set(s1)}")