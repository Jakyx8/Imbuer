The goal of this script is to imbue a text onto a frame of a video.

Using an OpenCV's VideoCapture class a VideoCapture object is created and using pandas we load CSV file.
Time position of each frame is extracted and compared to the values in CSV file(In this case the CSV file is a two column file where one column contains a text and the other one a timestamp of a text).
The frame that is closest to the timestamp of a text is chosen as a frame that is to receive that text.
