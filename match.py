# gale-shapely algorithm
# given two sets of ranked preferences of the members of an opposite group
# find a stable pairing between the members of the two groups

def format_inputs(input1, input2):
    # Get inputs into formatted numerical lists and check to make sure all rankings are same size
    # Input 1
    input1_formatted = input1.strip().split(",")
    input1Ind = 0
    for ranking in input1_formatted:
        if len(ranking) != len(input1_formatted):
            raise Exception("Individual rankings are not the same size.")
        input1_formatted[input1Ind] = list(ranking.strip().upper())
        rankingInd = 0
        for member in input1_formatted[input1Ind]:
            member = ord(member) - ord('A')
            input1_formatted[input1Ind][rankingInd] = int(member)
            rankingInd += 1
            if (member not in set(range(len(input1_formatted[input1Ind])))):
                raise Exception("Invalid members detected.")
        input1Ind += 1
    # Input 2
    input2_formatted = input2.strip().split(",")
    input2Ind = 0
    for ranking in input2_formatted:
        if len(ranking) != len(input2_formatted):
            raise Exception("Individual rankings are not the same size.")
        input2_formatted[input2Ind] = list(ranking.strip().upper())
        rankingInd = 0
        for member in input2_formatted[input2Ind]:
            member = ord(member) - ord('A')
            input2_formatted[input2Ind][rankingInd] = int(member)
            rankingInd += 1
            if (member not in set(range(len(input2_formatted[input2Ind])))):
                raise Exception("Invalid members detected.")
        input2Ind += 1
    # Check to make sure each list contains the correct number of rankings
    if len(input1_formatted) != len(input2_formatted):
        raise Exception("Asymmetric number of rankings submitted.")
    # Return
    return input1_formatted, input2_formatted

def pair_members(set1, set2):
    # assume set1 is making proposals (set1 optimal, set2 pessimal)
    matches1 = [-1] * len(set1) # [-1, -1, -1, -1] -> [1, 2, 3, 0]
    matches2 = [-1] * len(set2)
    proposer = 0

    while matches1.count(-1) != 0: # repeat until all members of set 1 have a match
        if matches1[proposer] == -1: # make an offer if no current match
            proposedInd = 0
            proposed = set1[proposer][proposedInd]
            # print("proposer: " + str(proposer))
            while set1[proposer][proposedInd] == -1: # find best to propose that hasn't rejected
                proposedInd += 1
                proposed = set1[proposer][proposedInd]
            # print("proposed: " + str(proposed))
            if matches2[proposed] == -1: # accept if first offer
                # print("accept first offer")
                matches1[proposer] = proposed
                matches2[proposed] = proposer
            elif set2[proposed].index(matches2[proposed]) < set2[proposed].index(proposer): # reject if worse than current offer
                # print("reject")
                set1[proposer][set1[proposer].index(proposed)] = -1
            elif set2[proposed].index(matches2[proposed]) > set2[proposed].index(proposer): # accept if better than current offer, reject previous
                # print("accept, reject previous")
                set1[matches2[proposed]][set1[matches2[proposed]].index(proposed)] = -1
                matches1[matches2[proposed]] = -1
                matches1[proposer] = proposed
                matches2[proposed] = proposer

        proposer = (proposer + 1) % len(set1)

    return matches1

def print_pairs(g1_name, g2_name, matches_list):
    # print stable matches
    for i in range(len(matches_list)):
        print(g1_name.strip() + " " + str(chr(i + ord('A'))) + " matches with " + g2_name.strip() + " " + str(chr(matches_list[i] + ord('A'))))


def main():
    print("All members of each group must uniquely rank all members of the opposite group")
    print("The first member is each set is denoted as A, second as B, and so forth")
    print("When inputting preferences, use the format: ABC,BCA,ACB (only letters and commas)")
    print("Rankings should be input in alphabetical order within a group")
    g1_name = input("What is the type of member of the first group: ")
    g2_name = input("What is the type of member of the second group: ")
    input1 = input("Input the " + g1_name.strip() + "s' rankings: ")
    input2 = input("Input the " + g2_name.strip() + "s' rankings: ")
    format1, format2 = format_inputs(input1, input2)
    match_list = pair_members(format1, format2)
    print_pairs(g1_name, g2_name, match_list)

if __name__ == "__main__":
    main()

# Example:
# set1 = [[1, 3, 2, 0],[0, 1, 2, 3],[1, 0, 2, 3],[3, 2, 1, 0]]
# set2 = [[2, 1, 0, 3],[0, 2, 3, 1],[3, 1, 0, 2],[2, 3, 0, 1]]
# BDCA,ABCD,BACD,DCBA
# CBAD,ACDB,DBAC,CDAB
# correct pairing should be: [1, 2, 0, 3] -> [2, 0, 1, 3]

# Example 1
# CABD,DBCA,ADBC,ACBD
# BADC,BACD,DABC,ABCD

# Example 2
# ACBD,BCDA,CABD,ABCD
# DCBA,CABD,BADC,CABD


# TODO
# implement irving's algorithm
# given one set of rankings of all members in the group other than oneself
# find a stable pairing between members in the group