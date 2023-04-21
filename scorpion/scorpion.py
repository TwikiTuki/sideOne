from PIL import Image
from PIL.ExifTags import TAGS
import sys

class Scorpion():
    avoid = ['exif', 'icc_profile']
    def __init__(self, arguments):
        print('initializing')
        for image_file in arguments:
            self.print_file_meta(image_file)
    def print_file_meta(self, image_file):
        print(f'\nGETTING FILE: {image_file}')
        image = Image.open('lizard.jpg')
        for key, value in image.info.items():
            if key in self.avoid:
                continue
            print(f'  {key}: {value}')
        if ('getexif' not in dir(image)): 
            return 
        exif = image.getexif()
        first = True
        for key, value in exif.items():
            if (first):
                print("\nExif metadata")
                first = False
            data_name = TAGS[key]
            print(f'  {data_name}: {value}')

if (__name__ == '__main__'):
    scorpion = Scorpion(sys.argv[1:])


        
