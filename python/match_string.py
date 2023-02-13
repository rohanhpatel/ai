import string
import random as rand

match_str = input("What is the string you are trying to match? ")
rand.seed(1)
characters = string.ascii_letters + string.digits + " " + string.punctuation
gen_size = 100
num_top = int(0.2 * gen_size)
breeding_amt = int(0.15 * gen_size)
mutation_amt = int(0.1 * gen_size)
creation_amt = gen_size - mutation_amt - breeding_amt - num_top  # remaining amount
mutation_rate = 0.1


# 1. create generation
# 2. get scores for generation
# 3. select top X number of strings and "breed" them
#   3a. select 20% top scoring strings
#   3b. 15%, randomly choose two strings to breed
#   3c. 10% mutations of top scorers
# 4. repeat 1-3 until string is obtained

def create_gen(seed_list):
    ret_list = []
    if seed_list is None:
        for i in range(gen_size):
            ret_list.append(create())
    else:
        # do breeding and mutation as described above
        top_list = []
        for i in range(num_top):
            top_list.append(seed_list[i])
        for i in range(len(top_list)):
            ret_list.append(top_list[i])
        for _ in range(breeding_amt):
            parent_indices = rand.sample(range(num_top), 2)
            ret_list.append(breed(top_list[parent_indices[0]], top_list[parent_indices[1]]))
        for _ in range(mutation_amt):
            parent_choice = rand.choice(range(num_top))
            ret_list.append(mutate(top_list[parent_choice]))
        for _ in range(creation_amt):
            ret_list.append(create())
    return ret_list


# helper functions for creating new generation
def create():
    return ''.join(rand.choices(characters, k=len(match_str)))


def breed(p1, p2):
    res = ''
    for i in range(len(p1)):
        if rand.random() < 0.5:
            res += p1[i]
        else:
            res += p2[i]
    return res


def mutate(parent):
    res = ''
    for i in range(len(parent)):
        if rand.random() < mutation_rate:
            res += rand.choice(characters)
        else:
            res += parent[i]
    return res


def get_key(lst):
    return lst[1]


# main function
def main():
    main_list = None
    num_gens = 0
    while main_list is None or main_list[0] != match_str:
        main_list = create_gen(main_list)
        sorting_list = []
        for s in main_list:
            score = 0
            for c in range(len(match_str)):
                if s[c] == match_str[c]:
                    score += 1
            sorting_list.append([s, score])
        sorting_list = sorted(sorting_list, reverse=True, key=get_key)
        main_list = []
        for t in sorting_list:
            main_list.append(t[0])
        print(sorting_list[0][0] + " has a score of " + str(sorting_list[0][1]))
        num_gens += 1
    print("It took " + str(num_gens) + " generations to get the string '" + match_str + "'")

main()
