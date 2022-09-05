# pixel-correction

Plugin for correcting pixel wrongly predicted on image segmented

----------------------------------


## Installation

You can install `pixel-correction` via [pip]:

    pip install pixel-correction



To install latest development version :

    pip install git+https://github.com/hereariim/pixel-correction.git

## How does it work

First, you need a compressed file (in .zip format) were you have all your images. For a compressed file named as `input.zip`, the compressed file should be built like :

```
.
└── input.zip
    └── repository
        ├── image_1
        │   ├── im_1.JPG
        │   └── im_1_mask.JPG
        ├── image_2
        │   ├── im_2.JPG
        │   └── im_2_mask.JPG
        ├── image_3
        │   ├── im_3.JPG
        │   └── im_3_mask.JPG
        ...
        └── image_n
            ├── im_n.JPG
            └── im_n_mask.JPG
```
In repository, each image folder should have two elements : image in RGB and the segmented mask in binary image (where no-flower class is 0 and flower class is 255)


![alt text](https://github.com/hereariim/pixel-correction/blob/main/readmeimage/IMG_3330.jpg)
![alt text](https://github.com/hereariim/pixel-correction/blob/main/readmeimage/IMG_3330_mask.png)

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.


## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[file an issue]: https://github.com/hereariim/pixel-correction/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
