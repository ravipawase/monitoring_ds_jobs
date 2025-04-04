from utils.scrape_utils import get_soup_from_url, get_all_tags, get_service_and_options_for_chromedriver

curr_job_detail_url = "https://www.naukri.com/job-listings-bigdata-data-science-engineer-quantta-analytics-pvt-ltd-pune-4-to-8-years-231122500002"

service, options = get_service_and_options_for_chromedriver()
job_details_url_soup = get_soup_from_url(curr_job_detail_url, service, options)
curr_df = get_all_tags(job_details_url_soup)
