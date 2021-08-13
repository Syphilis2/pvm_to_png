# pvm_to_png
Reads a specific PVRT image file format and converts that to a PNG file.

This script is hardcoded to extract and stitch together PVRT images stored in uncompressed PVM files.  
The specific PVR format assumed is Pixel Format 06 which seems to be BGRA-8888 and Data Format 70 which seems to be Twiddled with a Moser-de Bruijn sequence.  
Each PVM file is assumed to contain 8 images of size 256x256 that are concatenated into a single image sized 512x1024.  

How to use (more or less)
1) Get all your .prs files and copy them into a folder
2) Use the Puyo tool or whatever else to decompress them
3) Use the example at the bottom of the script to loop over every decompressed file in the folder and call pvm_to_png() on each file
4) I guess that's it, PNGs should be in the output directory
