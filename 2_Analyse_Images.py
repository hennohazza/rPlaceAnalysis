'''
Script to analyse r/place images.

Basic process is to iterate through images and open as arrays. 
This allows oppertunity for lots of analysis options! I went with colour percentage, but can be anything you want. 

Required packages ; Pillow, Matplotlib, Pandas
'''

#import packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys, os, glob
import PIL
import pandas as pd
from colormap import rgb2hex
from joblib import Parallel, delayed

# Create a lookup dataframe of image colour info. Saves opening an image each time.
def create_lookup_dataframe(images, outdf):
    for i, im in enumerate(images):
        print('Getting Image data for {}/{}'.format(i+1,len(images)))
        i = i+1
        # Open Image
        img = PIL.Image.open(im)
        # Handily, PIL has a count colours function builtin! 
        # Warning, using .convert('RGB') to RGB will mean it confuses black with transparent
        colors = img.getcolors()

        # if first item ; construct dataframe
        if i == 1:
            colnames = [str(x[1]) for x in colors]
            # add image index 
            colnames.insert(0, 'Image')
            colourinfo_df = pd.DataFrame(columns=colnames)
            del colnames

        # append image index
        colourinfo_df.append({'Image':i}, ignore_index=True)
        
        row = [i]
        # Get data as list from colors. comes as (count, (r,g,b))
        data = [str(x[0]) for x in colors]
        # Insert Image index as first item
        data.insert(0,os.path.basename(im)[:-4])
        colnames = [str(x[1]) for x in colors]
        # insert column name
        colnames.insert(0,'image_name')
        # write out
        newrow = pd.DataFrame([data], columns=colnames)
        colourinfo_df = colourinfo_df.append(newrow)

        del i, im, img, colors, row, data, colnames, newrow
    # fill empty cells with 0
    colourinfo_df = colourinfo_df.fillna(0)
    # write out
    colourinfo_df.to_csv(outdf)
 
# Script to create graphic output. Output Dir is '/Graph_Ims/'
def CreateGraphic(inIm):
    # Get basename of image
    basename = os.path.basename(inIm)[:-4]
    print('Processing {}'.format(basename))
    
    # match basename to dataframe to extract image data
    rowdata = df.loc[df['image_name'] == int(basename)]
    # Get row index
    image_n = rowdata['Image'].values[0]
    # now drop unecessary cols. (0, 0, 0, 0) is the transparent pixels
    rowdata = rowdata.drop(columns=['image_name', 'Image', '(0, 0, 0, 0)'])
    # Get hex names (easier for matplotlib / I was going to label them but thought against it)
    hexnames = []
    for i in rowdata.columns.values.flatten().tolist():
        # convert string to tuple
        cd_tup = eval(i)
        # calc hex and append
        hexnames.append(rgb2hex(cd_tup[0],cd_tup[1],cd_tup[2]))
        del i, cd_tup
    # Get colour data as list
    color_data = []
    for i in rowdata.values.flatten().tolist():
        color_data.append(i)
        del i

    # Draw first subplot using plt.subplot
    plt.subplot(1, 2, 2)
    # Went with horozontal bar chart, thought pie was nicer though and incorperated the later colours
    #plt.barh(hexnames,color_data, color=hexnames, edgecolor='black')
    plt.pie(color_data, colors=hexnames, wedgeprops = {'linewidth' : 0.5 , 'edgecolor' : 'black'} )
    plt.xlabel('Pixel Colour Percentage')
    
    # Draw second plot with image 
    plt.subplot(1, 2, 1)
    # easy to plot as 1 line!
    plt.imshow(PIL.Image.open(inIm))
    # turned off the axis ticks - can also turn off axis too!
    #plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    # style
    plt.suptitle("r/place Colour ({}/10411)".format(image_n), fontsize=14)
    plt.tight_layout()
    # recommend playing with the DPI/plot size. 10k images can get large!
    plt.savefig('/Graph_Ims/{}_mpl.png'.format(basename), dpi=250)
    #plt.show()
    del basename, rowdata, image_n, hexnames, color_data
    
    
images = sorted(glob.glob('/Ims/*.png'))
create_lookup_dataframe(images, 'image_colour_data.csv')

# parralel processing made the graph making MUCH QUICKER!
num_cores = 4
Parallel(n_jobs=num_cores)(delayed(CreateGraphic)(i) for i in images)


