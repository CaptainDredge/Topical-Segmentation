import re
import glob

def remove_no(path = '/home/ubuntu/text-segmentation/data/Dataset/training-data/'):
    for files in glob.glob(path+ '*.txt'):
    with open(files,  "r+") as f:
        data = f.read()
        output = re.sub(r'^\d+\s+', '', data,0, re.MULTILINE)
        f.seek(0)
        f.write(output)
        f.truncate()