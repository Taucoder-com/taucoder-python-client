# Official Taucoder Python Client

[Taucoder](https://taucoder.com) python client.

## Prerequisites

- Python 3.x
- `requests` library

You can install the required library using pip:

```sh
pip install requests
```

## Installation

Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/yourusername/taucoder-client.git
cd taucoder-client
```

## Usage

### Command line options

- `--apikey` your TauCoder API key
- `--input` list of input image files
- `--output` output for the processed images. Must be an existing directory

## Example

The following example encodes input images are stores them into a directory `./output`

```sh
python taucoder-client.py --apikey YOUR_API_KEY --input image1.jpg image2.png --output ./output
```

## Licence

This project is licensed under the MIT License.
