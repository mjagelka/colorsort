# Color sorter for images
This is a Python mini project that works as a CLI tool for sorting images
based on an average color. There are two possible forms of inputs: real images
and generated images. Source images are then sorted and send to newly created
directory structure based on their average color. The tool is using OpenCV
Python library for image processing.

## Usage
### Running from command line
For real images sorting we are using following command with PATH argument
representing the location of folder with real images. `sample` folder contains
some testing images and is used as default.
```
$ ./cli.py use-existing [-h] [--path PATH] [--debug]
```

If we want large amount of input images we can generate them using
the following command. Images are generated as copies of prototype image
with modified colors.
```
$ ./cli.py generate [-h] --count COUNT [--filename FILENAME]
                       [--path PATH] [--debug]
```

### Running from container
If you want to avoid installing the dependencies, you can use the
containerized version of project. For that follow these steps inside
colorsort folder:
```
$ docker pull fedora:34
$ docker build -t cs_image -f Dockerfile .
$ docker run -ti --name cs_container cs_image bash
```
The last command transfers you to the container console, from where you can
run the project directly.
```
cs_container$ ./cli.py use-existing ...
```
If you want to copy the directory structure to your host, type in the host
console:
docker cp cs_container:tmp/colorsort/colors colors

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
