def iterate_matrix(matrix, x, y, direction):
    if direction == 'R':  # Iterate through row
        for j in range(len(matrix[0])):
            print(matrix[x][j], end=" ")
        print()
    elif direction == 'C':  # Iterate through column
        for i in range(len(matrix)):
            print(matrix[i][y])
    else:
        print("Invalid direction. Please choose 'R' for row or 'C' for column.")

# Example usage:
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

x = 1  # Row index
y = 0  # Column index
direction = 'C'  # or 'C'

iterate_matrix(matrix, x, y, direction)
