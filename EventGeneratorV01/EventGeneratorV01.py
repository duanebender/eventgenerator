import random
import sys
import datetime

print('Event Generator Version 0.0.6')
print('1/19/2015\n')
print('Authors: Bender, Ma, Sartipi; Jan 2015\n\n')

# TODO: define a debug level 
# TODO: print simulation parameters
# declare global parameters

# Value set parameters
Roles = []
Number_of_Roles = 0
Users = []
Number_of_Users = 0
Locations = []
Number_of_Locations = 0
Times = []
Number_of_Times = 0
Patients = []
Number_of_Patients = 0
Data = []
Number_of_Data = 0
Operations = []
Number_of_Operations = 0

# itemset parameters
Itemsets = []
Number_of_Itemsets = 1000
Itemset_Correlation = 0
Average_Itemset_Length = 3
User_Defined_Itemsets = [["R-1","U-99", "", "", "P-1", "D-1", "O-1"], ["R-1", "U-66", "L-1", "", "", "", ""], ["R-2","U-2","","T-520","","",""]]
Itemset_Saturation = 0.2 # this is the itemset random saturation % (range 0.0 -> 1.0) (ie when generating events use 20% defined itemsets and 80% completely random events) 

# sequence pattern parameters
Sequence_Patterns = []
Number_of_Sequence_Patterns = 100
Sequence_Pattern_Correlation = 0.4
Average_Sequence_Pattern_Length = 3
User_Defined_Sequence_Patterns = [[0,1],[0,2]]


# simulation parameters
# day/month/year
Events = []
Start_Date = datetime.date(2011, 2, 12)
Start_Time = datetime.time(0, 0, 0)
End_Date = datetime.date(2011, 2, 16)
End_Time = datetime.time(23, 59, 59)
#Include_Days_of_Week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] # mon = 0, .... sun = 6
Include_Days = [0,1,2,3,4] # mon-fri; mon=0....sun=6
Average_Events_Per_Day = 250
Sequence_Saturation = 0.10 # value between 0-1 (percentage between random itemsets and defined sequence patterns)


def Load_ValueSets():
    "Procedure to load valuesets for each attribute"
    global Roles
    global Users
    global Locations
    global Times
    global Patients
    global Data
    global Operations

    # TODO: create User_Defined_Roles array, copy that into roles value set first then autgenerte roles up to NumberOFRoles
    Roles = ["R-1", "R-2"]
    Users = ["U-1", "U-2"]
    Locations = ["L-1", "L-2"]
    Times = ["T-1", "T-2"]
    Patients = ["P-1", "P-2"]
    Data = ["D-1", "D-2"]
    Operations = ["O-1", "O-2"]
     

def Load_Parameters():
    "Procedure to load simulation parameters"

    # TODO: these values will eventually be loaded from the UI
    global Number_of_Itemsets
    global Itemset_Correlation 
    global Average_Itemset_Length
    global User_Defined_Itemsets

    global Number_of_Sequence_Patterns
    global Sequence_Pattern_Correlation
    global Average_Sequence_Pattern_Length
    global User_Defined_Sequence_Patterns
    global Sequence_Patterns



def Generate_Itemsets():
    "Procedure which generates itemset templates"
    sys.stdout.write("Generating " + str(Number_of_Itemsets) + " itemsets...") 
    sys.stdout.flush()

    # TODO: make more configurable - i.e. should be able to set number of attributes and name them dynamically (other than time and date)
    global Roles
    global Users
    global Locations
    global Times
    global Patients
    global Data
    global Operations

    global Itemsets
    global User_Defined_Itemsets

    Number_of_Attributes = 7

    # how to keep track of types? should we use column ordinality in a sparse array structure? or include syntax inside the array? type:value in one position? or should we use "type", "value" pairs in sequence?
    # column cardinality (always same number of slots, just leave them blank (like a database): (assume the attribute set is user, location, time, resource
    #   Itemset = ["", "", "T4", "R1"]
    # syntax inside the array approach:
    #   Itemset = ["Location:L4", "Time:T3"]
    # type, value pairs in sequence:
    #   Itemset = ["Location", "L4", "User", "U3"]
    # I think for overall parsing efficiency the sparse method should be used
    # each column will be defined a meaning - i.e. the type is indicated by the position 

    # itemset columns will be hard-defined for now as : [ User, Role, Session, Resource, ResourceType, Operation, Patient,  Emergency, Time, Date]  

    # For comparison to the "live" data we have we should have an itemset definition that matches the ATNA logs 
    # the ATNA transformed output looks as follows : [ R-1, U-1, L-1, T-1, P-1, D-1, O-1 ] (role, user, location, time, patient, data, operation) 

    # if there are any defined, load user defined itemsets
    if len(User_Defined_Itemsets) > 0 :
        Itemsets = User_Defined_Itemsets
    
    # problem : if the attributes are empty in the previous entry then there is a chance the copied attributes will be empty
    # therefore we must "fill in" the itemset templates with random values before copying them, and we must also "fill in" the remaining attributes before adding them to the itemset collection
    # bigger problem : we can't fill in these itemset templates yet or else they will all be the same when instantiated :: do not fill in for now
    #Fill_Attributes()
    
    for x in range(len(Itemsets), Number_of_Itemsets): # need to account for Itemsets already added as user defined itemsets, i.e. begin creating templates at end of predefined template area and continue to max number 
        sys.stdout.write(".") # progress indicator
        sys.stdout.flush()
        
        attributes_copied = 0

        Itemset = ["","","","","","",""] # TODO: change to a dynamic structure using Number_of)Attributes instead of a hard coded list
        if (len(Itemsets) > 0 and Itemset_Correlation > 0) :
            # this is not the first itemset and the correlation is greater than 0 - this means we shall seed the current itemset with some of the values from the previous itemset  (why previous? can it be random?)
            # how many attributes to copy? -> as many as possible up to the average itemset length parameter, if not enough available then add some random ones 
            # pick a random number between 0 and the average itemset length 
            #Random_Number_of_Attributes = round(random.randint(0, round(Average_Itemset_Length * 2)))
            Random_Number_of_Attributes = int(random.normalvariate(Average_Itemset_Length, 1.0)) # Note: using a hard-coded std deviation of 1.0 -> possibly make a parameter 
            # don't go over the maximum number of attributes
            if (Random_Number_of_Attributes > Number_of_Attributes):
                Random_Number_of_Attributes = Number_of_Attributes
                        
            # select a random itemset template from the existing set to start with (problem is if only previous set is used and attributes are not all filled in the set quickly converges to empty)
            random_itemset_index = random.randint(0, len(Itemsets)-1)
            tmp_itemset = Itemsets[random_itemset_index]                                                                                                                   
            # how many of these are not empty/blank?
            random_itemset_size = 0
            for r in range(len(tmp_itemset)):
                if tmp_itemset[r] != "":
                    random_itemset_size = random_itemset_size + 1

            for y in range(0, Random_Number_of_Attributes): # this value is for the correlated attributes with the previous itemset, then we need to add the random values 
                # randomly pick attributes by index (number between 0 and 6 (7 attributes total for atna model))
                # keep going until they are all done (no way to know since we are randomly selecting and we may repeat the same attribute, that is the reason for the while 1 stmt
                while 1: 
                    if attributes_copied >= random_itemset_size:   # can only copy as many attributes as are available in the selected itemset (prevent endless loop, etc) 
                        break
                    attribute_index = random.randint(0, Number_of_Attributes-1) # pick a number between 0 and 6 - this is the array index of the attribute to copy 
                    if Itemsets[random_itemset_index][attribute_index] == "": # nothing to copy so try another attribute 
                        continue
                    # must be a non-empty attribute in the destination set as well
                    # make sure we didn't already replace that one (i.e. check to make sure it's empty) 
                    if Itemset[attribute_index] == "" :
                        # copy the value from the previous itemset to the current itemset
                        # Itemset[attribute_index] = Itemsets[x - 1][attribute_index]
                        Itemset[attribute_index] = Itemsets[random_itemset_index][attribute_index]
                        attributes_copied = attributes_copied + 1
                        break
            # now add some random attributes if needed to get up to the desired number of attributes in this itemset (ie only 2 may have been copied but we want a length of 4 for example)
            while attributes_copied < random_itemset_size:
                # randomly select the attribute to fill in 
                attribute_index = random.randint(0, Number_of_Attributes-1)
                # if the itemset value is blank, go ahead and select a value for that attribute
                if Itemset[attribute_index] == "":
                    # copy from the value sets or from other itemsets? (copy from value sets for now)
                    # structure is (role, user, location, time, patient, data, operation)
                    if attribute_index == 0:
                        # index 0 is Role
                        # make sure we have at least one value for role
                        if len(Roles) > 0 :
                            Itemset[attribute_index] = Roles[random.randint(0, len(Roles)-1)] # randomly select a value from Roles
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 1:
                        # index 1 is User
                        # make sure we have at least one value for users
                        if len(Users) > 0 : 
                            Itemset[attribute_index] = Users[random.randint(0, len(Users)-1)] # randomly select a value from Users
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 2:
                        # index 2 is locations
                        if len(Locations) > 0 :
                            Itemset[attribute_index] = Locations[random.randint(0, len(Locations)-1)] # randomly select a value from Locations
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 3:
                        # index 3 is times
                        if len(Times) > 0 :
                            Itemset[attribute_index] = Times[random.randint(0, len(Times)-1)] # randomly select a value from Times
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 4:
                        # index 4 is patients
                        if len(Patients) > 0 :
                            Itemset[attribute_index] = Patients[random.randint(0, len(Patients)-1)] # randomly select a value from Patients
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 5:
                        # index 5 is data
                        if len(Data) > 0 :
                            Itemset[attribute_index] = Data[random.randint(0, len(Data)-1)] # randomly select a value from Data
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 6:
                        # index 6 is operations
                        if len(Operations) > 0 :
                            Itemset[attribute_index] = Operations[random.randint(0, len(Operations)-1)] # randomly select a value from Operations
                            attributes_copied = attributes_copied + 1
        else : # this is the first itemset or there is no correlation between itemsets 
            # generate a random itemset template of the average length set in the parameter
            Random_Number_of_Attributes = int(random.normalvariate(Average_Itemset_Length, 1.0)) # Note: using a hard-coded std deviation of 1.0 -> possibly make a parameter 
            # make sure parameter was not set larger than the structure size
            if (Random_Number_of_Attributes > Number_of_Attributes):
                Random_Number_of_Attributes = Number_of_Attributes
            
            # now add random attributes get up to the desired number of attributes in this itemset 
            while attributes_copied < Random_Number_of_Attributes:
                # randomly select the attribute to fill in 
                attribute_index = random.randint(0, Number_of_Attributes-1)
                # if the itemset value is blank, go ahead and select a value for that attribute
                if Itemset[attribute_index] == "":
                    # copy values from the value set definitions 
                    # structure is (role, user, location, time, patient, data, operation)
                    if attribute_index == 0:
                        # index 0 is Role
                        # make sure we have at least one value for role
                        if len(Roles) > 0 :
                            Itemset[attribute_index] = Roles[random.randint(0, len(Roles)-1)] # randomly select a value from Roles
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 1:
                        # index 1 is User
                        # make sure we have at least one value for users
                        if len(Users) > 0 : 
                            Itemset[attribute_index] = Users[random.randint(0, len(Users)-1)] # randomly select a value from Users
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 2:
                        # index 2 is locations
                        if len(Locations) > 0 :
                            Itemset[attribute_index] = Locations[random.randint(0, len(Locations)-1)] # randomly select a value from Locations
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 3:
                        # index 3 is times
                        if len(Times) > 0 :
                            Itemset[attribute_index] = Times[random.randint(0, len(Times)-1)] # randomly select a value from Times
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 4:
                        # index 4 is patients
                        if len(Patients) > 0 :
                            Itemset[attribute_index] = Patients[random.randint(0, len(Patients)-1)] # randomly select a value from Patients
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 5:
                        # index 5 is data
                        if len(Data) > 0 :
                            Itemset[attribute_index] = Data[random.randint(0, len(Data)-1)] # randomly select a value from Data
                            attributes_copied = attributes_copied + 1
                    elif attribute_index == 6:
                        # index 6 is operations
                        if len(Operations) > 0 :
                            Itemset[attribute_index] = Operations[random.randint(0, len(Operations)-1)] # randomly select a value from Operations
                            attributes_copied = attributes_copied + 1
             
                                                     



        # add the (partially complete) itemset to set of itemset templates 
        Itemsets.append(Itemset)

        # TODO: move to event generator - cannot fill attrbutes here as the events would contain all the same values 
        # Fill_Attributes()

        # TODO: assign each itemset a probability (use a shadow matrix) 
        # normalize the probabilities
        # calculate cumulative probabilities 	

    # show itemset list for debugging purposes
    print()
    Attribute_Count = 0
    for x in range(len(Itemsets)):
        print(Itemsets[x])
        Current_Itemset = Itemsets[x]
        for x in range (0, len(Current_Itemset)) :
            if Current_Itemset[x] != "" :
                Attribute_Count = Attribute_Count + 1
    Average_Attributes = Attribute_Count / len(Itemsets)
    print("Average itemset length (desired / actual) = (" + str(Average_Itemset_Length) + " / " + str(Average_Attributes) + ")" )
    print()

    




def Generate_Sequence_Patterns():
    "Procedure which generates sequence patterns"
    sys.stdout.write("Generating " + str(Number_of_Sequence_Patterns) + " sequence patterns...")
    sys.stdout.flush()
    
    global Roles
    global Users
    global Locations
    global Times
    global Patients
    global Data
    global Operations

    global Itemsets
    global User_Defined_Itemsets

    global Number_of_Sequence_Patterns
    global Sequence_Pattern_Correlation
    global Average_Sequence_Pattern_Length 
    global Sequence_Patterns
    global User_Defined_Sequence_Patterns

    Index_Set = []
    Current_Sequence_Pattern = []
 
    # insert sequence patterns defined by the UI
    if len(User_Defined_Sequence_Patterns) > 0 :
        Sequence_Patterns = User_Defined_Sequence_Patterns
    Lower = len(Sequence_Patterns)
    # then randomly generate the rest based on the parameters
    for x in range(Lower, Number_of_Sequence_Patterns):
        sys.stdout.write(".")
        sys.stdout.flush()

        # reset local pattern
        Current_Sequence_Pattern = []
        Index_Set = [] # a set of indexes into the itemset collection is a sequence pattern
        # select the length of the sequence from a frequency distribution around the average 
         
        # if(correlation is defined (not 0) and this is not the first sequence pattern then (there is a correlation between the sequence and the previous sequence so copy some of the itemsets from the previous sequence
        # Note: use index into itemset collection to define sequence patterns, i.e. [0,3,4], [1,2,3] etc.
        if (Sequence_Pattern_Correlation > 0 and len(Sequence_Patterns) > 0) :
            # length of current sequence (avg length paramter rnd), don't want 0 length patterns
            #Current_Sequence_Length = random.randint(1, Average_Sequence_Pattern_Length * 2)
            Current_Sequence_Length = int(random.normalvariate(Average_Sequence_Pattern_Length, 1.0))
            # how many to copy from previous sequence?
            Sequence_Correlation_Overlap = int(Current_Sequence_Length * Sequence_Pattern_Correlation) # should this be int, round, ceil, floor, trunc?  
            # which ones? (randomly select?) 
            # first copy overlap sequences from randomly selected set
            #Previous_Sequence_Set = Sequence_Patterns[x-1]
            Previous_Sequence_Set = random.choice(Itemsets)
            Previous_Sequence_Length = len(Previous_Sequence_Set)
            # overlap can't be larger than the length of the previous sequence 
            if (Sequence_Correlation_Overlap > Previous_Sequence_Length) :
                Sequence_Correlation_Overlap = Previous_Sequence_Length

            # create a structure of the indexes to select from
            for y in range(Sequence_Correlation_Overlap):
                # copy the index values from previous sequence
                Index_Set.append(Previous_Sequence_Set[y])
            
            #randomize the list of indexes (why am i randomizing? that seems to ruin the sequence pattern)
            #random.shuffle(Index_Set)
             
            #for y in range(Sequence_Correlation_Overlap) : 
            #    Index = int(Index_Set.pop(0))
            #    Current_Sequence_Pattern.append(Index)

            # that takes care of the correlation overlap, now need to add additional random indexes up to the current sequence length
            # create a list of all available indexes
            for z in range(Number_of_Itemsets):
                Index_Set.append(z)

            random.shuffle(Index_Set)

            for y in range(len(Current_Sequence_Pattern), Current_Sequence_Length):
                Index = int(Index_Set.pop(0))
                Current_Sequence_Pattern.append(Index)


            
        else :
            # there is no correlation between subsequent sequence patterns so 
            # just randomly select itemsets to include in sequence patterns
            # length of current sequence (avg length paramter rnd)
            #Current_Sequence_Length = round(random.randint(0, Average_Sequence_Pattern_Length * 2))
            Current_Sequence_Length = int(random.normalvariate(Average_Sequence_Pattern_Length,1.0))

            # create a list of all available indexes
            for z in range(Number_of_Itemsets):
                Index_Set.append(z)

            random.shuffle(Index_Set)

            for y in range(Current_Sequence_Length):
                Index = int(Index_Set.pop(0))
                Current_Sequence_Pattern.append(Index)

        # don't add empty sequence patterns
        if (len(Current_Sequence_Pattern) > 0):
            Sequence_Patterns.append(Current_Sequence_Pattern)

        # TODO: assign each pattern a probability (use a shadow matrix) 
        # normalize the probabilities
        # calculate cumulative probabilities 	

    # show itemset list for debugging purposes
    print() 
    for x in range(len(Sequence_Patterns)):
        print(Sequence_Patterns[x])
    print()



def Generate_Events():
    "Procedure which generates events from the pattern templates"
    sys.stdout.write("Generating events....")
    sys.stdout.flush()

    global Start_Date
    global End_Date
    global Include_Days
    global Average_Events_Per_Day
    global Events
    global Average_Sequence_Length
    global Sequence_Saturation
    global Sequence_Patterns

    Current_Day = Start_Date
    # Event = ["","","","","","",""] (role, user, location, time, date, patient, data, operation) 
    Current_Event = ["","","","","","","",""] 
    Empty_Event = ["","","","","","","",""] 
    Daily_Events = []
    Pattern = []

    iIndex = 0
    eIndex = 0


    # need to consider %sequence patterns, % itemsets, % random 
    # for begin date to end date - make a list of days to be included in simulation first, then iterate through the list 
    # e.g. since there are day of week exclusions, make sure current day is an event day (i.e. Sundays could be blocked off) if it is a blocked day then skip to next day

    while Current_Day <= End_Date:
        sys.stdout.write(".")
        sys.stdout.flush()

        Current_Event = [] 
        Day = Current_Day.weekday()
        if Day in Include_Days:
            

            # do stuff for the current day
            # one of the simulation parameters is number of events per day ? 
            # calculate a deviation from mean to get the number of events to 
            # generate for this particular day
            Number_Events_This_Day = int(random.normalvariate(Average_Events_Per_Day, 1.0))
            Daily_Events = []
            #Marker = len(Events) 
            #for j in range(Number_Events_This_Day):
            #    Events.append(Empty_Event)

            # now assign the timeline for the current day
            Time_Samples = []

            # resultion is by minute (24 * 60), T0-T1439
            # we have to account for "include hours/exclude hours" (TODO)
            # we will use 2 normal distributions; half of the times will come from one and the other half from the other 
             
            # python random normal dist function
            # random.normalvariate(mu, sigma)
            # Normal distribution. mu is the mean, and sigma is the standard deviation.

            # 9am = 60 * 9 = 540
            # TODO: move these parameters to the global simulation parms 
            Mu_1 = 540
            # std deviation around 1 hr = 60 minutes
            Sigma_1 = 90
            # derive half of the times around peak time 1
            for k in range(int(Number_Events_This_Day/2)):      # TODO : check if num events is odd or even and account for edge case if odd
                Time_Sample = int(random.normalvariate(Mu_1, Sigma_1))
                # print(Time_Sample)
                Time_Samples.append(Time_Sample)

            # 2pm = 60 * (12 + 2) = 60 * 14 = 840
            Mu_2 = 840
            #std deviation around 90 minutes
            Sigma_2 = 90
            # derive the remaining half of the times around peak time 2
            # make sure we have enough samples for all events
            while (len(Time_Samples) < Number_Events_This_Day) :
                Time_Sample = int(random.normalvariate(Mu_2, Sigma_2))
                Time_Samples.append(Time_Sample)

            Time_Samples.sort() # sort the values to resemble a sequence log
            # add the "T-" string and copy to the events array
            for k in range(len(Time_Samples)):
                Date_String = "D-" + str(Current_Day.year) + "/" + str(Current_Day.month) + "/" + str(Current_Day.day) 
                Time_String = "T-" + str(Time_Samples[k])
                Current_Event = ["","","",Date_String, Time_String,"","",""]
                Daily_Events.append(Current_Event)


            # use ?sequence saturation %? (degree of utilization of sequences) to 
            # determine how many sequences to insert vs. just itemsets
            # for example assume sat % of 50% - approx half of events will be 
            # sequence patterns and the remainder will be filled with known itemsets
            # number of sequences to select = total number for the day / avg  sequence length * saturation ratio
            # Example: # seq to select = 100 events for the day  / avg seq length of 4 * 0.20 (20%) = 100 / 4 * 0.2 = 25 * .2 = 5 sequences
            # representing an average of 20% of the events for the day, the rest will be random itemsets

            Num_Sequences = int(Average_Events_Per_Day / Average_Sequence_Pattern_Length * Sequence_Saturation)
            Marker = 0

            for y in range(Num_Sequences):
                # randomly select a sequence and copy the contents into a temporary local variable 
                Rnd = random.randint(0, len(Sequence_Patterns)-1)
                Pattern = Sequence_Patterns[Rnd]
                for k in range(len(Pattern)):
                    # randomly insert into event stream, move along randomly through the stream 
                    Step = Marker + int((len(Daily_Events) - Marker) / (Num_Sequences * Average_Sequence_Pattern_Length))
                    Event_Index = random.randint(Marker, Step)
                    Itemset_Index = Pattern[k]
                    Itemset = Itemsets[Itemset_Index]
                    Daily_Events[Event_Index] = Itemset
                    Marker = Step

            # make another pass over the daily events collection and fill in the empty slots with randomly selected itemesets until all slots are full
            # need to know how many blank events are left to generate

            Events_Remaining = 0
            
            for x in range (len(Daily_Events)):
                # generate events
                Current_Event = Daily_Events[x]
                if(Current_Event[0] == ""):  
                    # blank event - either copy one of the defined itemsets at random or use random value sets - random saturation % will decide
                    Events_Remaining = Events_Remaining + 1

            Itemset_Events = int(Itemset_Saturation * Events_Remaining)
            Random_Events = Events_Remaining - Itemset_Events

            # randomly insert remaining events
            # randomly select a position, see if it is full, if not, insert an event until all are gone 
            Itemset_Time = ""
            Event_Low_Time = ""
            Event_High_Time = ""

            # insert itemsets 
            while(Itemset_Events > 0):
                Current_Event = []
                # randomly pick an itemset
                Random = random.randint(0, len(Itemsets)-1)
                Itemset = Itemsets[Random]
                # extract the time and find out the start position 
                Itemset_Time = Itemset[3]
                for x in range(0,len(Daily_Events)-1):
                    Current_Event = Daily_Events[x]
                    Event_Low_Time = Current_Event[3]
                    # make sure we're not at the last element and therefore would go out of bounds by checking the next element
                    if(x<len(Daily_Events)-1):
                        Next_Event = Daily_Events[x+1]
                        Event_High_Time = Next_Event[3]

                    if(Itemset_Time < Event_Low_Time):  # time is lower than the first element, add an event or overwrite? I think it is safer to add one at the beginning
                        Current_Event[0] = Itemset[0]
                        Current_Event[1] = Itemset[1]
                        Current_Event[2] = Itemset[2]
                        # leave [3] alone - it already has the time defined from above
                        Current_Event[4] = Itemset[4]
                        Current_Event[5] = Itemset[5]
                        Current_Event[6] = Itemset[6]
                        Current_Event[7] = Itemset[7]
                        # need to insert at beginning - no events with lower time
                        Daily_Events.insert(0, Current_Event)
                        # update size variable 
                        Number_Events_This_Day = Number_Events_This_Day + 1
                        Itemset_Events = Itemset_Events - 1                    
                         
                    if(Itemset_Time >= Event_Low_Time and Itemset_Time <= Event_High_Time and Current_Event[0] == ""): # we have found the sort position and the current slot is blank
                        # (role, user, location, time, patient, data, operation)
                        Current_Event[0] = Itemset[0]
                        Current_Event[1] = Itemset[1]
                        Current_Event[2] = Itemset[2]
                        # leave [3] alone - it already has the time defined from above
                        Current_Event[4] = Itemset[4]
                        Current_Event[5] = Itemset[5]
                        Current_Event[6] = Itemset[6]
                        Current_Event[7] = Itemset[7]
                        Daily_Events[Random] = Current_Event
                        Itemset_Events = Itemset_Events - 1                    

                    # the itemsets were templates, i.e. they have empty spaces
                    # now make sure all of the event attributes are filled in with values



            # insert random events
            while(Random_Events > 0):
                Random = random.randint(0, len(Daily_Events)-1)
                Current_Event = Daily_Events[Random]
                if (Current_Event[0] == ""):
                    # found one, fill it in with random values except time (time already defined)
                    # (role, user, location, time, patient, data, operation)
                    Current_Event[0] = Roles[random.randint(0, len(Roles)-1)]
                    Current_Event[1] = Users[random.randint(0, len(Users)-1)]
                    Current_Event[2] = Locations[random.randint(0, len(Locations)-1)]
                    # leave [3] alone - it already has the time defined from above
                    Current_Event[4] = Date_String # todays date
                    Current_Event[5] = Patients[random.randint(0, len(Patients)-1)]
                    Current_Event[6] = Data[random.randint(0, len(Data)-1)]
                    Current_Event[7] = Operations[random.randint(0, len(Operations)-1)]
                    Daily_Events[Random] = Current_Event                    
                    Random_Events = Random_Events - 1
                 
            # copy daily events to main event stream 
            for x in range(len(Daily_Events)):
                Events.append(Daily_Events[x])

        # increment day counter to next day 
        Current_Day = Current_Day + datetime.timedelta(1,0,0,0,0,0,0)

    # show event list for debugging purposes
    print()
    for x in range(len(Events)):
        print(Events[x])


    

#   //
#		// // since this is about user behaviour, start by selecting user...
#		// User
#		// if not already assigned from copy function above, randomly select user
#		//    	from users using probability distribution
#		// Role



#		// if not already assigned from itemset correlatin above, look in relations 
#				collection for a relationship between this user and role values 
#		// if exists, make a temporary copy of the roles collection
#		//	change the probability value in the roles collection to the value found 
#			in the set of relations
#		// look for any relation values of 0 in the relations set for this user and
#			a particular role, delete those roles from the temporary roles collection
#		// from the remaining modified set of roles, select one at random and assign 
#			it
#		//  REPEAT above steps for location, operation, resources, patient, 
#			sessionid, emergency, modality
#		 
#	//   make a pass over the structure to assign the events times
#	//     according to the time distribution function and time of day 
#	//     exceptions   
#		//	end for   
#


def Fill_Attributes():
    
    global Itemsets

    global Roles
    global Users
    global Locations
    global Times
    global Patients
    global Data
    global Operations


    for x in range(len(Itemsets)):
        Fill_Itemset = Itemsets[x]
        # for each event fill in with random attributes until desired number is achieved        
        if(Fill_Itemset[0] == "") :
            # Role is empty, select a random one
            z = random.randint(0, len(Roles)-1)
            Fill_Itemset[0] = Roles[z]

        if(Fill_Itemset[1] == "") :
            # User is empty, select a random one
            z = random.randint(0, len(Users)-1)
            Fill_Itemset[1] = Users[z]

        if(Fill_Itemset[2] == "") :
            # Location is empty, select a random one
            z = random.randint(0, len(Locations)-1)
            Fill_Itemset[2] = Locations[z]

        if(Fill_Itemset[3] == "") :
            # Time is empty, select a random one
            z = random.randint(0, len(Times)-1)
            Fill_Itemset[3] = Times[z]

        if(Fill_Itemset[4] == "") :
            # User is empty, select a random one
            z = random.randint(0, len(Patients)-1)
            Fill_Itemset[4] = Patients[z]

        if(Fill_Itemset[5] == "") :
            # User is empty, select a random one
            z = random.randint(0, len(Data)-1)
            Fill_Itemset[5] = Data[z]

        if(Fill_Itemset[6] == "") :
            # User is empty, select a random one
            z = random.randint(0, len(Operations)-1)
            Fill_Itemset[6] = Operations[z]

    Itemsets[x] = Fill_Itemset



# define global variable for simulation 
# these values will eventually be extracted from the UI

# initialize the list of itemsets
Itemsets = []

# load valuesets 
Load_ValueSets()

# load the parameters for the simulation 
Load_Parameters()

Generate_Itemsets()

Generate_Sequence_Patterns()

Generate_Events()