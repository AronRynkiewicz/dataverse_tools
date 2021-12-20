import ast
import os
from tools import *
from compres import *


def create_dataset_main(api_token, dir, files_prefix, json_file):
    print("Creating new dataset...")
    data = ast.literal_eval(create_dataset(api_token, json_file).stdout.decode("UTF-8"))
    print("Status: " + data["status"])

    if data["status"] == "OK":
        print("Preparing files...")
        zip_files_list = []

        zip_files_list.extend(zip_files(dir, files_prefix, files_prefix))
        print("Done")

        print("Sending zips to dataset...")
        for it, file in enumerate(zip_files_list):
            print("Uploading file #" + str(it))
            code = upload_file_to_dataset(
                api_token, data["data"]["persistentId"], file, ""
            )
            print("Status: " + str(code))
        print("Done")

        print("Cleaning...")
        for file in zip_files_list:
            os.remove(file)
        print("Done")
    else:
        print("There was a problem with dataset creation:")
        print(data)
