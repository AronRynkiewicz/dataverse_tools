import argparse
import pyDataverse
import create_dataset_main
import compres_files_main
import send_files_main
from tools import *
from compres import *

parser = argparse.ArgumentParser()
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
    help="Url of a dataset where zipped files will be send.",
)
parser.add_argument(
    "-m",
    "--mode",
    type=str,
    required=True,
    choices={"send", "zip", "create"},
    help="""
    Mode in which script will work:
    - send: zipps and sends files to given dataset,
    - zip: only zips files in given directory,
    - create: creates new dataset, zips files and sends them.
    """,
)

args = parser.parse_args()

ZIP_FILES_DESCRIPTION = ""


def main():
    print("Checking API TOKEN...")
    if API_TOKEN:
        api = NativeApi(MXRDR_PATH, API_TOKEN)

        print("Checking connection to dataverse...")
        try:
            connection_code = check_connection(api)
        except pyDataverse.exceptions.ApiAuthorizationError:
            connection_code = 403
            print("Bad api key!")
        print("Status: " + str(connection_code))

        if connection_code == 200:
            if args.mode == "create":
                try:
                    args.json_file
                except Exception:
                    print("JSON file was not set! Please set JSON files using -f flag.")
                    return
                create_dataset_main.create_dataset_main(
                    args.dir, args.files_prefix, args.json_file
                )

            if args.mode == "zip":
                compres_files_main.compres_files_main(args.dir, args.files_prefix)

            if args.mode == "send":
                try:
                    args.url
                except Exception:
                    print(
                        "Dataset URL was not set! Please set URL files using -u flag."
                    )
                    return
                send_files_main.send_files_main(
                    api, args.dir, args.files_prefix, args.url
                )

        else:
            print("Could not connect to dataverse!")

    else:
        print("There is not API TOKEN! Please run setup.py script!")


if __name__ == "__main__":
    main()
