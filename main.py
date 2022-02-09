import argparse
import pyDataverse
import create_dataset_main
import compres_files_main
import send_files_main
from tools import *
from compres import *

# pyinstaller main.py -F -n dataverse_tools

CONNECTION_CODES = {
    200: "OK",
    403: "Bad api token",
}

DOI_URL = "https://mxrdr.icm.edu.pl/dataset.xhtml?persistentId=doi:10.18150/"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-at",
    "--api_token",
    type=str,
    required=True,
    help="Your api token.",
)
parser.add_argument(
    "-f",
    "--json_file",
    type=str,
    required=False,
    help="Metadata for new dataset in json file.",
)
parser.add_argument(
    "-d",
    "--dir",
    type=str,
    required=True,
    help="Directory where script will look for data.",
)
parser.add_argument(
    "-fp",
    "--files_prefix",
    type=str,
    required=True,
    help="Common prefix for all files to be uploaded. Notice that script expects that file id will be separated by _ from common prefix, eg.: file_0001.txt file_0002.txt",
)
parser.add_argument(
    "-u",
    "--url",
    type=str,
    required=False,
    help="DOI of a dataset where zipped files will be send.",
)
parser.add_argument(
    "-m",
    "--mode",
    type=str,
    required=False,
    choices={"send", "zip", "create"},
    help="""
    Mode in which script will work:
    - send: zipps and sends files to given dataset,
    - zip: only zips files in given directory,
    - create: creates new dataset, zips files and sends them.
    """,
)

args = parser.parse_args()


def main():
    api_token = str(args.api_token).strip()

    api = NativeApi(MXRDR_PATH, api_token)

    print("Checking connection to dataverse...")
    try:
        connection_code = check_connection(api)
    except pyDataverse.exceptions.ApiAuthorizationError:
        connection_code = 403
    print("Status: " + CONNECTION_CODES[connection_code])

    if not connection_code == 200:
        print("Could not connect to dataverse!")
        return

    if not args.mode:
        zip_files_list = compres_files_main.compres_files_main(
            args.dir, args.files_prefix
        )

        user_answer = None
        while not user_answer:
            user_answer = input(
                "Do you want to \n 1) Create new dataset \n 2) Upload files to existing dataset \n 3) Exit \n (Type 1 or 2 or 3) \n"
            )

        try:
            user_answer = int(user_answer.strip())
        except Exception:
            return

        if user_answer == 1:
            json_file = None

            while not json_file:
                json_file = input("Please provide valid json file: ")

            create_dataset_main.create_dataset_main(
                api_token, args.dir, args.files_prefix, json_file, zip_files_list
            )
        elif user_answer == 2:
            url = None

            while not url:
                url = input("Please provide dataset url: ")

            dataset_url = DOI_URL + url.strip()
            send_files_main.send_files_main(
                api_token, api, args.dir, args.files_prefix, dataset_url, zip_files_list
            )
        else:
            return
    else:
        if args.mode == "create":
            try:
                args.json_file
            except Exception:
                print("JSON file was not set! Please set JSON files using -f flag.")
                return
            create_dataset_main.create_dataset_main(
                api_token, args.dir, args.files_prefix, args.json_file
            )

        if args.mode == "zip":
            compres_files_main.compres_files_main(args.dir, args.files_prefix)

        if args.mode == "send":
            try:
                args.url
            except Exception:
                print("Dataset URL was not set! Please set DOI using -u flag.")
                return
            dataset_url = DOI_URL + args.url.strip()
            send_files_main.send_files_main(
                api_token, api, args.dir, args.files_prefix, dataset_url
            )


if __name__ == "__main__":
    main()
