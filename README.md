# semi-automatic-2D-materials-detection
The goal is finding condition for monolayer, and build the data for future experiment 
Work Guide: Semi-Automatic 2D materials detection

Overview
This system is designed to automate the analysis of specific target features within material science images. The entire workflow is divided into two main scripts:

Step 1: find_cond.py (Condition Setup): This is a one-time setup script used to define the precise color range of a target feature under specific lighting conditions.

Step 2: cluster.py (Automated Analysis): This is the daily-use script that reads the pre-defined conditions to perform rapid analysis on new images.

File Descriptions and Operating Instructions
A. find_cond.py - Creating the Color Condition File
Purpose:
The sole purpose of this script is to generate a color condition file named condition.npy for a specific material type under a fixed lighting and camera setup.
When to Use (Crucial!):

When analyzing a new type of material for the first time.

When the camera settings or lighting environment have been significantly altered.

When you notice that the analysis results from cluster.py are becoming inaccurate.

Step-by-Step Guide:

Open the find_cond.py script.

Locate the IMAGE_PATH variable and change its value to the file path of your reference image.

Run the Python script.

An image window will pop up. Use your mouse to click on the target feature area within the image.

To teach the program the full color variance of the feature, click 15 times on different spots within that target area.

After the 15th click, the window will close automatically. A new file named condition.npy will be generated and saved in the same directory. The condition setup is now complete.

B. cluster.py - Running the Automated Analysis
Purpose:
To use the pre-defined condition.npy file to automatically identify and analyze features in new images.

When to Use:

For the routine analysis of a batch of samples that are of the same material type and were captured under the same conditions as the reference image.

Step-by-Step Guide:

Ensure the condition.npy file is located in the same directory as the cluster.py script.

Open the cluster.py script.

Locate the IMAGE_PATH variable and change its value to the file path of the new image you wish to analyze.

Run the Python script.

The program will execute the analysis automatically based on the conditions in condition.npy and will then display or save the results.

Important Notes & Best Practices
The Core Concept: The condition.npy file acts as the bridge between the two scripts. The accuracy of cluster.py is entirely dependent on the quality of condition.npy.
Environmental Consistency: It is crucial to ensure that all images intended for analysis are captured under lighting and camera settings identical to those used for the reference image. Any variations can lead to inaccurate results.

Troubleshooting: If the analysis from cluster.py looks incorrect, the first step is always to regenerate a new, high-quality condition.npy file using a new reference image.

File Paths: Always double-check that the image file paths are correct in the scripts to avoid errors.
