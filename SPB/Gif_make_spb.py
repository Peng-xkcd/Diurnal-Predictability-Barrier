import os
import imageio
path = 'E:/gif_PB/Typhon_Tracks'
filenames = []
for files in os.listdir(path):
    if files.endswith('jpg') or files.endswith('jpeg') or files.endswith('png'):
        file = os.path.join(path, files)
        filenames.append(file)

# file = 'E:/gif_PB/'
# filenames = os.listdir(file)
images = []
for filename in filenames:
	images.append(imageio.imread(filename))
imageio.mimsave('TY_Tracks.gif', images, duration=0.5)