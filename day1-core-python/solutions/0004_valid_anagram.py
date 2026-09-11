"""
Valid Anagram Problem Solution

Given two strings s and t, return true if t is an anagram of s, and false otherwise.

Approach 1: Character Counting (Hash Map)
- Count frequency of each character in both strings
- Compare the frequency maps
- If they match, strings are anagrams

Approach 2: Sorting
- Sort both strings
- Compare if sorted strings are equal

Time Complexity:
- Approach 1: O(n) where n is length of strings
- Approach 2: O(n log n) due to sorting

Space Complexity:
- Approach 1: O(1) - Fixed size (26 for lowercase English letters)
- Approach 2: O(n) - For storing sorted strings

Example:
Input: s = "anagram", t = "nagaram"
Output: true
"""

from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    """
    Check if t is an anagram of s using character counting.
    
    Args:
        s: First string
        t: Second string
        
    Returns:
        True if t is an anagram of s, False otherwise
    """
    # Early exit: if lengths differ, they can't be anagrams
    if len(s) != len(t):
        return False
    
    # Count characters in both strings
    return Counter(s) == Counter(t)

# Alternative approach: Manual counting with array (for lowercase letters)
def is_anagram_array(s: str, t: str) -> bool:
    """
    Check anagram using fixed-size array for character counts.
    Assumes input contains only lowercase English letters.
    """
    if len(s) != len(t):
        return False
    
    # Array to count characters (26 for lowercase English letters)
    char_count = [0] * 26
    
    # Increment for s, decrement for t
    for i in range(len(s)):
        char_count[ord(s[i]) - ord('a')] += 1
        char_count[ord(t[i]) - ord('a')] -= 1
    
    # Check if all counts are zero
    return all(count == 0 for count in char_count)

# Alternative approach: Sorting
def is_anagram_sort(s: str, t: str) -> bool:
    """
    Check anagram by sorting both strings.
    """
    return sorted(s) == sorted(t)

# Test cases
if __name__ == "__main__":
    # Test case 1
    s1 = "anagram"
    t1 = "nagaram"
    print(f"Test 1: '{s1}' and '{t1}' -> {is_anagram(s1, t1)}")  # Expected: True
    
    # Test case 2
    s2 = "rat"
    t2 = "car"
    print(f"Test 2: '{s2}' and '{t2}' -> {is_anagram(s2, t2)}")  # Expected: False
    
    # Test case 3: Empty strings
    s3 = ""
    t3 = ""
    print(f"Test 3: '{s3}' and '{t3}' -> {is_anagram(s3, t3)}")  # Expected: True
    
    # Test case 4: Single character
    s4 = "a"
    t4 = "a"
    print(f"Test 4: '{s4}' and '{t4}' -> {is_anagram(s4, t4)}")  # Expected: True
    
    # Test case 5: Different lengths
    s5 = "a"
    t5 = "ab"
    print(f"Test 5: '{s5}' and '{t5}' -> {is_anagram(s5, t5)}")  # Expected: False
    
    # Verify alternative approaches
    print(f"Array approach Test 1: {is_anagram_array(s1, t1)}")
    print(f"Sort approach Test 1: {is_anagram_sort(s1, t1)}")