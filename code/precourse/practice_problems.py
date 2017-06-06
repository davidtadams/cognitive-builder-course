def length_of_words(word_list):
    """Return a list indicating the length of every word in word_list.
    If word_list is empty, should return an empty list.

    Parameters
    ----------
    word_list : {list} of words ({str})

    Returns
    -------
    list : {list} of {int}

    Example
    -------
    >>> length_of_words(["salumeria", "dandelion", "yamo", "doc loi", "rosamunde", \
                      "beretta", "ike's", "delfina"], "d")
    [9, 9, 4, 7, 9, 7, 5, 7]
    """
    pass

def count_match_index(numbers):
    """Return the count of the number of items
    in the list whose value equals its index.

    Parameters
    ----------
    numbers : {list} of {int}

    Returns
    -------
    int : count the number of items in 'numbers' whose value equals its index

    Example
    -------
    >>> count_match_index([0, 2, 2, 3, 6, 5])
    4
    """
    pass

def max_lists(list1, list2):
    """Return a list which contains the maximum element of each list for every index.
    list1 and list2 have the same length.

    Parameters
    ----------
    list1 : {list} of integers
    list2 : {list} of integers

    Returns
    -------
    list : for each index, maximum element of list1 and list2 at this index


    Example
    -------
    >>> A = [0, 2, 1, 5, 4]
    >>> B = [1, 1, 4, 2, 7]
    >>> max_lists(A, B)
    [1, 2, 4, 5, 7]
    """
    pass

def only_sorted(L):
    """Return only the lists from L that are in sorted order.
    Note: an empty is considered as sorted,
    so is a list with one element only.

    Parameters
    ----------
    L : list of list of integers

    Returns
    -------
    list : a list of list of integers

    Example
    -------
    >>> only_sorted([[3, 4, 5], [4, 3, 5], [5, 6, 3], [5, 6, 7]])
    [[3, 4, 5], [5, 6, 7]]
    """
    pass

def convert_to_list(d):
    """Converts a dictionary of equal length lists into a list of dictionaries.

    Parameters
    ----------
    d : {dict} whose values are {list} of equal length

    Returns
    -------
    list : whose entries are dictionaries having keys of 'd'


    Example
    -------
    >>> convert_to_list({'a': [1, 2, 3], 'b': [3, 2, 1]})
    [{'a': 1, 'b': 3}, {'a': 2, 'b': 2}, {'a': 3, 'b': 1}]
    """
    pass
