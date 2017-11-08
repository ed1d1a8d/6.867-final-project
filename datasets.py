import os, sys

# Open a file
path = "/Users/nicholasguo/Downloads/voxceleb1_wav" # TODO change this to whatever you need
names = os.listdir( path )
names = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

for name in names:
   print(name, len(os.listdir(path + '/' + name)))d