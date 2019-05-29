import numpy as np
from collections import deque

FLAG = -2
INIT = -1

"""Get nearest pixels on the vertical axis and the horizontal axis

Args:
   height: int "The height of the image"
   width: int "The width of the image"
   pixel: 2*1 array "The coordinate of the pixel"

Returns:
   Numpy array
"""
def get_neighbours(height, width, pixel):
   return np.unique(np.array([[pixel[0],max(0,pixel[1]-1)],[pixel[0],min(width-1,pixel[1]+1)],[max(0, pixel[0] - 1),pixel[1]],[min(height-1, pixel[0] + 1),pixel[1]]]),axis=0)

"""Get the amount of the area having the same gray scale

Args:
   file: bin file "The image represented by a binary file"
   height: int "The height of the image"
   width: int "The width of the image"

Returns:
   1*256 Array
"""
def apply(file,height,width):
   current_label = 0
   flag = False
   fifo = deque()
   scale_indices = []
   current_scale = 0
   start_index = 0
   result=[0 for x in range(256)]
   image= np.fromfile(file,dtype='uint8')
   total = height * width

   # Create a canva with an identical scale covered by an intial value
   labels = np.full((height, width), INIT, np.int32)

   reshaped_image = image.reshape(total)
   # Create coordinates of every pixel.
   pixels = np.mgrid[0:height, 0:width].reshape(2, -1).T
   # Coordinates of neighbour pixels for each pixel.
   # neighbours = np.array([get_neighbours(height, width, p) for p in pixels]).reshape(height,width)

   # Sort coordinates by gray scale
   indices = np.argsort(reshaped_image)
   sorted_image = reshaped_image[indices]
   sorted_pixels = pixels[indices]

   # Get the boundaries of pixels with different gray scales.
   for i in range(total):
      if sorted_image[i] > current_scale:
         current_scale=sorted_image[i]
         scale_indices.append(i)
   scale_indices.append(total)

   # Pick up areas with the same gray scale
   for stop_index in scale_indices:
      # Put flags on all pixels with current scale.
      for p in sorted_pixels[start_index:stop_index]:
         labels[p[0], p[1]] = FLAG

      # Label all pixels with current scale within the same area.
      for p in sorted_pixels[start_index:stop_index]:
         if labels[p[0], p[1]] == FLAG:

            # Count as one new area with the current gray scale
            result[int(sorted_image[start_index])]+=1
            current_label += 1
            fifo.append(p)
            labels[p[0], p[1]] = current_label
            
            # Find if there is a new neighbour with the current scale
            while fifo:
               q = fifo.popleft()
               # for r in neighbours[q[0],q[1]]:
               for r in get_neighbours(height,width,q):
                  if labels[r[0], r[1]] == FLAG:
                     fifo.append(r)
                     labels[r[0], r[1]] = current_label

      # Turn to next gray scale
      start_index = stop_index
   return result