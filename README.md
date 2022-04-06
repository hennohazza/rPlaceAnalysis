# rPlaceAnalysis
Code showing analysis of r/place colour change (though can be more!)

Data is retrieved from here https://rplace.space/combined/
unfortunately the start of the canvas appears to missing. Also the date appears to be upload time not time it was taken. Else it would be have been good to add a timestamp to the figures. 

As total downloaded images is 16gb (>10k images), I'm not uploading them. Script '1_Retieve_Data.py' will get them for you though! 

# Creating a movie
I tried a couple of methods to put the graph slideshow together. PIL has Gif making functionality, however the gifs were massive. Resizing the graphs didnt help much, nor did dropping every other/3rd/5th frame etc >:(

Eventually I settled on the simple command line tool FFMPEG. Running the command below made a video from the images;

ffmpeg -framerate 60 -pattern_type glob -i '*.png' rPlace_ColourChange.mp4

https://ffmpeg.org/ffmpeg.html
