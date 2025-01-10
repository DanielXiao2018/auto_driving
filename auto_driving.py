# define the Field class for the simulation field
class Field:
    # Constructor method to initialize attributes
    def __init__(self, width, height):
        self.width = width                      # the width of the field
        self.height = height                    # the height of the field
        self.fleet = []                         # the list of cars to be running in the simution
        self.collided_cars = []                 # groups of collided cars
    def addCar(self, car):                      # add a new car into the fleet
        self.fleet.append(car)
    def isValidCoordinates(self, x, y):         # check whether a user-input car coordinates are within the range of the field
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True
    def isCarNameExist(self, car_name):         # to check whether user input a duplicate car name
        exist = False
        for car in self.fleet:
            if car.name==car_name:
                exist = True
                break
        return exist        
    def is_car_in_collision_group(self, car):   # check whether a car is already collided
        return_group = []
        in_group = False
        for group in self.collided_cars:
            if car in group:
                return_group = group
                in_group = True
                break
        return in_group, return_group 
    def set_mutual_collision(self, car, other): # if multiple cars have collided, then add each other into the collided-cars list, for the purpose of displaying the simulation result
        if isinstance(other, list):
            for veh in other:                   # mutual settings between a car and multiple cars in a list   
                self.set_mutual_collision(car, veh)
        else:                                   # car-to-car mutual setup
            if car==other:                      # cannot add itself
                return
            # mutually add cars into each other's collided-car-list        
            if not other in car.collided_cars_list:
                car.collided_cars_list.append(other)
            if not car in other.collided_cars_list:
                other.collided_cars_list.append(car)
    def push_car_into_collided_group(self, car1, car2): 
        # if a car is detected to collide with other car(s), push the collided car(s) into the collided-car-group
        is_in_group, collision_group = self.is_car_in_collision_group(car2)
        if is_in_group:
            collision_group.append(car1)
            self.set_mutual_collision(car1, collision_group)
        else:
            self.collided_cars.append([car1, car2])
            self.set_mutual_collision(car1, car2)
    def detectDuplicateCoordinates(self, x, y): # detect any duplication in user-input car coordinates
        res = False
        for car in self.fleet:
            if car.x==x and car.y==y:
                res = True
                break
        return res
    def detectCollision(self, myCar):           # during the simulation running, detect any car collision in each step
        for car in self.fleet:
            if myCar.name==car.name:
                continue
            if myCar.collide(car):              # if a collision is detected, set the collided flag of both cars, to stop their running
                myCar.collided = True
                car.collided = True
                self.push_car_into_collided_group(myCar, car)
    def showFleet(self, initial):               # show the status of each car in the fleet, before or after the simulation
        if initial:                             # initial: True - before the simulation; False - after the simulation     
            print("Your current list of cars are:")
        else:
            print("After simulation, the result is:")
        for car in self.fleet:                  # show the status of each individual car before or after running the simulation
            car.showStatus(initial)
        print()    
    def runFleet(self):                         # run the simulation upon the whole fleet (applied to the scenario 2: multiple cars)
        running = True
        while running:
            canRun = False
            for car in self.fleet:
                if car.isMoveable():
                    canRun = True
                    self.moveCar(car, car.commands[car.step])
                    self.detectCollision(car)    
            running = canRun        
    def runCar(self, car, commands):            # run the simulation on the scenario 1: a single car in the simulation field
        for c in range(0, len(commands)):
            self.moveCar(car, commands[c])
    def moveCar(self, car, action):             # move a single car in each step
        new_x = 0
        new_y = 0
        if action=="L":                         # turn left
            if car.direction=="N":
                car.direction = "W"
            elif car.direction=="E":
                car.direction = "N"
            elif car.direction=="S":
                car.direction = "E"
            elif car.direction=="W":
                car.direction = "S"
        elif action=="R":                       # turn right
            if car.direction=="N":
                car.direction = "E"
            elif car.direction=="E":
                car.direction = "S"
            elif car.direction=="S":
                car.direction = "W"
            elif car.direction=="W":
                car.direction = "N"
        elif action=="F":                       # going forward
            if car.direction=="N":
                new_x = car.x
                new_y = car.y + 1
            elif car.direction=="E":
                new_x = car.x + 1
                new_y = car.y
            elif car.direction=="S":
                new_x = car.x
                new_y = car.y - 1
            elif car.direction=="W":
                new_x = car.x - 1
                new_y = car.y
            if self.isValidCoordinates(new_x, new_y):
                car.x = new_x
                car.y = new_y
        car.step += 1
        
# define the Car class for each individual car
class Car:
    # Constructor method to initialize attributes
    def __init__(self, name, x, y, direction, commands):
        self.name = name                        # car name
        self.x = x                              # car x coordinates
        self.y = y                              # car y coordinates
        self.direction = direction              # car direction
        self.commands = commands                # car's running commands
        self.step = 0
        self.collided = False
        self.collided_cars_list = []
    def isMoveable(self):
        if self.step >= len(self.commands):     # a car has run out its commands
            return False
        if self.collided:                       # a car has already collided with another car, must stop
            return False
        return True
    def collide(self, anotherCar):              # to detect whether a car has collided with other car(s)
        return self.x==anotherCar.x and self.y==anotherCar.y
    def showStatus(self, initial):              # to display the current coordinates and direction of a car
        if initial:                             # display a car's initial status and to-be-run commands, before running a simulation
            print(f"- {self.name}, ({self.x},{self.y}) {self.direction}, {self.commands}")
        elif not self.collided:                 # display the coordinates and direction of a car in a normal statua (no collision), after runnig the simulation
            print(f"- {self.name}, ({self.x},{self.y}) {self.direction}")
        else:                                   # display the coordinates and direction of a car after a collision with other car(s)
            # extract the other car(s) colliding with this car
            collided_cars = ""
            for veh in range(0, len(self.collided_cars_list)):
                if veh==0:
                    collided_cars += self.collided_cars_list[veh].name
                else:
                    collided_cars += "," + self.collided_cars_list[veh].name
            print(f"- {self.name}, collides with {collided_cars} at ({self.x},{self.y}) at step {self.step}")    
def valid_input(stage, input_str):              # check whether a user input is valid in each stage
    if stage==1:                                # at the stage to input the width and height values of the field
        # Split the input string into a list of strings
        input_list = input_str.split()
        if len(input_list)!=2:
            print("You should input exactly two integers.")
            return 0, 0, False
        # Convert the strings to integers
        try:
            x = int(input_list[0])
            y = int(input_list[1])
            if x<=0 or y<=0:
                print("Both x and y must be positive integers.")
                return x, y, False
            else:
                return x, y, True
        except ValueError:
            print("Invalid input. Please enter two integers.")
            return 0, 0, False
    elif stage==2 or stage==5:                  # stage 2: select "add car" or "run simulation". stage 5: select to "start over" or "exit".      
        if not input_str in ["1", "2"]:
            print("Invalid option, please input either 1 or 2.")
            return input_str, False
        else:
            return input_str, True
    elif stage==3:                              # the stage of adding a car
        # Split the input string into a list of strings
        input_list = input_str.split()
        if len(input_list)!=3:
            print("You should input exactly 3 values.")
            return 0, 0, "", False
        # Convert the first 2 strings to integers
        try:
            x = int(input_list[0])
            y = int(input_list[1])
            if x<=0 or y<=0:
                print("Both x and y must be positive integers.")
                return x, y, "", False
            direction = input_list[2].strip()
            return x, y, direction, True
        except ValueError:
            print("Invalid input. Please enter two integers.")
            return 0, 0, False
        
def valid_commands(commands):                   # to check whether the input car commands are a valid string (only contains characters of 'L', 'F' or 'R'
    valid = True
    for c in commands:
        if not c in ["L", "F", "R"]:
            valid = False
            break
    return valid            
    
def prompt(stage):                              # to display the prompt messages for user input across all stages
    global myField
    input_ok = False
    while not input_ok:
        if stage==1:                            # user input the width and height of the simulation field    
            print("Welcome to Auto Driving Car Simulation!")
            print()
            print("Please enter the width and height of the simulation field in x y format:")
            input_str = input()
            input_str = input_str.strip()
            x, y, input_ok = valid_input(stage, input_str)
            if input_ok:
                return x, y
        elif stage==2:                          # user select the actions of either adding a car or running a simulation
            print("Please choose from the following options:")
            print("[1] Add a car to field")
            print("[2] Run simulation")
            input_str = input()
            input_str = input_str.strip()
            option, input_ok = valid_input(stage, input_str)
            if input_ok:
                if option=="2":
                    if len(myField.fleet)==0:
                        print("You have not added any car, so cannot run a simulation.")
                        input_ok = False
                    else:
                        return option
                else:
                    return option
        elif stage==3:                          # the stage of adding a car
            exist = True
            car_name = ""
            while exist:
                print("Please enter the name of the car:")
                car_name = input()
                car_name = car_name.strip()
                exist = myField.isCarNameExist(car_name)    
                if exist:                       # check the user-input car name, to avoid any duplication
                    print(f"Sorry your input car name {car_name} has already existed, please re-enter another car name.")
            duplicate = True
            while duplicate or not input_ok:    
                print(f"Please enter initial position of car {car_name} in x y Direction format:")
                input_str = input()
                input_str = input_str.strip()
                x, y, direction, input_ok = valid_input(stage, input_str)
                if input_ok:
                    if not myField.isValidCoordinates(x, y):    # the coordinates of the newly-added car must be within the range of the field
                        print(f"Sorry you input invalid coordinates ({x}, {y}) for the car {car_name}.")
                        input_ok = False
                        continue
                    duplicate = myField.detectDuplicateCoordinates(x, y)
                    if duplicate:               # to prevent any conflicting initial coordinates across all cars
                        print(f"The coordinate ({x}, {y}) of the car {car_name} is duplicate with another car.")
                        input_ok = False
                        continue
                    # check the validity of a car's direction
                    if not direction in ["E", "S", "W", "N"]:   
                        print(f"Sorry you input an invalid direction ({direction}) for the car {car_name}.")
                        input_ok = False
                        continue
            # input valid car commands            
            input_ok = False
            while not input_ok:
                print(f"Please enter the commands for car {car_name}:")
                input_str = input()
                input_str = input_str.strip()
                input_ok = valid_commands(input_str)    
                # check whether the user-input car commands are valid or not
                if not input_ok:
                    print(f"Sorry you input invalid commands ({input_str}) for the car {car_name}.")
                else:
                    commands = input_str
            return car_name, x, y, direction, commands
        elif stage==5:                          # at the stage to select to start over or exit
            print("Please choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")
            input_str = input()
            input_str = input_str.strip()
            option, input_ok = valid_input(stage, input_str)
            if input_ok:
                return option
        elif stage==0:                          # last stage: goodbye message        
            print("Thank you for running the simulation. Goodbye!")
            input_ok = True
def RunStage(Stage):                            # perform the detailed operations across all stages
    global myField
    if Stage==1:                                # Stage 1: input the size of the simulation field
        Width, Height = prompt(Stage)
        myField = Field(Width, Height)
        print(f"You have created a field of {myField.width} x {myField.height}.")
        print()
    elif Stage==2:                              # Stage 2: select the operations of either adding a car or running a simulation
        Option = prompt(Stage)
        return Option
    elif Stage==3:                              # Stage 3: the add-car procedure
        car_name, x, y, direction, commands = prompt(Stage)
        myCar = Car(car_name, x, y, direction, commands)
        myField.addCar(myCar)
        myField.showFleet(True)
    elif Stage==4:                              # Stage 4: running a simulation, with the scenarios of either a single or multiple cars
        fleet_len = len(myField.fleet)
        if fleet_len==1:                        # Scenario 1 - Running simulation with a single car
            myField.showFleet(True)
            myCar = myField.fleet[0]
            myField.runCar(myCar, myCar.commands)
            myField.showFleet(False)
        elif fleet_len>1:                       # Scenario 2 - Running simulation with multiple cars
            myField.showFleet(True)
            myField.runFleet()
            myField.showFleet(False)
    elif Stage==5:                              # Stage 5: select to start over or exit
        Option = prompt(Stage)
        if Option=="1":
            return 1                            # start over
        elif Option=="2":
            return 0                            # exit
    elif Stage==0:                              # Stage 0: display a "goodbye" message, then exit the simulation system
        prompt(Stage)
            
myField = None        
Stage = 1                                       # starting from Stage 1: input the size of the simulation field
while Stage > 0:                                # loop from Step 1 to 5, until the user selected to exit
    RunStage(Stage)                             # prompt "Welcome to" message, and invite to input the size of the simulation field
    Stage = 2
    while Stage==2:
        Option = RunStage(Stage)                # prompt "add car(s)" or "run simulation"
        if Option=="1":                         # add a new car
            Stage = 3
            RunStage(Stage)
            Stage = 2
        elif Option=="2":                       # run a simulation
            Stage = 4
            RunStage(Stage)
            Stage = 5
    Stage = RunStage(Stage)                     # to select either Start Over (Stage 1) or exit (Stage 0)
RunStage(Stage)                                 # exit, show a goodbye message    
