import os


def get_first_file(dir_name, prefix):
    """
    Looks for first file in dataset. Returns it.

    Parameters
    ----------
    dir_name : string
        The name of the directory where the desired files are located.
    prefix : string
        Prefix common to all files to be packed.

    Returns
    ------- 
        Name of first file.
    """
    files_lst = [file for file in os.listdir(dir_name) if file.startswith(prefix)]
    files_lst.sort()
    return files_lst[0]


def create_image(dir_name, prefix):
    """
    Creates image which will represent dataset. Uses adxv linux programm.

    Parameters
    ----------
    dir_name : string
        The name of the directory where the desired files are located.
    prefix : string
        Prefix common to all files to be packed.
    
    Returns
    ------- 
        Name of created file.
    """
    created_image_name = 'diff-image-thumb.jpeg'
    first_file = get_first_file(dir_name, prefix)
    print(first_file)
    os.system('adxv -jpeg_quality 100 -sa {} {}'.format(first_file, created_image_name))

    return created_image_name