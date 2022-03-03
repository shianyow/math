import re
from pprint import pprint


numbers = [str(i) for i in range(10)]
operators = ['+', '-', '*', '/']
equal = ['=']
guess_history = []
possible_number_dict = {x: '0' for x in numbers}
possible_operator_dict = {x: '0' for x in operators}
possible_list = list(numbers) + list(operators) + list(equal)
matched_list = ['=']
trial_pool = [
    list(numbers),
    list(numbers) + list(operators),
    list(numbers) + list(operators),
    list(numbers) + list(operators),
    list(numbers) + list(operators) + list(equal),
    list(numbers) + list(equal),
    list(numbers) + list(equal),
    list(numbers),
]

# pattern nxxxn=nn
#   LHS: 1_3 2_2 3_1 1_1_1
# pattern nxxxxn=n
#   LHS: 2_3 3_2 1_1_2 1_2_1 2_1_1
# pattern nonn=nnn
#   LHS: 1_2
patterns = {
    'nononn=nn': True,
    'nonnon=nn': True,
    'nnonon=nn': True,
    'nonon=nn': True,
    'nonnn=nn': True,
    'nnonn=nn': True,
    'nnnon=nn': True,
    'nnonnn=n': True,
    'nnnonn=n': True,
    'nnon=nnn': True,
    'nonn=nnn': True,
}

human_guess = False
human_match = True

initial_guess = '12+46=58'
# initial_guess = '12+47=59'
# initial_guess = '2*8-10=6'
# initial_guess = None
# initial_guess = '5*85=425'

# solution = '5*85=425'
solution = '1*3+7=10'
# solution = '3*42=126'
# solution = '101-2=99'
# solution = '24/4-4=2'
# solution = '24/6-4=0'
# solution = '111/3=37'
# solution = '24/8-3=0'
# solution = '24/3-8=0'
# solution = '24/3-7=1'
# solution = '98-54=44'
# solution = '29-10=19'
# solution = None


# Totally 5 times
# 1: 12+46=58 -> _B_BBB__
# 2: 7*6-40=2 -> __BBBBAB
# 3: 4-0/26=4 -> BBBBBBAB
# 4: 20/2-4=6 -> ABA_AAAB
# 5: 24/6-4=0 -> AAAAAAAA

# times
# 1: 12+46=58 -> B__A_ABB
# 2: 58-48=10 -> AAAA_AA_
# 3: 58-45=13 -> AAAA_AA_
# 4: 58-47=11 -> AAAABAAB
# 5: 58-41=17 -> AAAAAAAA

def is_valid_calc(calc):
    if not calc:
        return False

    if not len(calc) == 8:
        return False

    if not calc.count('=') == 1:
        return False

    # Remove leading zero
    calc = re.sub(r'\b0+(?!\b)', '', calc)

    c_list = calc.split('=')

    if len(c_list[0]) == 0 or len(c_list[1])== 0:
        return False

    try:
        return eval(c_list[0]) == eval(c_list[1])
    except ZeroDivisionError:
        return False


def check_match(guess, solution):
    g = list(guess)
    s = list(solution)

    for i in range(8):
        if g[i] == s[i]:
            g[i] = s[i] = 'A'

    for i in range(8):
        if g[i] == 'A':
            continue
        if g[i] in s:
            for j in range(8):
                if g[i] == s[j]:
                    g[i] = s[j] = 'B'
        else:
            g[i] = '_'

    return g


def get_used_count(calc, possible_list):
    return len(set(calc) & set(possible_list))


def get_valid_calc_r(trial, debug=False):
    pass

def get_valid_calc(trial, debug=False):
    if debug:
        print(f"{possible_list=}")
        print(f"{matched_list=}")
        print(f"{trial=}")

    max_used_count = 0
    final_calc = None
    for t0 in trial[0]:
        for t1 in trial[1]:
            for t2 in trial[2]:
                for t3 in trial[3]:
                    for t4 in trial[4]:
                        for t5 in trial[5]:
                            for t6 in trial[6]:
                                for t7 in trial[7]:
                                    calc = t0 + t1 + t2 + t3 + t4 + t5 + t6 + t7
                                    assert len(set(calc) | set(possible_list)) == len(set(possible_list))
                                    # skip if any number in matched list was not used
                                    if len(set(calc) | set(matched_list)) > len(set(calc)):
                                        continue
                                    # skip calcaution contains numbers of leading zero
                                    if not re.sub(r'\b0+(?!\b)', '', calc) == calc:
                                        continue

                                    if is_valid_calc(calc):
                                        count = get_used_count(calc, possible_list)
                                        if count > max_used_count:
                                            max_used_count = count
                                            final_calc = calc
                                            if debug:
                                                print("New calc found: ", calc, count)
                                            # if len(calc) == len(set(calc)):
                                            #     print("All different, return early.")
                                            #     return final_calc, max_used_count
    if debug:
        print(f"{final_calc=} {max_used_count=}")

    return final_calc, max_used_count


def filter_by_pattern(trial, pattern):
    # print("pattern: ", pattern)
    for i in range(8):
        if pattern[i] == 'n':
            trial[i] = list(set(trial[i]) & set(numbers))
        elif pattern[i] == 'o':
            trial[i] = list(set(trial[i]) & set(operators))
        elif pattern[i] == '=':
            trial[i] = ['='] if '=' in trial_pool[i] else []
        else:
            raise "Invalid pattern!" 


def find_combination(trial_pool):
    final_calc = None
    max_count = 0
    for i in patterns:
        if not patterns[i]:
            continue
        trial = list(trial_pool)

        filter_by_pattern(trial, i)
        calc, count = get_valid_calc(trial, False)
        if calc and count > max_count:
            final_calc = calc
            max_count = count
            # if len(final_calc) == len(set(final_calc)):
            #     print("All different", final_calc)
            #     return final_calc

    return final_calc


def update_possibility_status(guess, match):
    global matched_list
    global possible_list
    global trial_pool
    global possible_number_dict
    global possible_operator_dict

    for i in range(8):
        g = guess[i]
        if match[i] == 'A':
            trial_pool[i] = [g]
            if g in numbers:
                possible_number_dict[g] = 'A'
            elif g in operators:
                possible_operator_dict[g] = 'A'
    for i in range(8):
        g = guess[i]
        if match[i] == 'B':
            if g in trial_pool[i]:
                trial_pool[i].remove(g)
            if g in numbers:
                possible_number_dict[g] = 'B'
            elif g in operators:
                possible_operator_dict[g] = 'B'
        elif match[i] == '_':
            if g in trial_pool[i]:
                trial_pool[i].remove(g)
            # TODO: FIXME
            if g in numbers and possible_number_dict[g] == '0':
                possible_number_dict[g] = '_'
                possible_list.remove(g)
            elif g in operators and possible_operator_dict[g] == '0':
                possible_operator_dict[g] = '_'
                possible_list.remove(g)

    for i in range(8):
        trial_pool[i] = list(set(trial_pool[i]) & set(possible_list))

    matched_list += [i for i in possible_number_dict if possible_number_dict[i] == 'A' or possible_number_dict[i] == 'B']
    matched_list += [i for i in possible_operator_dict if possible_operator_dict[i] == 'A' or possible_operator_dict[i] == 'B']

    print(f"{possible_number_dict=}")
    print(f"{possible_operator_dict=}")
    print(f"{possible_list=}")
    print(f"{matched_list=}")
    print(f"{trial_pool=}")


def print_status():
    possible_str = ""
    for i in possible_number_dict:
        possible_str += i if not possible_number_dict[i] == '_' else '_'
    for i in possible_operator_dict:
        possible_str += i if not possible_operator_dict[i] == '_' else '_'
    # print(possible_str)
    # pprint(trial_pool)
    for g in guess_history:
        print(f"{g[0]}: {g[1]} -> {''.join(g[2])}")
    print("\n")


def main():
    for i in range(10):
        while True:
            if human_guess:
                guess = input("Enter calculation: ")
            else:
                if i == 0 and initial_guess:
                    guess = initial_guess
                    break

                print(f"1 {matched_list=}")

                guess = find_combination(trial_pool)
                if not guess:
                    print("No results found.")
                    return

            if is_valid_calc(guess):
                break
            print(f"Invalid calculation. {guess}")

        if human_match:
            while True:
                match = input(f"Enter match result for {guess}: ")
                if len(match) == 8:
                    break
        else:
            match = check_match(guess, solution)

        guess_history.append([i + 1, guess, match])

        # Update possibility status
        update_possibility_status(guess, match)
        print_status()
        if match[0] == 'A' and len(set(match)) == 1:
            return


if __name__ == "__main__":
    main()
