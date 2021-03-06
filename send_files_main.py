import os
from compres import zip_files
from tools import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
from halo import Halo


def send_files_main(api_token, api, dir, files_prefix, url, zip_files_list=None):
    parsed_url = urlparse(url)
    DOI = parse_qs(parsed_url.query)["persistentId"][0]

    if get_dataset_id(api, DOI) == -1:
        print("Please check the DOI, dataset with given DOI does not exists!")
        return False

    if not zip_files_list:
        print("Preparing files...")
        zip_files_list = zip_files(dir, files_prefix, files_prefix)
        print("Done")

    print("Sending zips to dataset...")
    for it, file in enumerate(zip_files_list):

        file_pos = str(it + 1) + ": " + file
        spinner = Halo(text="Uploading file #" + file_pos, spinner='dots')
        spinner.start()

        code = upload_file_to_dataset(api_token, DOI, file, "")
    
        if code == 200:
            spinner.succeed("Successful upload for file #" + file_pos)
        else:
            spinner.fail("Status: " + str(code))
    print("Done")

    print("Cleaning...")
    for file in zip_files_list:
        os.remove(file)
    print("Done")

    return True