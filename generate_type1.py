"""
Example Usage:
````
$ cd /my/dataset/directory
$ synbols /path/to/this/script/basic_usage.py
```

The synbols command will launch the docker containing the fonts (and download it if necessary). It will also
mount the current directory for saving the dataset and execute this script.

Alternatively, you can mount any extra directory with the arguement `--mount-path`, and have the dataset written at this
location by changing the `dataset_path` variable to point to the appropriate location.
"""

from synbols.generate import generate_and_write_dataset, basic_attribute_sampler
import os
from synbols.fonts import LANGUAGE_MAP
from synbols.generate import *
from synbols.predefined_datasets import * 
from synbols.utils import Alphabet

def path(name):
    path = "j_datasets" #FIXME Changed to Temporary Dataset path
    return os.path.join(path, name)

n_samples = 2000
seed = 123

# Plain
language = 'english'
domains = ['plain','rotation','translation','gradient']
fonts = ['Times New Roman','Calibri']
chars = ['0','1','2','3','4','5','6','7','8','9']
#alphabet = Alphabet('custom',fonts = fonts, symbols = symbols)
#char = 'j'
#for domain in domains:

#write_generated_dataset(file_path = path(domain), ds_generator = generate_i(n_samples, set = domain, seed=seed), n_samples=n_samples)
#write_generated_dataset(file_path = path(domains[0]), ds_generator = generate_plain_dataset_alphabet(n_samples, alphabet, seed=seed),\
        #n_samples=n_samples)
write_generated_dataset(file_path = path('custom_20fonts_natural_allchars_onlygrad'), ds_generator = generate_plain_dataset_alphabet_onlygrad(n_samples, chars = chars, seed=seed),\
        n_samples=n_samples)
    # Translated
#write_generated_dataset(file_path = path('plain'), ds_generator = generate_plain_dataset_alphabet(n_samples = n_samples, alphabet=alphabet), n_samples = n_samples)