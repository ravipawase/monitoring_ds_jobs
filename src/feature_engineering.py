from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from utils.feature_engineering_utils import HtmlTextFeatureTransformer, LengthTransformer, NumberOfElements, HashNStack
from sklearn.compose import ColumnTransformer


input_file = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_data/Analytics Data science and IOT Lead_160524502177.xlsx"
df = pd.read_excel(input_file, skipfooter=1).fillna("")


feat_1_pipe = Pipeline([
                    ("name_selector", ColumnTransformer([("selector", "passthrough", ["name"])], remainder="drop")),
                    ("name_encoder", OneHotEncoder())
            ])

feat_2_pipe = Pipeline([
                    ("text_selector_1", ColumnTransformer([("selector", "passthrough", ["text"])], remainder="drop")),
                    ("text_spl_symbol_counter", HtmlTextFeatureTransformer('spl_symbols_to_text_ratio'))
            ])

feat_3_pipe = Pipeline([
                ("text_selector_2",  ColumnTransformer([("selector", "passthrough", ["text"])], remainder="drop")),
                ("text_length_counter", LengthTransformer())
            ])

feat_4_pipe = Pipeline([
                ("attribute_selector_1",  ColumnTransformer([("selector", "passthrough", ["attribute"])], remainder="drop")),
                ("no_of_attributes", NumberOfElements())
            ])

feat_5_pipe = Pipeline([
                ("attribute_selector_2",  ColumnTransformer([("selector", "passthrough", ["attribute"])], remainder="drop")),
                ("expand_attributes", HashNStack("attribute"))
            ])

feat_6_pipe = Pipeline([
                ("class_selector",  ColumnTransformer([("selector", "passthrough", ["class_value"])], remainder="drop")),
                ("class_value_OHE", OneHotEncoder())
            ])

feat_7_pipe = Pipeline([
                ("id_selector",  ColumnTransformer([("selector", "passthrough", ["id_value"])], remainder="drop")),
                ("id_value_OHE", OneHotEncoder())
            ])

feat_8_pipe = Pipeline([
                ("id_selector",  ColumnTransformer([("selector", "passthrough", ["parents_no"])], remainder="drop"))
            ])

feat_9_pipe = Pipeline([
                ("id_selector",  ColumnTransformer([("selector", "passthrough", ["parents_names"])], remainder="drop")),
                ("expand_parents_names", HashNStack("parents_name"))
            ])


union = FeatureUnion([
                    ("feat_1_pipe", feat_1_pipe),
                    ("feat_2_pipe", feat_2_pipe),
                    ("feat_3_pipe", feat_3_pipe),
                    ("feat_4_pipe", feat_4_pipe),
                    ("feat_5_pipe", feat_5_pipe),
                    ("feat_6_pipe", feat_6_pipe),
                    ("feat_7_pipe", feat_7_pipe),
                    ("feat_8_pipe", feat_8_pipe),
                    ("feat_9_pipe", feat_9_pipe)
                    ])


out = union.fit_transform(df[0:-1])
# print(out)
# print(type(out))
print(out.shape)
f_names = union.get_feature_names_out()
print(f_names)


