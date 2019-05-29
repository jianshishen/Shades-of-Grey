import count
import argparse

# Setup arguments of this code
parser = argparse.ArgumentParser(description='Counting coloured areas in an image. The default shape is 256*256')
parser.add_argument('file', type=str, help='Input a binary file')
parser.add_argument('--shape', type=str, help='Input height and width')
args = parser.parse_args()

# Print the amounts of coloured areas
if (args.shape):
    print (count.apply(args.file,int(args.shape.split(',')[0]),int(args.shape.split(',')[1])))
else:
    print (count.apply(args.file,256,256))
