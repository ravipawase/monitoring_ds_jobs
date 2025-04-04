import glob
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold, train_test_split, cross_val_score
from feature_engineering import perform_feature_engineering
from sklearn.metrics import accuracy_score

# concat all files to get the final dataframe
input_files_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_data/"
excel_files = glob.glob(input_files_folder+"*.xlsx")
all_dfs = []
for file in excel_files:
    df = pd.read_excel(file, skipfooter=1).fillna("")
    all_dfs.append(df)
final_df = pd.concat(all_dfs)


# get features
feature_union = perform_feature_engineering()
out = feature_union.fit_transform(final_df)
print(out.shape)
f_names = feature_union.get_feature_names_out()
print(f_names)


