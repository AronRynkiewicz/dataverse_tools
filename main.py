from tools import *

api = NativeApi(MXRDR_PATH, API_TOKEN)
print(check_connection(api))
# get_license_info()
# data = read_from_file('dataset.json')
# data = wrapper(data)
# save_to_file('dataset.json', data)

# macromolecular_metadata = get_macromolecular_metadata(api, 'doi:10.21989/FK2/54VA1F')
# save_to_file('metadata.json', macromolecular_metadata)


# print(update_metadata('doi:10.21989/FK2/3AONMG', 'citation_metadata.json'))


# macromolecular_metadata = get_datasets_metadata(api, 'doi:10.21989/FK2/54VA1F')
# save_to_file('dataset.json', macromolecular_metadata)


# print(upload_file_to_dataset('doi:10.21989/FK2/3AONMG', 'dataset.json', 'Very short test descripton.'))
#zipFilesInDir('Nazwafolderu','nowyDir.zip','16S_D31-cyt180j_1')
print(create_dataset('dataset.json'))
