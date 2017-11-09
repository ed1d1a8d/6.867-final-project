import os, sys
import numpy

# Distribution of data
trainAmt = 0.40
cvAmt = 0.30
testAmt = 0.30

# Open a file
path = "/Users/nicholasguo/Downloads/voxceleb1_wav" # TODO change this to whatever you need
names = os.listdir( path )
names = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def numFiles(name):
    return len(os.listdir(path + '/' + name))

list.sort(names, key = numFiles, reverse = True) # sort by num files for each person

train = []
cv = []
test = []

for i in range(0,10): # gives top 10 people most files
    name = names[i]
    files = os.listdir(path + '/' + name)
    for j in range(0, int(trainAmt * len(files))):
        train.append((name,files[j]))
    for j in range(int(trainAmt * len(files)), int((trainAmt + cvAmt) * len(files))):
        cv.append((name,files[j]))
    for j in range(int((trainAmt + cvAmt) * len(files)), len(files)):
        test.append((name,files[j]))
    #print(name, len()) # this is to display metrics for each person ie #files, etc

print(train)
print(cv)
print(test)

# returned pairs of (person, file). Path of file is (path + '/' + name + '/' + file)
