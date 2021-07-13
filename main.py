import argparse
import ast
import os
from tools import *
from compres import *
from create_image import *


parser = argparse.ArgumentParser()
parser.add_argument(
        '-f',
        '--json_file',
        type=str,
        required=True,
        help = 'Metadata for new dataset in json file.',
    )
parser.add_argument(
        '-d',
        '--dir',
        type=str,
        required=True,
        help = 'Directory where script will look for data.',
    )
parser.add_argument(
        '-fp',
        '--files_prefix',
        type=str,
        required=True,
        help = 'Common prefix for all files to be uploaded. Notice that script expects that file id will be separated by _ from common prefix, eg.: file_0001.txt file_0002.txt',
    )

args = parser.parse_args()

ZIP_FILES_DESCRIPTION = ''

print('Creating new dataset with metadata from: ' +
        args.json_file +
        ', files from: ' + args.dir +
        ' dricractory, with common prefix: ' + args.files_prefix +
        ' and this text as desricption of all send files: ' + ZIP_FILES_DESCRIPTION
    )

api = NativeApi(MXRDR_PATH, API_TOKEN)
print('Checking connection to dataverse...')
connection_code = check_connection(api)
print('Status: ' + str(connection_code))

if connection_code == 200:
    print('Creating new dataset...')
    data = ast.literal_eval(create_dataset(args.json_file).stdout.decode("UTF-8"))
    print('Status: ' + data['status'])

    print('Preparing files...')
    zip_files_list = []

    zip_files_list.append(create_image(args.dir, args.files_prefix))
    
    zip_files_list.extend(zip_files(args.dir, args.files_prefix, args.files_prefix))
    print('Done')

    print('Sending zips to dataset...')
    for it, file in enumerate(zip_files_list):
        print('Uploading file #' + str(it))
        code = upload_file_to_dataset(data['data']['persistentId'], file, ZIP_FILES_DESCRIPTION)
        print('Status: ' + str(code))
    print('Done')

    print('Cleaning...')
    for file in zip_files_list:
        os.remove(file)
    print('Done')
else:
    print('Script could not connect to dataverse!')
