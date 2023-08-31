import difflib


def find_matches(list1, list2, cutoffs):
    matches = []
    list1 = set(list1)
    list2 = set(list2)

    for cutoff in cutoffs:
        for item in list1:
            match = difflib.get_close_matches(item, list2, n=1, cutoff=cutoff)
            if match:
                matches.append((item, match[0]))

        matched1, matched2 = zip(*matches) or [],[]
        list1 = list1 - set(matched1)
        list2 = list2 - set(matched2)

    return matches, list1, list2
