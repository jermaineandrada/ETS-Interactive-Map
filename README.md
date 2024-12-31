
  
# ETS Interactive Map

## Overview  
This project allows users to visualize routes by plotting pixel-based representations using data from a provided file. The data file includes essential details such as route paths, shape IDs, and corresponding coordinates.  

## Features  
- **Plot Routes:** Input starting and ending points to visualize the path.  
- **Partial Inputs:** If only one location (starting or ending point) is provided, the program will still attempt to plot the route.  
- **Error Handling:** If the specified route is invalid, the program will notify the user that the route cannot be processed.  

## How It Works  
1. Load the data file containing route paths and shape information.  
2. Enter the starting and/or ending points.  
3. The program will validate the route and plot the points along the path if the route exists.  
4. If the route is invalid, a notification will be displayed.  

## Requirements  
- Python 3.x  
- Graphics library (if applicable)  
- Required data files (located in `data/` directory)  

## Notes  
- Ensure the data file is up to date and properly formatted.  
- Partial inputs are allowed but may yield limited results if the full route cannot be determined.  
