import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
from pathlib import Path
from scipy.ndimage import label

CURRENT_IMAGE = None

class InteractiveSelector:
    def __init__(self, image_path):
        self.im = Image.open(image_path)
        self.A = np.array(self.im)
        self.selected_points = []
        self.selected_points_color = []
        self.max_clicks = 15
        self.fig = None
        self.ax = None
       
    def onclick(self, event):
        if event.inaxes and len(self.selected_points) < self.max_clicks:
            x, y = int(event.xdata), int(event.ydata)
            rgb = self.A[y, x]
            self.selected_points.append([x, y, rgb])
                       
            # Mark the clicked point on the image
            self.ax.plot(x, y, 'r+', markersize=10, markeredgewidth=2)
            self.fig.canvas.draw()
           
            clicks_remaining = self.max_clicks - len(self.selected_points)
      
            # Stop after 15 clicks
            if len(self.selected_points) >= self.max_clicks:
                '''    
                    print("\n15 clicks reached! Stopping selection...")
                   
                '''
               
                plt.close(self.fig)
                self.organize_rgb_ranges()
                masking(self.im)
                points = []
                colors = []
         
           
    def select_target_region(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.imshow(self.A)
        self.ax.set_title(f'Click target regions (0/{self.max_clicks} clicks - Close window or reach {self.max_clicks} clicks to finish)')
       
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()
       
        return self.selected_points
   
    def organize_rgb_ranges(self, tolerance=1):
        """Organize the RGB ranges after 15 clicks"""
        if not self.selected_points:
            print("No points selected!")
            return None
           
        # Extract RGB values from all selected points
        rgbs = np.array([point[2] for point in self.selected_points])
       
      
        # Organize by R, G, B channels
        channel_names = ['Red (R)', 'Green (G)', 'Blue (B)']
        rgb_ranges = {}
       
       
        for channel in range(3):
            channel_values = rgbs[:, channel]
            min_val = max(-1, channel_values.min() - tolerance)
            max_val = min(255, channel_values.max() + tolerance)
           
            rgb_ranges[channel_names[channel]] = {
                'raw_min': channel_values.min(),
                'raw_max': channel_values.max(),
                'range_min': min_val,
                'range_max': max_val,
               
            }
           
         
        # Generate conditions in your original format
        conditions = []
        for channel in range(3):
            min_val = rgb_ranges[channel_names[channel]]['range_min']
            max_val = rgb_ranges[channel_names[channel]]['range_max']
           
            conditions.append([channel, 1, min_val])   # Lower bound
            conditions.append([channel, -1, max_val]) # Upper bound
       
        print("=== GENERATED CONDITIONS ===")
        print("Conditions format: [channel, direction, threshold]")
        print(f"Conditions: {conditions}")
       
       
        np.save("conditions.npy", conditions)
        return conditions, rgb_ranges

def masking(im):
    A = np.array(im).transpose((2,0,1)) #RGB chaneels from(heigh, width, channel) to (channel, heigth, width) A[0]=R A=[1]=G A=[2]=B
    structure = np.ones((3, 3), dtype=int)

 

    #%%
    conditions=np.load("conditions.npy")
    print(conditions)

    F=np.ones_like(A[0]) #Color filter mask
    for cond in conditions:
        F=np.logical_and(cond[1]*A[cond[0]]>cond[1]*cond[2],F) #creat binary mask
    
    plt.figure()
    plt.imshow(F)

    #%%
    labeled, ncomponents = label(F, structure)
 ####
    unique,counts = np.unique(labeled, return_counts=True)
    count_list=np.array([unique,counts])
    count_list=count_list[:,np.argsort(counts)][:,::-1] #Choose count_list[0.1],argsort from small to big, [:,::-1] is inverse sort from big to small

    B=np.where(labeled==count_list[0,1],1,0) #Final result
    plt.figure()
    plt.imshow(B)

# Usage example
if __name__ == "__main__":
    # Update the path to your image
    image_path = r"C:\Users\po75quv\Downloads\Figure_1.png"  # Change this to your image path
   
    selector = InteractiveSelector(image_path)
    points = selector.select_target_region()

  
