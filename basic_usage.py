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


def path(name):
    path = "gen_datasets" #FIXME Changed to Temporary Dataset path
    return os.path.join(path, name)

n_samples = 5000
seed = 123


languages = ['arabic', 'bangla', 'greek', 'english', 'gujarati', 'hebrew', \
    'japanese', 'khmer', 'malayalam', 'russian', 'tamil', 'telugu', 'thai', 'vietnamese', 'chinese']


for language in languages:

    # Plain
    write_generated_dataset(file_path = path(language), ds_generator = generate_plain_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)
    # Translated
    write_generated_dataset(file_path = path(language+'_translated'), ds_generator = generate_plain_translated_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)
    # Rotated
    write_generated_dataset(file_path = path(language+'_rotated'), ds_generator = generate_plain_rotated_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)
    # Scaled
    write_generated_dataset(file_path = path(language+'_scaled'), ds_generator = generate_plain_scaled_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)
    # Bold
    write_generated_dataset(file_path = path(language+'_bold'), ds_generator = generate_plain_bold_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)   
    # Italic
    write_generated_dataset(file_path = path(language+'_italic'), ds_generator = generate_plain_italic_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)   
    # Gradient
    write_generated_dataset(file_path = path(language+'_gradient'), ds_generator = generate_plain_gradient_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)   
    # Natural
    write_generated_dataset(file_path = path(language+'_natural'), ds_generator = generate_plain_natural_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)   
    # Camouflage
    write_generated_dataset(file_path = path(language+'_camouflage'), ds_generator = generate_plain_camouflage_dataset(n_samples, language, seed=seed),\
        n_samples=n_samples)   

