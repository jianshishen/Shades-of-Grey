import time
import count
import argparse

start_time = time.time()

# Setup arguments of this code
parser = argparse.ArgumentParser(description='Counting coloured areas in an image. The default shape is 256*256')
parser.add_argument('file', type=str, help='Input a binary file')
parser.add_argument('--shape', type=str, help='Input height and width')
args = parser.parse_args()
c=count.Count()

# Print the amounts of coloured areas
if (args.shape):
    print (c.apply(args.file,int(args.shape.split(',')[0]),int(args.shape.split(',')[1])))
else:
    print (c.apply(args.file,256,256))

elapsed_time = time.time() - start_time
print('Duration:',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
