import random

def create_word_search(words):
    # Determine the size of the grid
    max_word_length = len(max(words, key=len))
    grid_size = max_word_length * 2
    
    # Create a blank grid
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Place words on the grid
    for word in words:
        direction = random.choice(['horizontal', 'vertical'])
        word_length = len(word)
        if direction == 'horizontal':
            # Try to place the word horizontally
            for i in range(grid_size - word_length):
                if all(grid[i][j] == ' ' or grid[i][j] == word[j-i] for j in range(i, i+word_length)):
                    for j in range(i, i+word_length):
                        grid[j][j-i] = word[j-i].lower()
                    break
            else:
                # Try to place the word vertically instead
                for i in range(grid_size - word_length):
                    if all(grid[j][i] == ' ' or grid[j][i] == word[j-i] for j in range(i, i+word_length)):
                        for j in range(i, i+word_length):
                            grid[j][i] = word[j-i].lower()
                        break
                else:
                    print(f"Could not place word '{word}'")
        else:
            # Try to place the word vertically
            for i in range(grid_size - word_length):
                if all(grid[j][i] == ' ' or grid[j][i] == word[j-i] for j in range(i, i+word_length)):
                    for j in range(i, i+word_length):
                        grid[j][i] = word[j-i].lower()
                    break
            else:
                # Try to place the word horizontally instead
                for i in range(grid_size - word_length):
                    if all(grid[i][j] == ' ' or grid[i][j] == word[j-i] for j in range(i, i+word_length)):
                        for j in range(i, i+word_length):
                            grid[i][j] = word[j-i].lower()
                        break
                else:
                    print(f"Could not place word '{word}'")
    
    # Fill in blank spaces with random letters
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice(letters)
    
    # Format the grid with spaces between the letters and all letters lower case
    formatted_grid = ''
    for row in grid:
        formatted_row = ' '.join([letter.lower() for letter in row])
        formatted_grid += formatted_row + '\n'
    
    return formatted_grid
