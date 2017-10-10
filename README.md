The dataset this project is based on is
[VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/).

We have written a script to assist in downloading the data.
The script requires:

* Python 3.5+
* [tqdm](https://github.com/tqdm/tqdm)
* [youtube-dl](https://github.com/rg3/youtube-dl)
* [ffmpeg](https://www.ffmpeg.org/)

To use the script, you will first need to download the VoxCeleb dataset.
Then run:

```
./download.py /location/to/voxceleb1_txt /location/to/output_dir
```

Any download errors will be logged in a generated file.
