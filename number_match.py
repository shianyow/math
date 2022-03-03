from copy import deepcopy

def squeeze_matrix(matrix):
    new_matrix = []
    for line in matrix:
        if any(line):
            new_matrix.append(line)
    return new_matrix

def count_line(matrix):
    return len(matrix)

def count_number(matrix):
    count = 0
    for line in matrix:
        count += len(list(filter(lambda n: n > 0, line)))

    return count

def count_kind(matrix):
    single_list = []
    for line in matrix:
        single_list += line

    unique_list = list(set(single_list))
    if 0 in unique_list:
        unique_list.remove(0)

    return len(unique_list)

def is_match(a, b):
    global total_match_called
    total_match_called += 1

    if a == b or a + b == 10:
        return True
    return False

def find_match(matrix, index):
    y = index[0]
    x = index[1]
    matrix_width = len(matrix[0])
    matrix_height = len(matrix)
    match = []
    # Right
    for i in range(x + 1, matrix_width):
        if matrix[y][i] != 0:
            if is_match(matrix[y][x], matrix[y][i]):
                match.append((y, i))
            break

    # Lower right
    for i, j in zip(range(x + 1, matrix_width), range(y + 1, matrix_height)):
        if matrix[j][i] != 0:
            if is_match(matrix[y][x], matrix[j][i]):
                match.append((j, i))
            break

    # Down
    for j in range(y + 1, matrix_height):
        if matrix[j][x] != 0:
            if is_match(matrix[y][x], matrix[j][x]):
                match.append((j, x))
            break

    # Lower left
    for i, j in zip(range(x - 1, 0, -1), range(y + 1, matrix_height)):
        if matrix[j][i] != 0:
            if is_match(matrix[y][x], matrix[j][i]):
                match.append((j, i))
            break

    # Next line
    if not any(matrix[y][x + 1:matrix_width]) and y + 1 < matrix_height:
        for i in range(matrix_width):
            if matrix[y + 1][i] != 0:
                if is_match(matrix[y][x], matrix[y + 1][i]):
                    match.append((y + 1, i))
                break

    return match

def is_better_solution(best_solution, cur_solution):
    if cur_solution['min_lines'] < best_solution['min_lines']:
        return True
    if cur_solution['min_lines'] > best_solution['min_lines']:
        return False
    
    if cur_solution['min_kinds'] < best_solution['min_kinds']:
        return True
    if cur_solution['min_kinds'] > best_solution['min_kinds']:
        return False

    if cur_solution['min_numbers'] < best_solution['min_numbers']:
        return True
    if cur_solution['min_numbers'] > best_solution['min_numbers']:
        return False

    return False

# Input:
#   initial_matrix,
#   prev_sol
# Output:
#   best_slution
def solve(matrix, prev_sequence):
    global total_solve_called
    global best_solution, tmp_solution
    global print_level

    total_solve_called += 1

    cur_solution = {
        'matrix': matrix,
        'sequence': prev_sequence,
        'min_lines': count_line(matrix),
        'min_kinds': count_kind(matrix),
        'min_numbers': count_number(matrix),
    }

    if len(prev_sequence) <= print_level:
        print("\n" + " " * len(prev_sequence) * 2 + "Starting new path: ",
            str(len(prev_sequence)) + ":", prev_sequence and prev_sequence[-1])
        print_matrix(matrix, len(prev_sequence) * 2)
        print("Total trial count:", total_solve_called, "Total match count:", total_match_called)

    for y in range(len(matrix)):
        for x in range(9):
            match = find_match(matrix, (y, x))
            for m in match:
                cur_sequence = list(prev_sequence)
                cur_sequence.append([
                    (y, x),
                    (m[0], m[1]),
                    (matrix[y][x], matrix[m[0]][m[1]]),
                ])
                cur_matrix = deepcopy(matrix)
                cur_matrix[y][x] = 0
                cur_matrix[m[0]][m[1]] = 0
                cur_matrix = squeeze_matrix(cur_matrix)
                cur_solution = solve(cur_matrix, cur_sequence)
                if is_better_solution(best_solution, cur_solution):
                    best_solution = cur_solution
                    print("=================================== New better solution!")
                    print("\n" + " " * len(prev_sequence) * 2  + "Current solution: ")
                    print_solution(best_solution, len(prev_sequence) * 2)
                if best_solution['min_lines'] == 0:
                    return best_solution

    return cur_solution

def print_solution(solution, indent):
    print(" " * indent + "Matrix:")
    print_matrix(solution['matrix'], indent)
    
    print(" " * indent + "Sequence:")
    c = 0 
    for i in solution['sequence']:
        direction = ""
        if (i[1][0] == i[0][0] and i[1][1] > i[0][1]):
            direction = "right"
        elif (i[1][0] - i[0][0] == i[1][1] - i[0][1]):
            direction = "rower right"
        elif (i[1][0] > i[0][0] and i[1][1] == i[0][1]):
            direction = "down"
        elif (i[1][0] - i[0][0] == i[0][1] - i[1][1]):
            direction = "lower left"
        else:
            direction = "next"
        c += 1
        print(" " * indent, f'{c}: {i[2][0]}({i[0][0]},{i[0][1]}) with {i[2][1]}({i[1][0]},{i[1][1]}) of {direction}')
        
    print(" " * indent + "Min_lines:", solution['min_lines'])
    print(" " * indent + "Min_kinds:", solution['min_kinds'])
    print(" " * indent + "Min_numbers:", solution['min_numbers'])
    print("\n")

def print_matrix(matrix, indent):
    for i in range(len(matrix)):
        print(" " * indent, matrix[i])

orig_matrix = [
    # [9, 6, 4, 8, 5, 8, 1, 5, 4],
    # [3, 1, 7, 1, 4, 3, 5, 6, 2],
    # [5, 2, 5, 8, 7, 2, 1, 9, 5],
    # [9, 6, 4, 8, 5, 8, 1, 5, 4],

    # Test sample 1
    # [9, 7, 0, 1, 5, 0, 2, 9, 4],
    # [0, 2, 4, 9, 5, 0, 3, 7, 0],
    # [1, 0, 2, 3, 0, 0, 8, 1, 0],
    # [9, 7, 0, 1, 5, 0, 2, 9, 4],
    # [0, 2, 4, 9, 5, 0, 3, 7, 0],
    # [1, 0, 2, 3, 0, 0, 8, 1, 0],

    # Test sample 2 (takes about 5 minutes)
    # [0, 0, 0, 0, 0, 0, 0, 0, 4],
    # [0, 0, 0, 0, 0, 0, 0, 1, 8],
    # [0, 9, 0, 0, 0, 0, 8, 0, 5],
    # [0, 3, 0, 0, 0, 0, 5, 0, 3],
    # [0, 8, 0, 0, 5, 0, 0, 0, 0],
    # [0, 0, 4, 0, 0, 9, 0, 0, 0],
    # [3, 5, 3, 1, 0, 5, 8, 4, 5],
    # [4, 4, 1, 8, 9, 8, 5, 3, 5],
    # [3, 8, 5, 4, 9, 3, 5, 3, 1],
    # [5, 8, 4, 5, 4, 0, 0, 0, 0],

    # [4,8,7,4,2,6,7,6,5],
    # [1,5,9,5,1,5,1,8,7],
    # [8,7,6,4,2,8,0,0,0],

    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],

    # Test sample 2-1 (takes about 5 minutes)
    # [0, 0, 0, 0, 0, 0, 0, 0, 4],
    # [0, 0, 0, 0, 0, 0, 0, 1, 8],
    # [0, 9, 0, 0, 0, 0, 8, 0, 5],
    # [0, 3, 0, 0, 0, 0, 5, 0, 3],
    # [0, 8, 0, 0, 5, 0, 0, 0, 0],
    # [0, 0, 4, 0, 0, 9, 0, 0, 0],
    # [3, 5, 3, 1, 0, 5, 8, 4, 5],
    # [4, 4, 1, 8, 9, 8, 5, 3, 5],
    # [3, 8, 5, 4, 9, 3, 5, 3, 1],
    # [5, 8, 4, 5, 4, 0, 0, 0, 0],

    # Test 4 kinds plus 1
    # [0, 0, 0, 0, 0, 0, 0, 0, 4],
    # [0, 9, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 5, 0, 0, 0, 0],
    # [0, 0, 4, 0, 0, 0, 0, 0, 0],
    # [0, 5, 3, 8, 8, 8, 8, 8, 0],
    # [0, 4, 0, 0, 0, 0, 0, 8, 5],
    # [0, 0, 0, 0, 9, 3, 8, 0, 0],
    # [5, 0, 4, 8, 8, 0, 0, 0, 8],

    # [0, 0, 0, 0, 0, 0, 0, 0, 4],
    # [0, 9, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 5, 0, 0, 0, 0],
    # [0, 0, 4, 0, 0, 0, 0, 0, 0],
    # [0, 5, 3, 0, 0, 0, 0, 0, 0],
    # [0, 4, 0, 0, 0, 0, 0, 0, 5],
    # [0, 0, 0, 0, 9, 3, 0, 0, 0],
    # [5, 0, 4, 0, 0, 0, 0, 0, 0],

    # [0, 0, 0, 0, 0, 0, 0, 0, 4],
    # [0, 9, 0, 0, 0, 0, 0, 0, 0],
    # [0, 0, 0, 0, 5, 0, 0, 0, 0],
    # [0, 0, 4, 0, 0, 0, 0, 0, 0],
    # [0, 5, 3, 0, 0, 0, 0, 0, 0],
    # [0, 4, 0, 0, 0, 0, 0, 0, 5],
    # [0, 0, 0, 0, 9, 3, 0, 0, 0],
    # [5, 0, 4, 0, 0, 0, 0, 0, 0],

    # Test sample 4
    # [0,0,0,0,0,0,0,0,5],
    # [6,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,5,1,0,6],
    # [5,6,0,5,1,6,5,6,5],
    # [1,6,5,6,5,1,6,0,0],

    # Test sample 5 (takes about 30 secs)
    # [8,4,3,2,6,2,7,9,6],
    # [7,1,5,9,7,1,5,2,7],
    # [5,9,7,8,6,2,7,4,1],
    # [8,4,3,2,6,2,7,9,6],
    # [7,1,5,9,7,1,5,2,7],
    # [5,9,7,8,6,2,7,4,1],

    # Test (takes about 3 secs)
    # [8,0,3,2,6,2,7,9,6],
    # [7,0,5,9,7,1,5,2,7],
    # [5,0,7,8,6,2,7,4,1],
    # [8,0,3,2,6,2,7,9,6],
    # [7,0,5,9,7,1,5,2,7],
    # [5,0,7,8,6,2,7,4,1],

    # [0,0,0,0,0,0,0,0,0]
]

# total_solve_called = 0
# total_match_called = 0

# best_solution = {
#     'matrix': orig_matrix,
#     'sequence': [],
#     'min_lines': count_line(orig_matrix),
#     'min_kinds': count_kind(orig_matrix),
#     'min_numbers': count_number(orig_matrix),
# }
print_level = 2

def convert_num(matrix):
    for line in matrix:
        for i in range(9):
            if line[i] > 5:
                line[i] = 10 - line[i]
    return matrix


def insert_lines(matrix, append_next_line):
    new_matrix = deepcopy(matrix)

    if append_next_line:
        # Case 1: append from next line
        new_matrix.append([0] * 9)
        index_y = len(new_matrix) - 1
        index_x = 0
    else:
        # Case 2: append after last number
        index_y = len(new_matrix) - 1
        if 0 in new_matrix[index_y]:
            index_x = new_matrix[index_y].index(0)
        else:
            new_matrix.append([0] * 9)
            index_y += 1
            index_x = 0
        
    for line in matrix:
        for i in range(9):
            if line[i] > 0:
                new_matrix[index_y][index_x] = line[i]
                index_x += 1
                if index_x == 9:
                    new_matrix.append([0] * 9)
                    index_y += 1
                    index_x = 0

    return new_matrix

while True:
    total_solve_called = 0
    total_match_called = 0

    best_solution = {
        'matrix': orig_matrix,
        'sequence': [],
        'min_lines': count_line(orig_matrix),
        'min_kinds': count_kind(orig_matrix),
        'min_numbers': count_number(orig_matrix),
    }

    print("Original matrix:")
    print_matrix(orig_matrix, 0)

    # print("Converted matrix:")
    # print_matrix(convert_num(orig_matrix), 0)

    final_solution = solve(best_solution['matrix'], best_solution['sequence'])
    print("Original matrix:")
    print_matrix(orig_matrix, 0)
    print("\nFinal solution: ")
    print_solution(final_solution, 0)

    print("Total trial count:", total_solve_called, "Total match count:", total_match_called)

    if len(final_solution['matrix']) == 0:
        break

    while True:
        cont = str(input("Continue?\n1: append from next line\n2: append after last number\nq: quit\n"))
        if cont in ['1', '2', 'q']:
            break
    if cont == 'q':
        break
    print_matrix(final_solution['matrix'], 0)
    orig_matrix = insert_lines(final_solution['matrix'], cont == '1')
