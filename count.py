import numpy as np
from collections import deque
from multiprocessing import Pool

class Count(object):
   def __init__(self) :
      self.height=None
      self.width=None
      self.sorted_pixels=None
      self.sorted_image=None
      self.labels=None

   """Get nearest pixels on the vertical axis and the horizontal axis

   Args:
      height: int "The height of the image"
      width: int "The width of the image"
      pixel: 1*2 array "The coordinate of the pixel"

   Returns:
      Set
   """
   def get_neighbours(self,height, width, pixel):
      # return np.unique(np.array([[pixel[0],max(0,pixel[1]-1)],[pixel[0],min(width-1,pixel[1]+1)],[max(0, pixel[0] - 1),pixel[1]],[min(height-1, pixel[0] + 1),pixel[1]]]),axis=0)
      return set([(pixel[0],max(0,pixel[1]-1)),(pixel[0],min(width-1,pixel[1]+1)),(max(0, pixel[0] - 1),pixel[1]),(min(height-1, pixel[0] + 1),pixel[1])])

   """Count numbers of area with the same gray scale

   Args:
      index: 1*2 array "Two boundaries where pixels with the same gray scale starts and ends"

   Returns:
      1*256 array
   """
   def count_areas(self,index):
      FLAG = -2
      CHECK=1
      start_index = index[0]
      stop_index=index[1]
      fifo = deque()
      result=[0 for x in range(256)]

      # Put flags on all pixels with current scale.
      for p in self.sorted_pixels[start_index:stop_index]:
         self.labels[p[0], p[1]] = FLAG

      # Label all pixels with current scale within the same area.
      for p in self.sorted_pixels[start_index:stop_index]:
         if self.labels[p[0], p[1]] != FLAG:continue
         # Count as one new area with the current gray scale
         result[int(self.sorted_image[start_index])]+=1
         fifo.append(p)
         self.labels[p[0], p[1]] = CHECK
         
         # Find if there is a new neighbour with the current scale
         while fifo:
            q = fifo.popleft()
            # for r in neighbours[q[0],q[1]]:
            for r in self.get_neighbours(self.height,self.width,q):
               if self.labels[r[0], r[1]] != FLAG:continue
               fifo.append(r)
               self.labels[r[0], r[1]] = CHECK
      return result

   """Get the amount of the area having the same gray scale

   Args:
      file: bin file "The image represented by a binary file"
      height: int "The height of the image"
      width: int "The width of the image"

   Returns:
      1*256 array
   """
   def apply(self,file,height,width,process,maxtask):
      if process==None:process=1
      if maxtask==None:maxtask=3
      INIT = -1
      scale_indices = []
      current_scale = 0
      image= np.fromfile(file,dtype='uint8')
      total = height * width
      self.height=height
      self.width=width
      results=[]

      # Create a canva with an identical scale covered by an intial value
      self.labels = np.full((height, width), INIT, np.int32)

      reshaped_image = image.reshape(total)
      # Create coordinates of every pixel.
      pixels = np.mgrid[0:height, 0:width].reshape(2, -1).T

      # Sort coordinates by gray scale
      indices = np.argsort(reshaped_image)
      self.sorted_image = reshaped_image[indices]
      self.sorted_pixels = pixels[indices]

      # Get the boundaries of pixels with different gray scales.
      for i in range(total):
         if self.sorted_image[i] <= current_scale:continue
         if len(scale_indices)==0:
            scale_indices.append([0,i])
         else:
            last_scale_indices=scale_indices[-1][1]
            scale_indices.append([last_scale_indices,i])
         current_scale=self.sorted_image[i]
      final_scale_indices=scale_indices[-1][1]
      scale_indices.append([final_scale_indices,total])

      # Use multiprocessing to count areas
      with Pool(processes=process,maxtasksperchild=maxtask) as pool:
         results=pool.map(self.count_areas, scale_indices)

      # Aggregate all arrays in results
      return [sum(x) for x in zip(*results)]
