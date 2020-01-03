import gzip
import os
import time
import shutil
import tempfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

def download(directory, filename):
    """Download images of filename to directory"""
    if not tf.gfile.Exists(directory):
        tf.gfile.MakeDirs(directory)
    with open(filename,'r+') as fin:
        lines = fin.readlines()
        count = 0
    for url in lines:
        count +=1
        filepath = os.path.join(directory,str(count)+'.jpg')
        if tf.gfile.Exists(filepath):
            print('processed %d image.',count)
            continue
        try:
            time.sleep(1)
            urllib.request.urlretrieve(url,filepath)
        except Exception as e:
            print('Acui what error: ',str(e))
            time.sleep(10)
        print('processing %d image.',count)

if __name__=='__main__':
    download('costa_datas','/home/acui/Downloads/costa.txt')
