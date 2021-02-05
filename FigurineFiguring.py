from math import sqrt, factorial
from collections import Counter
import time

def upper_products(starting_value, n_products):
    prod = starting_value
    for i in range(1, n_products):
        prod *= (starting_value-i)
    return prod

def is_good_comb(indices, max_count_letter):

    for letter in range(0,11):
        count = 0
        for el in indices:
            if el == letter:
                count += 1
                if count > max_count_letter[letter]:
                    return False, letter
    return True, 0

def next_indices(indices, n, r):

    for i in reversed(range(r)):
        if indices[i] != n - 1:
            break
    else:
        return []

    indices[i:] = [indices[i] + 1] * (r - i)
    return indices

def combinations_with_replacement_and_selection(iterable, r, max_count_letter):

    """Modified verision of combinations_with_replacement in itertools to skip not allowed combinations"""

    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r


    good_comb, letter_overflowing = is_good_comb(indices, max_count_letter)
    if good_comb:
        yield tuple(pool[i] for i in indices)

    while True:

        indices = next_indices(indices, n, r)
        if not indices: #Empty string
            return

        good_comb, letter_overflowing = is_good_comb(indices, max_count_letter)

        while not good_comb:
            k = indices.index(letter_overflowing)
            new_indices = indices[:k] + [letter_overflowing] * max_count_letter[letter_overflowing] + [letter_overflowing+1] * (r-k-max_count_letter[letter_overflowing])
            if max(new_indices) > 10:
                indices = next_indices(indices, n, r)
                if not indices:
                    return
                good_comb = True
            else:
                indices = new_indices
            good_comb, letter_overflowing = is_good_comb(indices, max_count_letter)


        yield tuple(pool[i] for i in indices)

def calculate_expected_frequencies(rounds = 75, single_round = False):

    f = open("speed.csv", "w")

    figurines = ['a','a','a','a','a','a','a','a','a','a','a','a',
                 'b','b','b','b','b','b','b','b','b','b','b',
                 'c','c','c','c','c','c','c','c','c','c',
                 'd','d','d','d','d','d','d','d','d',
                 'e','e','e','e','e','e','e','e',
                 'f','f','f','f','f','f','f',
                 'g','g','g','g','g','g',
                 'h','h','h','h','h',
                 'i','i','i','i',
                 'j','j','j',
                 'k','k',
                 'l']
    
    letters = ['a','b','c','d','e','f','g','h','i','j','k']
    reversed_letters = list(reversed(letters))
    counter_figurines = Counter(figurines)

    ####Inverted max count ####
    max_count_letter = {}
    max_count_letter[0] = 2   #k
    max_count_letter[1] = 3   #j
    max_count_letter[2] = 4   #i
    max_count_letter[3] = 5   #h 
    max_count_letter[4] = 6   #g
    max_count_letter[5] = 7   #f
    max_count_letter[6] = 8   #e
    max_count_letter[7] = 9   #d
    max_count_letter[8] = 10  #c
    max_count_letter[9] = 10 #To speed up calculations instead of 11  
    max_count_letter[10] = 10 #To speed up calculations instead of 12 
    
    ### To speed up the code, use dp ###
    quick_upper_products = {} #starting_value, n_products
    for i in range(1,13):
        for j in range(1,13):
            quick_upper_products[i * 13 + j] = upper_products(i,j)
    for j in range(1,78):
        quick_upper_products[78 * 13 + j] = upper_products(78,j)
    
    
    small_factorials = {}
    for i in range(1, 13):
        small_factorials[i] = factorial(i)
    ####################################
    
    result = [0] * 13

    ### Results calculated analytically
    result[0] = 1./78.
    result[11] = 0.09685058233819921 #(factorial(12)/factorial(24) + 1 / 13) * (factorial(21) / factorial(10) + factorial(20) / factorial(9) + factorial(19) / factorial(8)  + factorial(18) / factorial(7) + factorial(17) / factorial(6)  + factorial(16) / factorial(5) + factorial(15) / factorial(4)  + factorial(14) / factorial(3) + factorial(13) / factorial(2)  + factorial(12) / factorial(1) + 1)
    result[12] = 1./13. 
    
    if single_round == True:
        first_round = rounds
    else:
        first_round = 1
    
    for i in range(first_round, rounds + 1):

        start = time.time()

        combs = combinations_with_replacement_and_selection(reversed_letters, i, max_count_letter)
        factorial_factor = factorial(i)
        
        for c in combs:

            counter_c = Counter(c)

            prod = factorial_factor
            for letter in set(c):
                prod *= quick_upper_products[13 * counter_figurines[letter] + counter_c[letter]] / small_factorials[counter_c[letter]]
            
            result[max(counter_c.values())] += prod / quick_upper_products[13 * 78 + i + 1] #1015 = 13 * 78 + 1 = 1015
            
        end = time.time()
        
        print("Time for round", i, ": ", round(end - start,2))
        print(["{0:0.8}".format(float(val)) for val in result])
        print("======================================================")
        f.write(str(i) + "," + str(round(end - start,2)) + "\n")
        
    f.close()
    return result

if __name__ == '__main__':
    print("Begin!")
    result = calculate_expected_frequencies(rounds = 75, single_round = False)
    expected_val = 0
    for i in range(0, 13):
        expected_val += i * result[i]
    print("Expected val:", expected_val)
