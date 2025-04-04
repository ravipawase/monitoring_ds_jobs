import time
from pathlib import Path
from utils.scrape_utils import get_soup_from_url, get_service_and_options_for_chromedriver, get_already_scraped_job_ids, \
    update_index_file, get_urls_of_subsequent_pages
from tqdm import tqdm

main_url_to_scrape = "https://www.naukri.com/data-science-jobs-in-pune?k=data%20science&l=pune&experience=8&nignbevent_src=jobsearchDeskGNB"
output_folder = "/home/ravindra/git_repos/monitoring_ds_jobs/data/html_dump"
index_file_path = "/home/ravindra/git_repos/monitoring_ds_jobs/data/index.xlsx"

urls_to_scrape = []
service, options = get_service_and_options_for_chromedriver()
search_result_page_soup = get_soup_from_url(main_url_to_scrape, service, options)
urls_to_scrape.append(main_url_to_scrape)
subsequent_pages_urls = get_urls_of_subsequent_pages(search_result_page_soup, main_url_to_scrape)
urls_to_scrape.extend(subsequent_pages_urls)

scraped_job_ids = get_already_scraped_job_ids(index_file_path)
curr_job_ids = []
curr_job_urls = []
curr_html_paths = []
for url in tqdm(urls_to_scrape):
    search_results_soup = get_soup_from_url(url, service, options)
    results = search_results_soup.findAll(class_="srp-jobtuple-wrapper")

    for result in results:
        job_id = int(result.get("data-job-id"))
        title_tag = result.findChild("div", class_="row1").findChild("a", class_="title")
        title = title_tag.get("title")
        job_details_url = title_tag.get("href")

        if job_id not in scraped_job_ids:
            job_details_soup = get_soup_from_url(job_details_url, service, options)
            out_file_path = Path(output_folder).joinpath(str(job_id)+".html")
            with open(out_file_path, "wt", encoding='utf-8') as file:
                file.write(str(job_details_soup))
            time.sleep(2)
            curr_job_ids.append(job_id)
            curr_job_urls.append(job_details_url)
            curr_html_paths.append(out_file_path)

update_index_file(index_file_path, curr_job_ids, curr_job_urls, curr_html_paths)