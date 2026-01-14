import pandas as pd
import glob
from pathlib import Path

newly_scraped_data_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_data/"
labelled_data_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/labelled_data/"

scraped_files = glob.glob(newly_scraped_data_folder + "*.xlsx")
labelled_files = glob.glob(labelled_data_folder + "*.xlsx")
labelled_file_names = [Path(labelled_file).name for labelled_file in labelled_files]

for scraped_file in scraped_files:
    scraped_file_name = Path(scraped_file).name
    if scraped_file_name in labelled_file_names:
        scrape_df = pd.read_excel(scraped_file)
        labelled_file_index = labelled_file_names.index(scraped_file_name)
        labelled_file = labelled_files[labelled_file_index]

        labelled_df = pd.read_excel(labelled_file)
        labels = labelled_df["label"].values.tolist()

        if len(scrape_df) - len(labels) > 0:
            extra_labels = ["dummy_label" for _ in range()]
            final_labels = labels + extra_labels
        elif len(scrape_df) - len(labels) < 0:
            final_labels = labels[0:len(scrape_df) - len(labels)]


        # print(len(scrape_df))
        # print(len(labels))
        # print(len(final_labels))
        scrape_df["labels"] = final_labels
        out_file_path = Path(scraped_file).parent.joinpath(Path(scraped_file).stem + "_labelled.xlsx")
        scrape_df.to_excel(out_file_path, index=False)
