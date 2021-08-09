# Color sorter for images
This is a Python mini project that works as a CLI tool for sorting images
based on an average color. There are two possible forms of inputs: real images
and generated images. Source images are then sorted and send to newly created
directory structure based on their average color. The tool is using OpenCV
Python library.

## Usage
For real images sorting we are using following command with PATH argument
representing the location of folder with real images.
```
$ ./cli.py use-existing [-h] [--path PATH] [--debug]
```

If we want large amount of input images we can generate them using
the following command. Images are generated as copies of prototype image
with modified colors.
```
$ ./cli.py generate [-h] [--count COUNT] [--filename FILENAME]
                       [--path PATH] [--debug]
```

## Dependencies
All dependencies can be installed with
```
$ pip install -r requirements.txt
```

## Testing
All unit tests are available in the `tests/` directory and can be run using:
```
$ python3 -m unittest discover tests
```
