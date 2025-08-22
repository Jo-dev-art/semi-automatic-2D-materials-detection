import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

CURRENT_IMAGE = None

class InteractiveSelector:
    def __init__(self, image_path):
        self.im = Image.open(image_path)
        self.A = np.array(self.im)
        self.selected_points = []
        self.selected_points_color = []
        self.max_clicks = 1
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
            '''
            print(f"Click {len(self.selected_points)}: Position ({x}, {y}), RGB: {rgb}")
            print(f"Clicks remaining: {clicks_remaining}")
            '''
            # Stop after 15 clicks
            if len(self.selected_points) >= self.max_clicks:
                '''    
                    print("\n15 clicks reached! Stopping selection...")
                    
                '''
                
                plt.close(self.fig)
                self.organize_rgb_ranges()
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
        
        '''
        print(f"\n=== RGB ANALYSIS FROM {len(self.selected_points)} CLICKS ===")
        print(f"Selected RGB values:")
        
        for i, (x, y, rgb) in enumerate(self.selected_points):
            print(f"  Click {i+1}: ({x}, {y}) -> RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")
        '''
        # Organize by R, G, B channels
        channel_names = ['Red (R)', 'Green (G)', 'Blue (B)']
        rgb_ranges = {}
        
        '''
        print(f"\n=== RGB CHANNEL RANGES (tolerance = ±{tolerance}) ===")
        '''
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
            
            '''
            print(f"{channel_names[channel]}:")
            print(f"  Raw range: {channel_values.min()} - {channel_values.max()}")
            print(f"  With tolerance: {min_val} - {max_val}")
           
            print(f"  All values: {sorted(channel_values)}")
            print()
            '''
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
       
        
        np.save(f".\conditions\{CURRENT_IMAGE.split('.')[0]}-conditions.npy", conditions)
        return conditions, rgb_ranges


# new function
def process(image_path):
    selector = InteractiveSelector(image_path)
    print("Click 1 point inside any of monolayers")
    points = selector.select_target_region()

# Usage example
if __name__ == "__main__":
    for file in os.listdir('images'):
        CURRENT_IMAGE = file
        process('images\\' + file)
