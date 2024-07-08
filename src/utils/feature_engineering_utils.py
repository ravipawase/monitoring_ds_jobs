from sklearn.base import BaseEstimator, TransformerMixin
import string
import collections as ct
import numpy as np


def get_spl_symbols_to_text_ratio(input_text):
    if len(input_text) == 0:
        return 0
    else:
        input_text = str(input_text)
        text_length = len(input_text)
        count_of_spl_symbols = sum(v for k, v in ct.Counter(input_text).items() if k in string.punctuation)
        return round((count_of_spl_symbols / text_length) * 100, 2)


class HtmlTextFeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, name):
        self.name  = name

    def fit(self, X, y=None):
        return self  # The fit method typically does nothing for transformers

    def transform(self, X):
        X_transformed = X.copy()
        # X_transformed  = X_transformed.flatten()
        # X_transformed  = list(X_transformed)
        # X_transformed = [get_spl_symbols_to_text_ratio(element_string) for element_string in X_transformed]
        X_transformed = np.vectorize(get_spl_symbols_to_text_ratio)(X_transformed)
        return X_transformed

    def get_feature_names_out(self, X):
        return [self.name]


class LengthTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self  # The fit method typically does nothing for transformers

    def transform(self, X):
        X_transformed = X.copy()
        # X_transformed = X_transformed.flatten()
        # X_transformed = list(X_transformed)
        # X_len = [len(element_string) for element_string in X_transformed]
        X_len = np.vectorize(len)(X_transformed)
        return X_len

    def get_feature_names_out(self, X):
        return ['length']


def split_n_find_length(input_string):
    input_string_list = input_string.split(",")
    list_length = len(input_string_list)
    return list_length


class NumberOfElements(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self  # The fit method typically does nothing for transformers

    def transform(self, X):
        X_transformed = X.copy()
        X_len = np.vectorize(split_n_find_length)(X_transformed)
        return X_len

    def get_feature_names_out(self, X):
        return ['no_of_elements']


# def hash_and_stack(input_string, max_length=5):
#     input_string_list = input_string.split(",")
#     if len(input_string_list) == 0:
#         return [0] * max_length
#     else:
#         hashed_values = [np.array(hash(value)) for value in input_string_list]
#         hashed_values = hashed_values[0:max_length]
#         hashed_values = hashed_values + [ np.array([0]) for _ in range(0, (max_length - len(hashed_values)))]
#         print(hashed_values)
#         return np.asarray(hashed_values, dtype="object")
#


def hash_and_stack(input_array, max_length=5):
    output_list = []
    for row in input_array:
        input_string = row.tolist()[0]
        input_string_list = input_string.split(",")
        if len(input_string_list) == 0:
            return [0] * max_length
        else:
            hashed_values = [hash(value) for value in input_string_list]
            # hashed_values = [3 for value in input_string_list]
            hashed_values = hashed_values[0:max_length]
            hashed_values = hashed_values + [0] * (max_length - len(hashed_values))
            # print(hashed_values)
            # return np.asarray(hashed_values, dtype="object")
            output_list.append(hashed_values)
    return np.array(output_list)


class HashNStack(BaseEstimator, TransformerMixin):
    def __init__(self, feature_name):
        self.no_of_elements = 0
        self.feature_name = feature_name

    def fit(self, X, y=None):
        return self  # The fit method typically does nothing for transformers

    def transform(self, X):
        X_transformed = X.copy()
        hashed_stack = hash_and_stack(X_transformed)
        # self.no_of_elements = hashed_stack.shape[0]
        return hashed_stack

    def get_feature_names_out(self, X):
        return [self.feature_name + "_" + str(element + 1) for element in range(0, X.shape[0])]
