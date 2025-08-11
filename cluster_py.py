import numpy as np

from scipy.ndimage import label
from PIL import Image
import matplotlib.pyplot as plt

im=Image.open(r'Y:/Gufos/Users/Jean/JEAN/WSe2_sequre.PNG.jpg')
A = np.array(im).transpose((2,0,1)) #RGB chaneels from(heigh, width, channel) to (channel, heigth, width) A[0]=R A=[1]=G A=[2]=B
structure = np.ones((3, 3), dtype=int) 

'''
for n in range(3):
    plt.figure()
    plt.imshow(A[n])
    plt.colorbar()
'''    


#%%
conditions=np.load("conditions.npy")
print(conditions)

F=np.ones_like(A[0]) #Color filter mask
for cond in conditions:
    F=np.logical_and(cond[1]*A[cond[0]]>cond[1]*cond[2],F) #creat binary mask
'''   
plt.figure()
plt.imshow(F) #you can check the original channel connection
'''
#%%
labeled, ncomponents = label(F, structure)

unique,counts = np.unique(labeled, return_counts=True)
count_list=np.array([unique,counts])
count_list=count_list[:,np.argsort(counts)][:,::-1] #Choose count_list[0.1],argsort from small to big, [:,::-1] is inverse sort from big to small

B=np.where(labeled==count_list[0,1],1,0) #Final result
plt.figure()

plt.imshow(B)

