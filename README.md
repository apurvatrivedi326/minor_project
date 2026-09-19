# PixelPress

PixelPress is a desktop application built with Python and PyQt5 for resizing images and processing entire folders of images efficiently. It is designed for quick image optimization workflows, whether you need to resize a single photo or batch-process a folder of images.

## Features

- Resize a single image by width or percentage
- Resize all images in a selected folder
- Save output in PNG, JPEG, or BMP format
- Optional black-and-white conversion
- Batch processing output stored in a dedicated `compressed_images` folder
- Clean and simple GUI interface

## Project Overview

This tool is useful for:

- reducing image size for web uploads
- preparing images for app or website use
- optimizing folders of product or gallery images
- quick lightweight image editing without a full design suite

## Tech Stack

- Python 3
- PyQt5 for the graphical interface
- Pillow (PIL) for image processing

## Project Structure

```text
pixelpress/
├── pixelpress.py
├── README.md
├── requirements.txt
└── compressed_images/
```

## Requirements

- Python 3.10 or newer
- PyQt5
- Pillow

## Installation

Open PowerShell or Command Prompt in the project folder and run:

```powershell
cd "C:\Users\apurv\OneDrive\Desktop\project\pixelpress"
python -m pip install -r requirements.txt
```

If `python` is not recognized on your system, use:

```powershell
py -3 -m pip install -r requirements.txt
```

## Run the Application

```powershell
cd "C:\Users\apurv\OneDrive\Desktop\project\pixelpress"
python pixelpress.py
```

Or with the Windows launcher:

```powershell
py -3 pixelpress.py
```

## Usage

1. Select an image or folder.
2. Choose resize mode:
   - Resize by width
   - Resize by percentage
3. Enter the desired width or percentage.
4. Choose the output format.
5. Optionally enable black-and-white conversion.
6. Click the resize or folder processing button.

## Notes

- For individual image resizing, the output is saved beside the original file.
- For folder processing, resized files are saved in a folder named `compressed_images` inside the selected directory.
- The UI is designed with a dark theme for a modern look.

## License

This project is provided for educational and personal use.

## Author

Apurv Trivedi
