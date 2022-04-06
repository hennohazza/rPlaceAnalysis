'''
Script to create gifs from output graphs.
Warning, gifs for me were massive. Dropping frames / resizing to tiny dims helped

Required packages ; Pillow, Pandas
'''

# import packages
import glob, os, sys
from PIL import Image
import pandas as pd
from joblib import Parallel, delayed

# read lookup dataframe - ensures correct order of the graphs 
df = pd.read_csv('image_colour_data.csv')
filenames = df['image_name'].values.tolist()
graph_ims = []
for f in filenames:
    find_file = './Graph_Ims/'+str(f)+'_mpl.png'
    if os.path.exists(find_file):
        graph_ims.append(find_file)
    del find_file
del df

def resize_image(input_image_path):
    # lazy coding here - you'll need to make the below dir 'Graph_Ims_Resized' to run
    output_image_path = input_image_path.replace('Graph_Ims', 'Graph_Ims_Resized')
    # change size if desired
    size = (400, 300)
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print('The original image size is {wide} wide x {height} high'.format(wide=width, height=height))
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    print('The resized image size is {wide} wide x {height} high'.format(wide=width, height=height))
    #resized_image.show()
    resized_image.save(output_image_path)
    
num_cores = 4
Parallel(n_jobs=num_cores)(delayed(resize_image)(i) for i in graph_ims)


resized_graph_ims = []
for f in filenames:
    find_file = './Graph_Ims_Resized/'+str(f)+'_mpl.png'
    if os.path.exists(find_file):
        resized_graph_ims.append(find_file)
    del find_file
    
# condense to every nth frame where [1::n]
resized_graph_ims = resized_graph_ims[1::3]

fp_out = "rPlace_Colour_Change.gif"

# Read all images
imgs = (Image.open(f) for f in resized_graph_ims)
# Start with first image
img = next(imgs)
# duration is time in ms for each frame
img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=10, loop=0)
