# Author: Surinder Matharu
# Date Last Modified: 10-Nov-2026
# Purpose: 
# References: 

def follow_instructions(instructions: list[str]) -> list[int]:

# Base Case
    def steps(i: int) -> list[int]:
        if i <  0 or i >= len(instructions):
            return []

        current_val = instructions[i]
        item_visited = [i]
        
        # if current value is blue then scan list from this value to find next element that has the value 'blue'. Once found, the target element (index) is next position after this word blue. 
        if current_val == 'blue':
            next_blue = next (
                (index for index in range (i + 1, len (instructions))
                if instructions[index] == 'blue'), 
                None, 
            )
            if next_blue is None: 
                return [item_visited]
            next_element = next_blue + 1

        # If current value is red, then the next element is calculated using formula: 2*current_val + 1
        elif current_val == 'red':
            next_element = 2 * i + 1

        # If current value is green, the next element is the next position in the list
        elif current_val == 'green':
            next_element = i + 1
        else:
            return item_visited
        # Recurisve Step
        return item_visited + steps(next_element)

    if not instructions:
        return []
    return steps (0)

# Test Example 1:
list_1 = ['blue', 'green', 'red', 'blue', 'green', 'red'] 
       
# Test Example 2:
list_2 = ['green', 'red', 'blue', 'green', 'blue', 'green'] 
          
# This runs the tests automatically, one after the other.
tests = {
        'test_1': list_1,
        'test_2': list_2
}

print(f'Test 1 Result, instruction_followed_output(list_1)')
print(f'Test 1 Result, instruction_followed_output(list_2)')

  
     


