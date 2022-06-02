from code import interact
from math import ceil, floor
import tabulate

def decay(input):
    for i in range(len(input)):
        if i == len(input)-1:
            return input
        current = input[i]
        next = input[i+1]

        if next == 1:
            continue
        elif current > next:
            print("ERROR!")
            return input
        elif current == next:
            continue
        elif next == current + 1:
            continue
        else:
            
            input[i] = current + 1
            input[i+1] = next - 1
            return input

def decay2(input):
    for i_n in range(len(input)):
        i = len(input) -1 - i_n
        for j_n in range(len(input)-i):
            j = j_n + i
            if j <= i:
                continue
            current = input[i]
            next = input[j]
            if next > current + 1:
                input[i] = current + 1
                input[j] = next - 1
                return input
    return input

def get_decay_number(number_of_ones, righthand_side, should_print=False):
    current = [1 for i in range(number_of_ones)] + [righthand_side]
    count = 1
    previous = None
    if (should_print):
        print(0, current)
    while current != previous:
        
        previous = current.copy()
        current = decay2(current)
        if current == previous:
            break
        if should_print:
            print(count, current)
        count+=1
    return count

def total_decay(n):
    count = 0
    for i in range(n):
        decay_amount = get_decay_number(i, n-i, should_print=True)
        print(i, decay_amount)
        count+=decay_amount
    print(count)
    return count

def decay_sweep(n):
    previous = 0
    for i in range(n):
        
        decay_number = get_decay_number(i, n, should_print=False)
        print(i, decay_number, decay_number-previous)
        previous = decay_number
        

def super_decay_sweep(n):
    lines = []
    lines.append([""]+[f"r={y}" for y in range(n)])
    for x in range(n):
        line = [f"n1={x}"]
        for y in range(n):
            line.append(str(get_decay_number(x, y)))
        lines.append(line)
    print(tabulate.tabulate(lines))

def super_decay_sweep2(n):
    lines = []
    lines.append([""]+[f"r={y}" for y in range(n+1)])
    for x in range(n+1):
        line = [f"n1={x}"]
        for y in range(n+1):
            line.append(str(get_decay_number(x, y) - get_decay_number(x-1, y)))
        lines.append(line)
    print(tabulate.tabulate(lines))

def f(i, r):
    return get_decay_number(i, r)

def f_i(i, r):
    return f(i, r) - f(i-1, r)

def f_ii(i, r):
    return f_i(i, r) - f_i(i, r-1)

def super_decay_sweep3(n):
    lines = []
    print("".join(["  "]+[f"{y%10} " for y in range(n+1)]))
    for x in range(n+1):
        line = [f"{x%10}"]
        for y in range(n+1):
            #number = (get_decay_number(x, y) - get_decay_number(x-1, y))-(get_decay_number(x, y-1) - get_decay_number(x-1, y-1))
            number = f_ii(x, y)
            to_print = ""
            if number == 1:
                to_print = "🟩"
            elif number == -1:
                to_print = "🟥"
            else:
                to_print = "⬜"
            line.append(to_print)
        #print("".join(line))
        lines.append("".join(line))
    print("\n".join(lines))
    #print(tabulate.tabulate(lines))

def get_increase_from_n1_increment(low_n1, high_n1, high_r):
    for r in range(high_r):
        low_d = get_decay_number(low_n1, r)
        high_d = get_decay_number(high_n1, r)
        print(f"{r} => {high_d - low_d}")

def test_on_r_range(n1, h_r, func):
    for r in range(h_r):
        expected = get_decay_number(n1, r)
        actual = func(r)
        if (expected == actual):
            print(f"{r} => ✅")
        else:
            print(f"{r} => ❌ (expected: {expected} actual: {actual})")

def generalized_r_scan_for_f_ii(i, func):
    for r in range(200):
        n = func(i, r)
        to_print = ""
        if n == 1:
            to_print = "O"
        elif n == -1:
            to_print = "X"
        else:
            to_print = "_"
        print(to_print, end="")
    print()

def f_ii_analysis(i):
    generalized_r_scan_for_f_ii(i, f_ii)

def f_ii_estimation(i, r):
    if (r < i + 2):
        return 0
    if (r == i + 2):
        return 1
    
    if (i == 1):
        return r%2

    c = 0

    if ((r+1)%(i+1) < 3):
        c = 1
    
    if ((r+i-1)%i == 0):
        c -= 1
    
    return c

def f_i_by_non_estimated_integration(i, r):
    count = 0
    for x in range(r+1):
        count+=f_ii(i, x)
    return count

def f_i_by_non_estimated_integration_pos(i, r):
    count = 0
    for x in range(r+1):
        n = f_ii(i, x)
        if (n >= 0):
            count+=f_ii(i, x)
    return count

def f_i_by_non_estimated_integration_neg(i, r):
    count = 0
    for x in range(r+1):
        n = f_ii(i, x)
        if (n <= 0):
            count+=f_ii(i, x)
    return count

def f_i_estimation(i, r):
    adjusted_r = r-i-2
    if (f_i_adjusted_r(i, r) < 0):
        return 0
    
    if (i == 1):
        return ceil(r/2)-1
    return f_i_positive(i, r) - f_i_negs(i, r)

def f_i_adjusted_r(i, r):
    return r-i-2

def f_i_threes(i, r):
    return floor((f_i_adjusted_r(i, r)-1)/(i+1))

def f_i_positive(i, r):
    s = f_ii_get_s(i, r+1)
    return ((3*(f_ii_get_group(i,r+1)-2))) + min(3, s)

def f_i_negs(i, r):
    return floor((f_i_adjusted_r(i, r)+1)/(i))-1

def compare_f_i(i):
    expected_list = ["f_i"]
    actual_list = ["f_i_estimation"]
    estimated_positives_list = ['f_i_estimation_pos']
    estimated_negatives_list = ['f_i_estimation_neg']
    integration_list = ["f_i_by_integration"]
    positive_integration_list = ["f_i_by_integration_pos"]
    negative_integration_list = ["f_i_by_integration_neg"]

    for x_i in range(20):
        x = x_i 
        expected_list.append(f_i(i, x))
        actual_list.append(f_i_estimation(i, x))
        estimated_positives_list.append(f_i_positive(i, x))
        estimated_negatives_list.append(f_i_negs(i, x)*-1)
        integration_list.append(str(f_i_by_non_estimated_integration(i, x)))
        positive_integration_list.append(str(f_i_by_non_estimated_integration_pos(i, x)))
        negative_integration_list.append(str(f_i_by_non_estimated_integration_neg(i, x)))
    print(tabulate.tabulate([expected_list, actual_list, integration_list, positive_integration_list, estimated_positives_list, negative_integration_list, estimated_negatives_list]))

def f_ii_get_group(i, r):
    return floor((r+1)/(i+1))

def f_ii_get_d(i, r):
    return (i)-((f_ii_get_group(i, r)-3) % (i)) - 1

def f_ii_get_s(i, r):
    return ((r+1)%(i+1))

def compare_f_ii_estimation(i):
    generalized_r_scan_for_f_ii(i, f_ii)
    generalized_r_scan_for_f_ii(i, f_ii_estimation)
    for r in range(200):
        adjusted_r = r-i-2
        negs = floor((adjusted_r+1)/(i))
        print(f"{negs%10}", end="")
    print()
    for r in range(200):
        adjusted_r = r-i-2
        threes = floor((adjusted_r-1)/(i+1))
        print(f"{threes%10}", end="")
    print()
    for r in range(200):
        print(f"{f_ii_get_d(i, r)}", end="")
    print()
    for r in range(200):
        if f_ii_get_d(i, r) == f_ii_get_s(i, r) or (f_ii_get_d(i, r) == 0 and f_ii_get_s(i, r) == 7):
            print("^", end="")
        else:
            print("_", end="")

def range_test(expected_function, actual_function, test_scope):
    for i_ in range(test_scope):
        for r_ in range(test_scope):
            i = i_ + 1
            r = r_ + 1
            if expected_function(i, r) != actual_function(i, r):
                print(f"FAILED. i = {i}, r = {r}, expected = {expected_function(i, r)}, actual = {actual_function(i, r)}")



INITIAL = [1,1,1,17]

#print(get_decay_number(3, 17))

#total_decay(20)
#decay_sweep(20)
#super_decay_sweep(40)
r_when_n1_is_1 = lambda r: ceil(r/2)
r_when_n1_is_2 = lambda r: r_when_n1_is_1(r) + floor((r/2)-1)
#test_on_r_range(2, 50, r_when_n1_is_2)

#get_increase_from_n1_increment(3, 4, 50)
#super_decay_sweep3(40)
#f_ii_analysis(6)
#compare_f_i(7)

range_test(f_ii, f_ii_estimation, 100)

# I_TO_CHECK = 5
# for r_high in range(20):
#     if f_ii_estimation(I_TO_CHECK, r_high) == -1:
#         print(f"f_ii = {f_ii_estimation(I_TO_CHECK, r_high)}")
#         r_low_delta = get_decay_number(I_TO_CHECK, r_high-1, should_print=True) - get_decay_number(I_TO_CHECK-1, r_high-1, should_print=True)
#         r_high_delta = get_decay_number(I_TO_CHECK, r_high  , should_print=True) - get_decay_number(I_TO_CHECK-1, r_high  , should_print=True)

#         print(f"effect of increasing I from {I_TO_CHECK-1} to {I_TO_CHECK} in R={r_high-1} = {r_low_delta}")
#         print(f"effect of increasing I from {I_TO_CHECK-1} to {I_TO_CHECK} in R={r_high} = {r_high_delta}")
        


