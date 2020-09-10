# Synbols: Probing Learning Algorithms with Synthetic Datasets

![Synbols](https://github.com/ElementAI/synbols/raw/master/cover.png)

> Progress in the field of machine learning has been fueled by the introduction of benchmark datasets pushing the limits of existing algorithms.  Enabling the design of datasets to test specific properties and failure modes of learning algorithms is thus a problem of high interest, as it has a direct impact on innovation in the field. In this sense, we introduce Synbols — Synthetic Symbols — a tool for rapidly generating new datasets with a rich composition of latent features rendered in low resolution images. Synbols leverages the large amount of symbols available in the Unicode standard and the wide range of artistic font provided by the open font community. Our tool's high-level interface provides a language for rapidly generating new distributions on the latent features, including various types of textures and occlusions. To showcase the versatility of Synbols, we use it to dissect the limitations and flaws in standard learning algorithms in various learning setups including supervised learning, active learning, out of distribution generalization, unsupervised representation learning, and object counting.

[[paper]](./coming_soon.md)

## Installation

The easiest way to install Synbols is via [PyPI](https://pypi.org/project/synbols/). Simply run the following command:

`pip install synbols`


## Software dependencies

Synbols relies on fonts and system packages. To ensure reproducibility, we provide a [Docker image](https://hub.docker.com/repository/docker/aldro61/synbols) with everything
preinstalled. Thus, the only dependency is [Docker](https://docs.docker.com/get-docker/).

## Usage

### Using predefined generators

`$ synbols-predefined --help`

```bash
$ synbols-predefined --dataset=some-large-occlusion --n_samples=1000 --seed=42`

Generating some-large-occlusion dataset. With probability 20%, add a large occlusion over the existing symbol.
Preview generated.
 18%|####################################7                      | 182/1000 [00:03<00:12, 65.95it/s
```
### Defining your own generator


Examples of how to create new datasets can be found in the [examples](examples) directory.

```python

def translation(rng):
    """Generates translations uniformly from (-2, 2), going outside of the box."""
    return tuple(rng.uniform(low=-2, high=2, size=2))


# Modifies the default attribute sampler to fix the scale to a constant and the (x,y) translation to a new distribution
attr_sampler = basic_attribute_sampler(scale=0.5, translation=translation)

generate_and_write_dataset(dataset_path, attr_sampler, n_samples)

```

To generate your dataset, you need to run your code in the Synbols runtime environment. This is done using the `synbols` command as follows:

`synbols mydataset.py --foo bar`


## Contact

For any bug or feature requests, please create an issue.
