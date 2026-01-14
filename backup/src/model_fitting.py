import glob
import pandas as pd
from src.feature_engineering import perform_feature_engineering

# from sklearn.pipeline import Pipeline
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import KFold, train_test_split, cross_val_score
# from feature_engineering import perform_feature_engineering
# from sklearn.metrics import accuracy_score

# concat all files to get the final dataframe
input_files_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_data/labelled_data/"
excel_files = glob.glob(input_files_folder+"*.xlsx")
all_dfs = []
for file in excel_files:
    df = pd.read_excel(file, skipfooter=1).fillna("")
    all_dfs.append(df)
final_df = pd.concat(all_dfs)


# get features
feature_union = perform_feature_engineering()
final_pipe = Pipeline([
    ("features", feature_union),
    ("model", RandomForestClassifier(max_depth=8))
    # ("model", LogisticRegression)
])

# encode labels
le = LabelEncoder()
encoded_labels = le.fit_transform(final_df['label'])
print(encoded_labels)

folds = 3
X_train, X_test, y_train, y_test = train_test_split(final_df.drop('label', axis=1), encoded_labels, test_size=(1 / folds),
                                                    random_state=0, stratify=encoded_labels)
# cv = KFold(n_splits=(folds - 1))
# scores = cross_val_score(final_pipe, X_train, y_train, cv=cv)
# print(scores)

# final_pipe.fit(X_train, y_train)
final_pipe.fit(final_df.drop('label', axis=1), encoded_labels)
print(accuracy_score(final_pipe.predict(final_df.drop('label', axis=1)), encoded_labels))
# print(accuracy_score(final_pipe.predict(X_test), y_test))
# print(accuracy_score(final_pipe.predict(X_train), y_train))
# print(accuracy_score(final_pipe.predict(X_test), y_test))

# evaluation_df = pd.concat([X_train]) #, y_train, final_pipe.predict(X_train)])
# evaluation_df['label_name'] = list(le.inverse_transform(y_train))
# evaluation_df['label'] = list(y_train)
# evaluation_df['prediction'] = list(final_pipe.predict(X_train))
# evaluation_df.to_excel("/home/ravindra/git_repos/monitoring_ds_jobs/data/evaluation_df.xlsx", index=False)

evaluation_df = pd.concat([final_df.drop('label', axis=1)]) #, y_train, final_pipe.predict(X_train)])
evaluation_df['label_name'] = list(le.inverse_transform(encoded_labels))
evaluation_df['label'] = list(encoded_labels)
evaluation_df['prediction'] = list(final_pipe.predict(final_df.drop('label', axis=1)))
evaluation_df.to_excel("/home/ravindra/git_repos/monitoring_ds_jobs/data/evaluation_df.xlsx", index=False)
