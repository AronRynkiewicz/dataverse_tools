from PIL import Image
import os
import PIL

IMAGE_SCALE = 0.2

def resize_img(img_name):
    """
    Resizes image, uses global IMAGE_SCALE. Overwrites existing image.

    Parameters
    ----------
    img_name : str
        Image file name to be resized.
    """
    image = Image.open(img_name)
    image = image.resize((int(IMAGE_SCALE * image.size[0]), int(IMAGE_SCALE * image.size[1])), PIL.Image.NEAREST)
    image.save(img_name, 'JPEG')



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
    files_lst = [file for file in os.listdir(dir_name) if file.startswith(prefix) and 'master' not in file]
    files_lst.sort()
    return files_lst[0]


def create_image(dir_name, prefix):
    """
    Creates image which will represent dataset. Uses adxv linux program.

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
    slabs = ''
    created_image_name = 'diff-image-thumb.jpeg'
    first_file = get_first_file(dir_name, prefix)
    created_image_dir = os.path.join(dir_name, '..')

    if first_file.endswith('.h5'):
        slabs = '-slabs 10'
    
    os.system('adxv {} -jpeg_quality 100 -sa {} {}'.format(slabs, os.path.join(dir_name, first_file), os.path.join(created_image_dir, created_image_name)))
    resize_img(os.path.join(created_image_dir, created_image_name))
    
    return os.path.join(created_image_dir, created_image_name)
