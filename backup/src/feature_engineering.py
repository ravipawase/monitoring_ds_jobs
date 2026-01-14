from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from utils.feature_engineering_utils import HtmlTextFeatureTransformer, LengthTransformer, NumberOfElements, HashNStack
import glob


# input_files_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_data/"
# df = pd.read_excel(input_file, skipfooter=1).fillna("")

def perform_feature_engineering():
    feat_1_pipe = Pipeline([
        ("name_selector", ColumnTransformer([("selector", "passthrough", ["name"])], remainder="drop")),
        ("name_encoder", OneHotEncoder(handle_unknown='infrequent_if_exist'))
    ])

    feat_2_pipe = Pipeline([
        ("text_selector_1", ColumnTransformer([("selector", "passthrough", ["text"])], remainder="drop")),
        ("text_spl_symbol_counter", HtmlTextFeatureTransformer('spl_symbols_to_text_ratio'))
    ])

    feat_3_pipe = Pipeline([
        ("text_selector_2", ColumnTransformer([("selector", "passthrough", ["text"])], remainder="drop")),
        ("text_length_counter", LengthTransformer())
    ])

    feat_4_pipe = Pipeline([
        ("attribute_selector_1", ColumnTransformer([("selector", "passthrough", ["attribute"])], remainder="drop")),
        ("no_of_attributes", NumberOfElements())
    ])

    feat_5_pipe = Pipeline([
        ("attribute_selector_2", ColumnTransformer([("selector", "passthrough", ["attribute"])], remainder="drop")),
        ("expand_attributes", HashNStack("attribute"))
    ])

    feat_6_pipe = Pipeline([
        ("class_selector", ColumnTransformer([("selector", "passthrough", ["class_value"])], remainder="drop")),
        ("class_value_OHE", OneHotEncoder(handle_unknown='infrequent_if_exist'))
    ])

    feat_7_pipe = Pipeline([
        ("id_selector", ColumnTransformer([("selector", "passthrough", ["id_value"])], remainder="drop")),
        ("id_value_OHE", OneHotEncoder(handle_unknown='infrequent_if_exist'))
    ])

    feat_8_pipe = Pipeline([
        ("id_selector", ColumnTransformer([("selector", "passthrough", ["parents_no"])], remainder="drop"))
    ])

    feat_9_pipe = Pipeline([
        ("id_selector", ColumnTransformer([("selector", "passthrough", ["parents_names"])], remainder="drop")),
        ("expand_parents_names", HashNStack("parents_name"))
    ])

    feat_10_pipe = Pipeline([
        ("id_selector", ColumnTransformer([("selector", "passthrough", ["parents_class"])], remainder="drop")),
        ("expand_parents_names", OneHotEncoder(handle_unknown='infrequent_if_exist'))
    ])

    feature_union = FeatureUnion([
        # ("feat_1_pipe", feat_1_pipe),
        # ("feat_2_pipe", feat_2_pipe),
        # ("feat_3_pipe", feat_3_pipe),
        # ("feat_4_pipe", feat_4_pipe),
        # ("feat_5_pipe", feat_5_pipe),
        ("feat_6_pipe", feat_6_pipe)
        # ("feat_7_pipe", feat_7_pipe),
        # ("feat_8_pipe", feat_8_pipe),
        # ("feat_9_pipe", feat_9_pipe),
        # ("feat_10_pipe", feat_10_pipe)
    ])

    return feature_union

# concat all files to get the final dataframe
input_files_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_data/labelled_data/"
excel_files = glob.glob(input_files_folder+"*.xlsx")
all_dfs = []
for file in excel_files:
    df = pd.read_excel(file, skipfooter=1).fillna("")
    all_dfs.append(df)
final_df = pd.concat(all_dfs)

feature_union = perform_feature_engineering()
out = feature_union.fit_transform(df)
print(out.shape)
f_names = feature_union.get_feature_names_out()
print(f_names)


