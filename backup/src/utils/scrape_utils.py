from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
import pandas as pd
from urllib.parse import urljoin


# @cachetools.func.ttl_cache(maxsize=128, ttl=24 * 3600)
def get_soup_from_url(in_url, in_service, in_options):
    with webdriver.Chrome(service=in_service, options=in_options) as driver:
        driver.get(in_url)
        time.sleep(3)
        # soup = BeautifulSoup(driver.page_source, "html5lib")
        curr_soup = BeautifulSoup(driver.page_source, "html.parser")
        # user_agent = driver.execute_script("return navigator.userAgent")
        # print(user_agent)
    return curr_soup


def get_service_and_options_for_chromedriver():
    # define and get chromedriver object
    CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
    WINDOW_SIZE = "1920,1080"
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    options.add_argument('--no-sandbox')
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    return service, options


def get_already_scraped_job_ids(file_path):
    df = pd.read_excel(file_path)
    job_ids = df["job_id"].values.tolist()
    return job_ids


def update_index_file(file_path, job_ids, job_urls, html_paths):
    df = pd.read_excel(file_path)
    old_job_ids = df["job_id"].values.tolist()
    old_job_urls = df["url"].values.tolist()
    old_html_paths = df["html_file_path"].values.tolist()
    updated_job_ids = old_job_ids + job_ids
    updated_job_urls = old_job_urls + job_urls
    updated_html_paths = old_html_paths + html_paths
    new_df = pd.DataFrame(data={"job_id": updated_job_ids, "url": updated_job_urls,
                                "html_file_path": updated_html_paths})
    new_df.to_excel(file_path, index=False)


def get_urls_of_subsequent_pages(in_page_soup, parent_url):
    # results = in_page_soup.findAll(a , class_="srp-jobtuple-wrapper")
    results = in_page_soup.find("div", class_="styles_pages__v1rAK")
    urls = results.findChildren("a")
    updated_urls = [urljoin(parent_url, url.get("href")) for url in urls]
    return updated_urls


def get_all_tags(in_page_soup):
    names, texts, attributes, class_value_list, id_value_list, no_of_parents_list, parents_names_list, \
    parents_class_list = [], [], [], [], [], [], [], []
    for tag in in_page_soup.find_all():

        if (len(tag.find_all()) == 0 and tag.name != "script") or tag.name == 'p':
            # print(tag)
            names.append(tag.name)
            texts.append(tag.text)
            attribute_names = list(unpack_uneven_list_of_list(list(tag.attrs.keys())))
            attributes.append(",".join(attribute_names))

            if 'id' in attribute_names or 'class' in attribute_names:
                att_values = list(unpack_uneven_list_of_list(list(tag.attrs.values())))
                print(f"attribute names are {attribute_names}")
                print(f"attribute values are {att_values}")
                if 'id' in attribute_names:
                    try:
                        id_value = att_values[attribute_names.index('id')]
                    except:
                        id_value = ""
                else:
                    id_value = ""
                if 'class' in attribute_names:
                    try:
                        class_value = att_values[attribute_names.index('class')]
                    except:
                        class_value = ""
                else:
                    class_value = ""
            else:
                id_value, class_value = "", ""

            class_value_list.append(class_value)
            id_value_list.append(id_value)
            # att_values.append(",".join(list(unpack_uneven_list_of_list(list(tag.attrs.values())))))
            no_of_parents, parents_names, parents_class  = get_parents_details(tag)
            print()
            no_of_parents_list.append(no_of_parents)
            parents_names_list.append(parents_names)
            parents_class_list.append(parents_class)

    temp_df = pd.DataFrame(data={'name': names, "text": texts, "attribute": attributes, "class_value": class_value_list,
                                 "id_value" : id_value_list, "parents_no": no_of_parents_list,
                                 "parents_names": parents_names_list, "parents_class":parents_class_list})
    return temp_df


def get_parents_details(input_tag):
    no_of_parents = len(input_tag.find_parents())
    parents_names = [parent.name for parent in input_tag.find_parents()]
    class_values = []
    for parent in input_tag.find_parents():
        print(parent)
        att_names = list(parent.attrs.keys())
        att_values = list(parent.attrs.values())
        if 'class' in att_names:
            try:
                class_value = att_values[att_names.index('class')][0]
            except:
                class_value = "class_absent"
        else:
            class_value = "class_absent"
        class_values.append(class_value)
    return no_of_parents, ",".join(parents_names), ",".join(class_values)
    # return no_of_parents, ",".join(parents_names)


def unpack_uneven_list_of_list(input_list):
    for element in input_list:
        if isinstance(element, list):
            yield from unpack_uneven_list_of_list(element)
        else:
            yield element


if __name__ == "__main__":
    test_list = ["one", ["two", "three"], [["four", "five"], "six"], "seven"]
    out = unpack_uneven_list_of_list(test_list)
    # print(list(out))
