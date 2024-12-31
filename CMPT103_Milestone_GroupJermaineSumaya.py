# Jermaine, Sumaya
# Programming Project - Milestone#1


from graphics import *
import pickle
from datetime import date

def options_prompt():
    """
    
    Purpose:
        Displays a menu of options for the Edmonton Transit System program.
    
    Parameters:
        None
    
    Return Value(s):
        None
    """
    
    # shows the options
    print()
    print('Edmonton Transit System')
    print('---------------------------------')
    print('(1) Load route data')
    print('(2) Load shapes data')
    print('(3) Load disruptions data')
    print('\n(4) Print shape IDs for a route')
    print('(5) Print coordinates for a shape ID')
    print('(6) Find longest shape for route')
    print('\n(7) Save routes, shapes and disruptions in a pickle')
    print('(8) Load routes, shapes and disruptions from a pickle')
    print('\n(9) Interactive Map')
    print('(0) Quit')

def option_chosen():
    """
  
    
    Purpose:
        Prompts the user to input a command and returns the selected command.
    
    Parameters:
        None
    
    Return Value(s):
        str: The command entered by the user.
    """    
    
    print()
    command_chosen = input('Enter Command: ')
    
    return command_chosen



# option_1(): the functions needed when the user chooses option 1
def option_1():
    """

    
    Purpose:
        Loads route data from a specified file or a default file. Parses data to build a dictionary
        associating route IDs with route names and shape IDs.
    
    Parameters:
        None
    
    Return Value(s):
        tuple: A dictionary (`route_info`) containing route data and the filename used.
    
    """
    global route_info
    global shape_id_route
    route_info = {}
    shape_id_route = {}
    
    
    # Get file input or use default
    file_input = input('Enter a filename: ')
    if file_input == '':
        file_input = 'data/trips.txt'
    
    try:
        with open(file_input, 'r') as file, open('data/routes.txt', 'r') as file_2:
            print(f'Data from {file_input} loaded')
            
            file.readline()  # Skipping the header of trips.txt
            file_2.readline()  # Skipping the header of routes.txt
            
            # Step through trips.txt and store route_id and shape_id
            for line in file:
                data = line.strip().split(',')
                route_id = data[0]  # Extract route_id from trips.txt
                shape_id = data[6]  # Extract shape_id from trips.txt
                
                # Store the route_id and associated shape_id
                if route_id not in shape_id_route:
                    shape_id_route[route_id] = []
                shape_id_route[route_id].append(shape_id)
            
            # Step through routes.txt to store route_name and match with route_id
            for line_1 in file_2:
                data_1 = line_1.strip().split(',')
                route_id_2 = data_1[0]  # Extract route_id from routes.txt
                route_name = data_1[3]  # Extract route_name from routes.txt
                
                # If route_id exists in shape_id_route, add the name and shape_id
                if route_id_2 in shape_id_route:
                    # Associate the route_name with its shape_ids
                    route_tuple = (route_name, shape_id_route[route_id_2])
                    
                    # If route_id exists in route_info, append the tuple if it's unique
                    if route_id_2 in route_info:
                        if route_tuple not in route_info[route_id_2]:
                            route_info[route_id_2].append(route_tuple)
                    else:
                        route_info[route_id_2] = [route_tuple]
        
    except IOError as e:
        print(f"IOError: Couldn't open {file_input}")
        
    
    
    
    
    # Return the dictionary and the filename
    
    return route_info, file_input

    
# option_2(): Function needed when user chooses option 2
def option_2():
    """
    
    
    Purpose:
        Loads shape data from a specified file or a default file. Parses data to build a dictionary
        associating shape IDs with their latitude and longitude coordinates.
    
    Parameters:
        None
    
    Return Value(s):
        tuple: A dictionary (`shape_ids_info`) containing shape data and the filename used.
    """
    global shape_ids_info
    shape_ids_info = {}
    
    
    
    # Get file input or use default
    file_input = input('Enter a filename: ')
    if file_input == '':
        file_input = 'data/shapes.txt'
    
    try:
        with open(file_input, 'r') as file:
            print(f'Data from {file_input} loaded')
            
            file.readline()    # Skipping the header of shapes.txt
            
            # Processes each line in the file
            for line in file:
                data = line.strip().split(',')  # Splits the line up
                shape_ids = data[0]     # extracts shapes id from data
                shapes_pt_lat = data[1]    # Extracts latitude from data
                shapes_pt_long = data[2]   # Extracts longitutde from data
                
                coordinates = (shapes_pt_lat, shapes_pt_long) 
                
                #initializes set if shape_id is not in dictionary 
                if shape_ids not in shape_ids_info:
                    shape_ids_info[shape_ids] = []   
                    
                shape_ids_info[shape_ids].append((coordinates))
                
                
    
    
    except IOError as e:
        print(f"IOError: Couldn't open {file_input}")    
    
    
    return shape_ids_info, file_input



   


def option_3():
    """
  
    
    Purpose:
        Loads disruption data. Stores the finis date and coordinates of disruption in a dictionary.
    
    Parameters:
        None
    
    Return Value(s):
        disruption_info, file_input
        disruption_info -> dictionary
        file_input -> string
    """        
    
    global disruption_points
    disruption_info = {}
    disruption_points = []
    
        
    file_input = input('Enter a filename: ') 
    if file_input == '':
        file_input = 'data/traffic_disruptions.txt'    
        
    try:
        with open(file_input, 'r') as file:
            print(f'Data from {file_input} loaded')
            next(file)  # Skip the header
            
            for line in file:
                line = line.strip().split(',')
                
                # Ensure we have enough columns
                if len(line) < 15:
                    continue
                
                disruption_id = line[0].strip()
                finish_date_line = line[3].strip().replace('"', '')
                disruption_point = line[-1].strip().replace('POINT (', '').replace(')', '')
                
                # Split the finish date and parse
                date_parts = finish_date_line.split()
                if len(date_parts) < 2:
                    print(f"Invalid date format for disruption ID {disruption_id}: {finish_date_line}")
                    continue
                
                month_str, day = date_parts[:2]
                day = int(day.strip(','))
                month = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                         'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}.get(month_str)
                
                # Get current year if only month and day
                year = date.today().year if len(date_parts) == 2 else int(date_parts[2])
                
                try:
                    finish_date = date(year, month, day)
                    finish_date_str = finish_date.strftime('%Y-%m-%d')
                    
                    # If ID exists, append the point; otherwise, create a new entry
                    if disruption_id in disruption_info:
                        if disruption_point not in disruption_info[disruption_id]["Points"]:
                            disruption_info[disruption_id]["Points"].append(disruption_point)
                    else:
                        disruption_info[disruption_id] = { "Finish Date": finish_date_str, "Points": [disruption_point]}
                        #disruption_point = int(disruption_point)
                        disruption_points.append((disruption_point))
                        
                        
                except ValueError:
                    print(f"Invalid date for disruption ID {disruption_id}: {finish_date_line}")
                    continue
        
    except IOError:
        print(f"IOError: Couldn't open {file_input}")
    
    #print(disruption_info)
    #print(int_numbers)
    #print(disruption_points)
    
    
  
    #
    return disruption_info, file_input




# must first load in route_info and shape_ids_info
# which can be obtained through option 1 and option 2
def option_6(route_info, shape_ids_info):
    """
  
    
    Purpose:
        In option 6, the user must be prompted for a route id. If the route id is valid, you must report back to the user the
        shape id with the longest route (longest set of coordinates).

    
    Parameters:
        route_info -> dict
        shape_ids_info -> dict
    
    Return Value(s):
        None
    
    """        
    # Ask user for the key they want to search for
    key_to_find = input("Enter route ID: ")
    
    # Try to find the value corresponding to the key
    try:
        if key_to_find in route_info:
            value = route_info[key_to_find]
            
            
            
            shape_id = value[0][1]
            shape_id = set(shape_id)
            shape_id = list(shape_id)
            
            
            
            values = []
            
            for item in shape_id:
                # finds the lenght of each shape id, which is just finding # of coordinates associated with that shape id
                len(shape_ids_info[item])
                # appends it to a empty list of the # of coordinates
                values.append(len(shape_ids_info[item]))
            
            index_of_max = values.index(max(values))
            
            # matches the index with the highest value to it's associated shape id's index
            print(f'The longest shape of {key_to_find} is shape {shape_id[index_of_max]} with {max(values)} coordinates')
            
                
    
        
        
        else:
            print('       ** NOT FOUND **')
            return None    
    except:
        print('ERROR HAS OCCURED, MAKE SURE THE REQUIRED DATA IS LOADED')
    
    

    

            
                
def option_4(route_info, file_input):
    """
   
    
    Purpose:
        Prints the shape IDs for a specific route entered by the user.
    
    Parameters:
        - route_info (dict): Dictionary containing route data.
        - file_input (str): Filename used to load route data.
    
    Return Value(s):
        None
    """    
    
    route_num = ''
    
    if not route_info or not file_input:
        print("Route data hasn't been loaded yet")
    else:
       
        
        route_num = input('Enter route: ')
        
       
        
        # error checks, if route num is not an actual key it will say to the user not found
        if route_num not in route_info:
            print('       ** NOT FOUND **') 
            return
        
        else:
            route_name_ = route_info[route_num][0][0]
            route_name_ = route_name_.replace('"','')
            
            shape_id_ = route_info[route_num][0][1]
            shape_id_ = set(shape_id_) 
            # converted it to a set to remove any duplicates
            print(f'Shape ids for route [{route_name_}]')
            for shape_i in shape_id_:
                print(f'       {shape_i}')
            
    #print(route_info)
    
    
def option_5(shape_ids_info,file_input):
    """
    
    
    Purpose:
        Prints the coordinates for a specific shape ID entered by the user.
    
    Parameters:
        - shape_ids_info (dict): Dictionary containing shape data.
        - file_input (str): Filename used to load shape data.
    
    Return Value(s):
        None
    """
    
    
    
    # Verifies if shape_id data is loaed or not
    if not shape_ids_info or not file_input:
        print("Shape ID data hasn 't been loaded yet")
        
    else:
        # Prompts user to input the shape ID
        shape_id_input = input("Enter shape ID : ")
        
        # Displays coordinates for the shape IDs with no duplicates
        if shape_id_input in shape_ids_info:
            print(f"Shape ID coordinates for {shape_id_input} are:\n")
            
            for shapes_pt_lat,shapes_pt_lon in shape_ids_info[shape_id_input]:
                print(f"({shapes_pt_lat},{shapes_pt_lon})")
        
        else:
            print('       ** NOT FOUND **')
            
    


    

    

    
def option_7(route_info, shape_ids_info,disruption_info):
    """
    
    
    Purpose:
        Saves route and shape data into a pickle file.
    
    Parameters:
        - route_info (dict): Dictionary containing route data.
        - shape_ids_info (dict): Dictionary containing shape data.
    
    Return Value(s):
        None
    """
    
    
    # Verifies that route_info, shape_ids, disruption_info are loaded
    if not route_info or not shape_ids_info or not disruption_info :
            print("Route, shape, and disruption data haven't been loaded yet.")
            return
     
    file_name = input("Enter a filename : ")
    if file_name == '':
        file_name = 'data/etsdata.p' 
    
    # Opens the file in write binary mode and pickles the data    
    try:
        with open(file_name, 'wb') as file:
            pickle.dump((route_info, shape_ids_info,disruption_info),file)
            print(f"Data structures successfully written to {file_name}")
             
             
    except:
        print(f"IOError: Couldn't save data structures to {file_name}")    


def option_8 ():
    """

    Purpose:
        Loads route,shape, and disruption data from a pickle file.
    
    Parameters:
        None
    
    Return Value(s):
        tuple: Two dictionaries (`route_info`, `shape_ids_info`) containing the loaded data.
    """
    
    
        
    file_name = input("Enter a filename : ")
    if file_name == '':
        file_name = 'data/etsdata.p'    
        
        # Opens the file in binary mode and unpickles the data
        try:
            with open(file_name, 'rb') as file:
                route_info, shape_ids_info,disruption_info = pickle.load(file)  # Loads the data back into route_info,shape ids, and disruption_info
                print(f"Routes,shapes,and disruption data structures successfully loaded from {file_name}")        
            
        except:
            print(f"IOError: Couldn't load data structures from {file_name}")         
        
   
    # add on to this regarding the option the user chooses
def option_function(command_chosen, route_info,shape_ids_info,disruption_info,file_input):
    """

    
    Purpose:
        Executes the appropriate function based on the user's selected command.
    
    Parameters:
        - command_chosen (str): Command chosen by the user.
        - route_info (dict): Dictionary containing route data.
        - shape_ids_info (dict): Dictionary containing shape data.
        - file_input (str): Filename used to load data.
    
    Return Value(s):
        tuple: Updated route_info, shape_ids_info, and file_input.
    """
    
    # calls upon the function regarding what the user has chosen
    
        
    if command_chosen == '1':
        route_info, file_input = option_1()
    
    elif command_chosen == '2':
        shape_ids_info, file_input = option_2()
        
    elif command_chosen == '3':
        disruption_info, file_input = option_3()
        
    elif command_chosen == '4':
        option_4(route_info, file_input)
        
    elif command_chosen == '5':
        option_5(shape_ids_info, file_input)
    
    elif command_chosen == '7':
        option_7(route_info, shape_ids_info,disruption_info)
        
    elif command_chosen == '8':
        option_8()
        
    elif command_chosen == '9':
        option_9(route_info, shape_ids_info)
        
    elif command_chosen == '6':
        option_6(route_info, shape_ids_info)
    
    # test runs
    #elif command_chosen == '00':
        #get_coords(route_info, shape_ids_info, check_places)
    
        
    
    return route_info,shape_ids_info, disruption_info,file_input

     

            
def main():
    """
    
    
    Purpose:
        Main function that drives the program. Displays the menu, handles user input, 
        and calls the appropriate functions based on the user's choice.
    
    Parameters:
        None
    
    Return Value(s):
        None
    """
    
   # main function, brings everything together
    route_info,shape_ids_info,disruption_info,file_input = None, None, None, None
    command_chosen = ''
    
    while command_chosen != '0':
        options_prompt()
        command_chosen = option_chosen()
        route_info,shape_ids_info,disruption_info,file_input = option_function(command_chosen, route_info,shape_ids_info, disruption_info,file_input)
        
        if command_chosen not in ('0','1','2','3','4','5','6','7','8','9'):
            print('Invalid Option')
        
        

# draws the gui for option 9 part of the project
# main function for the map, calls on all other helper functions


# GUI setup with "From" and "To" entry fields
# MAIN FUNCTION MAP - DRAW
#rounded_coordinates = draw_map(check_places, route_info, shape_ids_info, win)

def gui(route_info, shape_ids_info):
    """
  
    
    Purpose:
        Essentially just makes the window and the 'edmonton.png' as the background. The texts, text boxes and buttons are also created here.
    
    Parameters:
        route_info -> dict
        shape_ids_info -> dict
    
    Return Value(s):
        win -> GraphWin
    
    """         
    
    
    #global win
    win = GraphWin('ETS Data', 800, 920)
    win.setCoords(-113.720049, 53.393703, -113.320418, 53.657116)
    
    
          
   
    # Sets the background image to 'edmonton.png' 
    background_points = win.toWorld(800/2, 920/2)
    #background_points[0] and background_points[1]
    background = Image(Point(background_points[0], background_points[1]), "edmonton.png")
    background.draw(win)
    
    coordinate_tuples = [tuple(map(float, point.split())) for point in disruption_points]
    for x,y in coordinate_tuples:
        win.plot(x,y, 'red')
  
    

    

    
    # Create 'From' text entry field
    from_text_points = win.toWorld(130, 100)
    # from_text_points[0 - 1]
    from_text = Entry(Point(from_text_points[0], from_text_points[1]), 15)
    from_text.setFill('white')
    from_text.draw(win)
    
    # Instruction label for 'From'
    inst_from_text_points = win.toWorld(30, 100)
    #inst_from_text_points[0]
    instruction_from = Text(Point(inst_from_text_points[0], inst_from_text_points[1]), 'From:')
    instruction_from.setSize(15)
    instruction_from.setStyle('bold')
    instruction_from.draw(win)    
    
    # Create 'To' text entry field
    to_text_points = win.toWorld(130, 130)
    #to_text_points[0]
    to_text = Entry(Point(to_text_points[0], to_text_points[1]), 15)
    to_text.setFill('white')
    to_text.draw(win)
    
    # Instruction label for 'To'
    
    _points_to = win.toWorld(30 + 11,130)
    instruction_to = Text(Point(_points_to[0], _points_to[1]), 'To:')
    
    instruction_to.setSize(15)
    instruction_to.setStyle('bold')
    instruction_to.draw(win)
    
            
                
    # Create the buttons
    # get_coords(route_info, shape_ids_info, check_places)
    check_places, rounded_coordinates = button_gui(win, from_text, to_text, route_info)
    
        
    
   
      
        
    
   
        
    find_route_id(route_id_name_dict, from_text_get, to_text_get)
        
    
   
       
    
    return win

# Creates buttons for 'Search' and 'Clear'

# draws the map according to the coordinates given in the data
# ['518-14-West', '518-30-East', '518-29-East', '518-1-West', '519-87-East', '519-90-East', '519-59-West', '519-73-West', '521-51-West', '521-5-East', '521-52-West']
# ^ example of the shape_id may look like
def draw_map(check_places, route_info, shape_ids_info, win):
    """
  
    
    Purpose:
        Extracts the geographical coordinates based on the route number with the most amount of coordinates.
    
    Parameters:
        check_places -> a list of route numbers
        route_info -> dict
        shape_ids -> dict
        win -> GraphWin
    
    Return Value(s):
        
        rounded_coordinates -> list
    
    """    
    
    global rounded_coordinates
    global route_longest


    shape_coord_amount = {} 
    coordinates = []
    route_longest = ''
    # this is for shape_id:amount of coordinates
    # this is used to compare
    

    
    for key_to_find in check_places:
        if key_to_find in route_info:
            value = route_info[key_to_find]
            
            
            
            shape_id = value[0][1]
            shape_id = set(shape_id)
            shape_id = list(shape_id)
            
            
            
            values = []
            
            for item in shape_id:
                # finds the lenght of each shape id, which is just finding # of coordinates associated with that shape id
                len(shape_ids_info[item])
                # appends it to a empty list of the # of coordinates
                values.append(len(shape_ids_info[item]))
            
            index_of_max = values.index(max(values))
            shape_coord_amount[shape_id[index_of_max]] = max(values)
            route_longest = key_to_find
            # matches the index with the highest value to it's associated shape id's index
            #print(f'The longest shape of {key_to_find} is shape {shape_id[index_of_max]} with {max(values)} coordinates') 
        
        
        shape_most_coordinates = max(shape_coord_amount, key=shape_coord_amount.get)   
        if shape_most_coordinates in shape_ids_info:
                #print(f"Shape ID coordinates for {shape_most_coordinates} are:\n")
                
                for shapes_pt_lat,shapes_pt_lon in shape_ids_info[shape_most_coordinates]:
                    #print(f"({shapes_pt_lat},{shapes_pt_lon})")   
                    #coord_ = shapes_pt_lat,shapes_pt_lon
                    coordinates.append((shapes_pt_lat,shapes_pt_lon))
        
        #print(coordinates)
        rounded_coordinates = [(round(float(lat), 6), round(float(lon), 6)) for lat, lon in coordinates]
        # rounded_coords -> converts the coordinates into floats, usable for pixels
        print(rounded_coordinates)
        
        return rounded_coordinates
            
            
            
            
        
            
          
    
    
   
        
        
            
    
    
    # this is the shape with the most amount of coordinates
    
      
    #print(most_coordinates)    
  
    #print(shape_coord_amount)
                
            
        
               

    
            
    
    
                
            
    
def button_gui(win, from_text, to_text, route_info):
    """
  
    
    Purpose:
        This the main focus in regards to calling the helper functions such as plotting the points, displaying what route number is being drawn. 
        This also creates usable buttons such as Search and Clear.
        
    
    Parameters:
        win -> GraphWin
        from_text -> string
        to_text -> string
        route_info -> dict
    
    Return Value(s):
        check_places -> list
        rounded_coordinates -> list
                        
    
    """     
    
    
    rect_x1_, rect_y1_ = 30+23, 130 + 20 # Coordinates for the top-left corner of the 'Search' button
    rect_x2_, rect_y2_ = 181+23, 155 + 20  # Coordinates for the bottom-right corner
    
    rect_100 = win.toWorld(53, 150)
    rect_200 = win.toWorld(204, 175)
    
    
    rectangle = Rectangle(Point(rect_100[0], rect_100[1]), Point(rect_200[0], rect_200[1]))
    rectangle.setFill('orange')
    rectangle.draw(win)    
    
    
   
    cent_x = (rect_x1_ + rect_x2_) / 2
    cent_y = (rect_y1_ + rect_y2_) / 2
    cent_points = win.toWorld(cent_x, cent_y)
    # cent_points[0]
    
    text_search = Text(Point(cent_points[0], cent_points[1]), 'Search')
    text_search.setSize(15)
    text_search.setStyle('bold')
    text_search.draw(win)
    
    # 'Clear' button rectangle
    rectangle_1_point = win.toWorld(30+23, 130 + 20 + 40)
    rectangle_2_point = win.toWorld(181+23, 155 + 20 + 40)
    # rectangle_1_point[0]
    rectangle_1 = Rectangle(Point(rectangle_1_point[0], rectangle_1_point[1]), Point(rectangle_2_point[0], rectangle_2_point[1]))
    rectangle_1.setFill('orange')
    rectangle_1.draw(win)    
    
    text_clear_point = win.toWorld(cent_x, cent_y + 40 )
    # text_clear_point[0]
    text_clear = Text(Point(text_clear_point[0], text_clear_point[1]), 'Clear')
    text_clear.setSize(15)
    text_clear.setStyle('bold')
    text_clear.draw(win)    
    
    # Initialize output texts
    not_found = None
    drawing_route = None
    
    
    
    
    while True:
        click = win.getMouse()
        click_points = win.toWorld(click.getX(), click.getY())
    
        # If the "Search" button is clicked
        button_click_1 = win.toWorld(30+23, 181+23)
        button_click_2 = win.toWorld(130 + 20, 155 + 20)
        button_click_3 = win.toWorld(130 + 20 - 40 , 155 + 20 - 40)
        # button_click_3[0]
        
        draw_route_point = win.toWorld(cent_x, cent_y + 80)
        #draw_route_point[0]
        #button_click_1[0]
        
        # click_points[0]
        # (button_click_1[0] <= click.getX() <= button_click_1[1]) and (button_click_2[0] <= click.getY() <= button_click_2[1])
        if ( rect_100[0] <= click.getX() <= rect_100[1] ) and (button_click_2[0] <= click.getY() <= button_click_2[1]):
            if not_found:
                not_found.undraw()
            if drawing_route:
                drawing_route.undraw()
            clear_input(from_text)
            clear_input(to_text)              
            
        
            
                
        
       
        # (button_click_1[0] <= click.getX() <= button_click_1[1]) and (button_click_3[0] <= click.getY() <= button_click_3[1])
        elif (button_click_1[0] <= click.getX() <= button_click_1[1]) and (button_click_3[0] <= click.getY() <= button_click_3[1]):
            from_text_get = from_text.getText().strip()
            
            to_text_get = to_text.getText().strip()
            
            
            
            
            
            print(f'From: {from_text_get} and To: {to_text_get}')
            
            route_id_name_dict = route_dict()
            check_places = find_route_id(route_id_name_dict, from_text_get, to_text_get)
            
                            
            
            # Show the result on the window
            rounded_coordinates = draw_map(check_places, route_info, shape_ids_info, win)
            
                                
                        
            if check_places:
                                    
                
                        
                        
                               
                
                if drawing_route:
                    drawing_route.undraw()
                
               
                drawing_route = Text(Point(draw_route_point[0], draw_route_point[1]), f"Drawing route {route_longest}")
                drawing_route.setSize(12)
                drawing_route.setStyle('bold')
                drawing_route.draw(win) 

                for lat, lon in rounded_coordinates:
                    #print(rounded_coordinates)
                    win.plot(lon, lat, 'blue')                
                
                
                
                            
                
               
                
                # draw function here!
                        
             
            else:
                if not_found:
                    not_found.undraw()
                not_found = Text(Point(draw_route_point[0], draw_route_point[1]), f"NOT FOUND")
                not_found.setSize(12)
                not_found.setStyle('bold')
                not_found.draw(win)
                    
                         
            
    return check_places, rounded_coordinates
                        
            
            
            
           
                
            


def route_dict():
    """
  
    
    Purpose:
        Returns a dictionary {route number : [list of shape id's]}
    
    Parameters:
        None
    
    Return Value(s):
        route_id_name -> dict
    
    """      
    route_id_name_dict = {}
    try:
        with open('data/routes.txt', 'r') as file:
            file.readline()  # Skip the header line
            for line in file:
                data = line.strip().split(',')
                route_id = data[0]
                route_long_name = data[3]
                
                route_long_name_list = [part.strip('"') for part in route_long_name.split(' - ')]
                route_id_name_dict[route_id] = route_long_name_list
    except FileNotFoundError:
        print("Error: 'data/routes.txt' file not found.")
    
    #print(route_id_name_dict)
        
   
    return route_id_name_dict

route_id_name_dict = route_dict()
from_text_get = 'mill woods'
to_text_get = 'century park'

def find_route_id(route_id_name_dict, from_text_get, to_text_get):
    """
  
    
    Purpose:
        Based on what the user entered as 'from' and 'to' we use that to get the route number
        there may be multiple route numbers so we must check every single route number
        to compare, find which one has the longest coordinate
    
    Parameters:
        route_id_name_dict -> dict
        from_text_get -> string
        to_text_get -> string
    
    Return Value(s):
        check_places -> list
    
    """      
    check_places = []
    from_input = from_text_get
    to_input = to_text_get
    
    if from_input == '':
        for key, value in route_id_name_dict.items():
            if len(value) == 1:
                if to_input.lower() in value[0].lower():
                    check_places.append(key)
                    
    elif to_input == '':
        for key, value in route_id_name_dict.items():
            if len(value) == 1:
                if from_input.lower() in value[0].lower():
                    check_places.append(key)
                    
    else:
        for key, value in route_id_name_dict.items():
            if len(value) != 1:
                if any(from_input.lower() in place.lower() for place in value) and any(to_input.lower() in place.lower() for place in value):
                    check_places.append(key)
    
    # returns the route id, example mill woods - century park -> [521, 519, 518]
    
    return check_places

    

    


    



        


    


# Function to clear the text from entry boxes
def clear_input(entry_box):
    """
  
    
    Purpose:
        Clears the entry boxes
    
    Parameters:
        entry_box -> Other type, entry box
    
    Return Value(s):
       None
    
    """      
    
    entry_box.setText("")  # Clears the text in the entry widget



    

    
    

            
    



def option_9(route_info, shape_ids_info):
    """
  
    
    Purpose:
        Used in option_function(), basically calls in to do what option 9 does in regards to the project.
    
    Parameters:
        route_info -> dict
        shape_ids_info -> dict
    
    Return Value(s):
        None
    
    """      
    
    gui(route_info, shape_ids_info)
    

# calls the main function


main()