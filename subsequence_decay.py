from code import interact
from math import ceil, floor
import tabulate

def decay(input):
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
        current = decay(current)
        if current == previous:
            break
        if should_print:
            print(count, current)
        count+=1
    return count

class SubsequenceDecay:
    '''
    Decay single.
    '''
    def decay(input):
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
    
    def get_initial_state(i, r):
        return [1 for i in range(i)] + [r]

    def decay_fully(i, r):
        states = []
        current = SubsequenceDecay.get_initial_state(i, r)
        states.append(current.copy())
        previous = None
        while current != previous:
            previous = current.copy()
            current = SubsequenceDecay.decay(current)
            if current == previous:
                break
            states.append(current.copy())
        return states

    def get_decay_number(i, r):
        return len(SubsequenceDecay.decay_fully(i, r))

    def get_fully_decayed_state(i, r):
        return SubsequenceDecay.decay_fully(i, r)[-1]

    def get_new_states(i, r):
        return [[1]+SubsequenceDecay.get_fully_decayed_state(i-1, r)] + [x for x in SubsequenceDecay.decay_fully(i, r) if x[0] != 1]

class F_II:
    def actual(i, r):
        return F_I.actual(i, r) - F_I.actual(i, r-1)

    def estimated(i, r):
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
    
    '''
    Gets the group number.
    '''
    def group(i, r):
        return floor((r+1)/(i+1))

    '''
    Position within group.
    '''
    def s(i, r):
        return ((r+1)%(i+1))

class F_I:
    def actual(i, r):
        return F.actual(i, r) - F.actual(i-1, r)

    def integrated(i, r):
        count = 0
        for x in range(r+1):
            count+=F_II.actual(i, x)
        return count
    
    '''
    This is a simplified form of the estimated integral function
    '''
    def estimated(i, r):
        if (F_I._adjusted_r(i, r) < 0):
            return 0
        
        if (i == 1):
            return ceil(r/2)-1

        term_1 = (3*floor((r+2)/(i+1)))
        term_2 = min(3, (r+2)%(i+1))
        term_3 = -1*floor((r-1)/i)
        term_4 = -4
        return term_1 + term_2 +term_3 +term_4

    '''
    Return integral evaluated only when f_ii is positive or zero
    '''
    def integral_positive(i, r):
        return F_I._filtered_integral(i, r, lambda a : a >= 0)

    '''
    Return integral evaluated only when f_ii is positive or zero
    '''
    def integral_negative(i, r):
        return F_I._filtered_integral(i, r, lambda a : a <= 0)

    '''
    Estimates the positive component of the integral.
    '''
    def estimated_positive_integral(i, r):
        s = F_II.s(i, r+1)
        return ((3*(F_II.group(i,r+1)-2))) + min(3, s)

    '''
    Estimates the negative component of the integral.
    '''
    def estimated_negative_integral(i, r):
        return -1*(floor((F_I._adjusted_r(i, r)+1)/(i))-1)

    '''
    Sums the negative and positive components.
    '''
    def estimated_integral(i, r):
        if (F_I._adjusted_r(i, r) < 0):
            return 0
        
        if (i == 1):
            return ceil(r/2)-1
        return F_I.estimated_positive_integral(i, r) + F_I.estimated_negative_integral(i, r)

    def _filtered_integral(i, r, filter):
        count = 0
        for x in range(r+1):
            n = F_II.actual(i, x)
            if (filter(n)):
                count+=F_II.actual(i, x)
        return count

    def _adjusted_r(i, r):
        return r-i-2

class F:
    def actual(i, r):
        return SubsequenceDecay.get_decay_number(i, r)
    
    def integrated(i, r):
        count = ceil(r/2)
        for x_ in range(i+1):
            x = x_ +1
            count += F_I.actual(x, r)
        return count

def range_test(expected_function, actual_function, test_scope):
    for i_ in range(test_scope):
        for r_ in range(test_scope):
            i = i_ + 1
            r = r_ + 1
            if expected_function(i, r) != actual_function(i, r):
                print(f"FAILED. i = {i}, r = {r}, expected = {expected_function(i, r)}, actual = {actual_function(i, r)}")

def generalized_sweep(function, low_i, high_i, low_r, high_r):
    lines = []
    for i_ in range(high_i - low_i):
        i = i_ + low_i
        line = []
        for r_ in range(high_r - low_r):
            r = r_ + low_r
            line.append(function(i, r))
        lines.append(line)
    print(tabulate.tabulate(lines))

def terminal():
    while True:
        command = input("> ").split(" ")
        if command[0] == "e":
            i = int(command[1])
            r = int(command[2])
            get_decay_number(i, r)
            print(SubsequenceDecay.get_new_states(i, r))
            print(f"I = {i} R = {r} F = {F.actual(i, r)} F' = {F_I.estimated(i, r)} F'' = {F_II.estimated(i, r)}")
        if command[0] == "test":
            print("===== F_II =====")
            print("Estimated = Actual")
            range_test(F_II.actual, F_II.estimated, 50)
            print("===== F_I =====")
            print("Estimated = Actual")
            range_test(F_I.actual, F_I.estimated, 50)
            print("Integrated = Actual")
            range_test(F_I.actual, F_I.integrated, 50)
            print("Estimated Integral = Actual")
            range_test(F_I.actual, F_I.estimated_integral, 50)
            print("===== F =====")
            print("Nothing to test.")
        elif command[0] == "c": 
            i_1 = int(command[1])
            r_1 = int(command[2])
            i_2 = int(command[1])
            r_2 = int(command[2])

terminal()


