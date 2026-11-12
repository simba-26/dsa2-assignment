# Author: Surinder Matharu
# Date Last Modified: 12-Nov-2026
# Purpose: Build a recursive traversal that iterates through a list of colours ['blue', 'red', or 'green') and follows defnined instructions for each colour. 
#             Return the indices visited. 
# References: 

def follow_instructions(instructions: list[str]) -> list[int]:

# Base Case. This section checks the boundaries
    def steps(i: int) -> list[int]:
        if i <  0 or i >= len(instructions): # Lower (i < 0) prevents negative indices, while Upper (i >= len (instructions)) catches out-of-range indices early, preventing an IndexError.
            return [] # if it does, it will return an empty list. 

        current_val = instructions[i]
        item_visited = [i] # serves as a memory of the indices visited
        
        # if current value is blue then scan list from this value to find next element that has the value 'blue'. 
        # Once found, the target element (index) is next position after this word blue. 
        if current_val == 'blue':
            next_blue = next (
                (index for index in range (i + 1, len (instructions)) # Looks through instructions at current index and checks every element after this for the next string 'blue'
                if instructions[index] == 'blue'), 
                None, 
            )
            if next_blue is None: 
                return item_visited # if not found, returns full visited list
            next_element = next_blue + 1 #if found, returns index of value after next_blue

        # If current value is red, then the next element is calculated using formula: 2*current_val + 1
        elif current_val == 'red':
            next_element = 2 * i + 1

        # If current value is green, the next element is the next position in the list
        elif current_val == 'green':
            next_element = i + 1
        else:
            return item_visited
        
        return item_visited + steps(next_element) # Key recursion element. This aims to build the final output list by adding the steps together until the recursion teriminates. 

    if not instructions: # Without this the output printed is None
        return []
    return steps (0)

# Test Example 1:
list_1 = ['red', 'green', 'red', 'blue', 'green', 'red', 'blue', 'green'] 
       
# Test Example 2:
list_2 = ['red','blue', 'red', 'blue', 'green', 'blue', 'red', 'green'] 
          
# This runs the tests automatically, one after the other.
tests = {
        'test_1': list_1,
        'test_2': list_2
}

print(f'Test 1: {follow_instructions(tests['test_1'])}')
print(f'Test 2: {follow_instructions(tests['test_2'])}')


  
     


