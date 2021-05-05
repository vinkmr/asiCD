Steps to obtain labels and images for image segmentation using lablme

Pre-requisites :

https://github.com/wkentaro/labelme#requirements

## Procedure:

1. Launch the labelme gui after installation with the command ```labelme``` in a terminal
2. Navigate to the folder containing images to be labelled.
3. Click on "Create polygons".
4. Draw the bounding area by drawing a contour by clicking to add vertices.
5. Enter a label for the marked area.
6. Click on save, to generate a json file describing the marked area.
7. Click on next Image to move to new image.
8. Repeat above steps for other images.
9. Download labelme2voc.py from here : https://github.com/wkentaro/labelme/tree/master/examples/semantic_segmentation
10. Call the downloaded python script as a module in a terminal. Provide folder containing the json files as input and a suitable output directory. The output directory will be created if it doesn't exist (Might need to provide absolute paths on windows). A text file containing label names must also be provided. ('__ignore__' must be the first label)