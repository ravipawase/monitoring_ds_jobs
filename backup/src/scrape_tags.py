from pathlib import Path
from utils.scrape_utils import get_soup_from_url, get_service_and_options_for_chromedriver, get_already_scraped_job_ids, \
    update_index_file, get_urls_of_subsequent_pages, get_all_tags
from tqdm import tqdm
import pandas as pd

main_url_to_scrape = "https://www.naukri.com/data-science-jobs-in-pune?k=data%20science&l=pune&experience=8&nignbevent_src=jobsearchDeskGNB"
output_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_data"
index_file_path = "/home/ravindra/git_repos/monitoring_ds_jobs/data/scraped_index.xlsx"

urls_to_scrape = []
service, options = get_service_and_options_for_chromedriver()
search_result_page_soup = get_soup_from_url(main_url_to_scrape, service, options)
urls_to_scrape.append(main_url_to_scrape)
subsequent_pages_urls = get_urls_of_subsequent_pages(search_result_page_soup, main_url_to_scrape)
urls_to_scrape.extend(subsequent_pages_urls)
# urls_to_scrape.append('https://www.naukri.com/job-listings-pyspark-developer-iqvia-bengaluru-9-to-14-years-290824000022?src=drecomm_dashboard_profile')

scraped_job_ids = get_already_scraped_job_ids(index_file_path)
curr_job_ids = []
curr_job_urls = []
curr_html_paths = []
for url in tqdm(urls_to_scrape):
    print(f"url to scrape is {url}")
    search_results_soup = get_soup_from_url(url, service, options)
    results = search_results_soup.findAll(class_="srp-jobtuple-wrapper")

    for result in results:
        job_id = int(result.get("data-job-id"))
        if job_id not in scraped_job_ids:
            title_tag = result.findChild("div", class_="row1").findChild("a", class_="title")
            title = title_tag.get("title").replace("/", "-")
            job_details_url = title_tag.get("href")
            print(f"Job detail url is {job_details_url}")
            job_details_url_soup = get_soup_from_url(job_details_url, service, options)
            curr_df = get_all_tags(job_details_url_soup)

            # temp_df = pd.DataFrame(
            #     data={'name': names, "text": texts, "attribute": attributes, "class_value": class_value_list,
            #           "id_value": id_value_list, "parents_no": no_of_parents_list,
            #           "parents_names": parents_names_list, "parents_class": parents_class_list})
            # return temp_df


            url_df = pd.DataFrame(data={'name': ["url of page"], "text": [job_details_url], "attribute": [""],
                                        "class_value": [""],  "id_value": [""], "parents_no": [""], "parents_names": [""],
                                         "parents_class": [""] })
            final_df = curr_df._append(url_df, ignore_index=True)

            out_file_path = Path(output_folder).joinpath(title + "_" + str(job_id) + ".xlsx")
            print(out_file_path)
            final_df.to_excel(out_file_path, index=False)
            curr_job_ids.append(job_id)
            curr_job_urls.append(job_details_url)
            curr_html_paths.append(out_file_path)
    break
update_index_file(index_file_path, curr_job_ids, curr_job_urls, curr_html_paths)