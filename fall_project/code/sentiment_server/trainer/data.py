"""
    Get data sets. Both train set and test set.
    Default factor for train set is 3/4. 

    E.g. on a set of 2000 entries, 1500 is used for training and 500 for testing. 
"""

def get_test_set(dataset, factor_of_train = 3/4):
    pass

def get_train_set(dataset, factor = 3/4):
    pass

def get_data_set(filename):
    pass

def get_complete_set(filename):
    data = get_data_set(filename)

    return [get_train_set(data), get_test_set(data)]