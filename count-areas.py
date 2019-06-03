import time
import count
import argparse

# Start a timer
start_time = time.time()

# Setup arguments of this code
parser = argparse.ArgumentParser(description='Counting coloured areas in an image. The default shape is 256*256 and the default number of processes using is 2.')
parser.add_argument('file', type=str, help='Input a binary file')
parser.add_argument('--shape', type=str, help='Input height and width')
parser.add_argument('--process',type=int, help='Input number of processes')
args = parser.parse_args()
c=count.Count()

# Print the amounts of coloured areas
if (args.shape):
    print (c.apply(args.file,int(args.shape.split(',')[0]),int(args.shape.split(',')[1]),args.process))
else:
    print (c.apply(args.file,256,256,2))

# Stop and display the timer
elapsed_time = time.time() - start_time
print('Duration:',time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
