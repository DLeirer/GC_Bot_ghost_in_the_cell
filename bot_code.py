######################################################
################## load libraries ####################
######################################################
import sys
import math


######################################################
################## Global Variables ##################
######################################################
#dictionary to keep track of pacs
factory_dict = {}
turn_counter = 0



######################################################
################## Define Classes ####################
######################################################

class Factory():
    
    def __init__(self,factory_id):
        self.factory_id = factory_id ## integer 
        self.n_adjacent_factories = None ## number of adjacent factories. 
        self.adjacent_factories = [] ## list of tuples  looking like ==  [(adjacent_factory_id, distance)]
        self.owned_by = None  ## integer (1 for me, -1 for opponent, 0 for neutral.)
        self.incoming_cyborgs = 0 ## list of tuples looking like == [(n_cyborgs,arrival_turn)] n_cyborgs is negative if enemy. positive if mine.


    def update_cyborgs_needed(self):
        if self.owned_by == 1: 
            self.cyborgs_needed = int((self.n_cyborgs * -1) - self.incoming_cyborgs)
            if self.n_cyborgs < 10:
                 self.cyborgs_needed + 20 
        else:
            self.cyborgs_needed = int(self.n_cyborgs - self.incoming_cyborgs)
        
        print(["cyborgs_needed]",self.cyborgs_needed], file=sys.stderr)


    #update basic information regarding current owner. number of cyborgs in factory and production per turn. 
    def update_information(self,arg_1, arg_2, arg_3):
        
        self.owned_by = arg_1
        self.n_cyborgs = arg_2
        self.n_production = arg_3

        self.incoming_cyborgs = 0

        self.update_cyborgs_needed()


    #arg1 is owner, arg4 is number of cyborgs (army_size), arg5 is turns till arrival. 
    def get_incoming_cyborgs(self,entity_id,owner,army_size,turns_till_arrival,turn_counter):
        #number of cyborgs if positive mine, if negative enemy. 
        arrival_turn=turn_counter + turns_till_arrival 
        number_of_cyborgs = owner * army_size

        self.incoming_cyborgs = self.incoming_cyborgs + number_of_cyborgs 
        print(["Factory_id",self.factory_id], file=sys.stderr)
        print(["incoming_cyporgs",self.incoming_cyborgs], file=sys.stderr)
        
        
        self.update_cyborgs_needed()

        #cyborgs needed for me to win. if enemy factory, positive 10 means 10 more needed. 
        #if mine


    def update_command(self,new_command):
        self.last_command = new_command #needs to be list (own_id,destination_id,number_cyborgs_sent)


######################################################
################## Functions #########################
######################################################

def find_target(factory_dict):

    #check if any neutral enemies.
    best_move = False
    for current_factory in factory_dict:
        #if factory is neutral and (n_cyborgs - incoming_cyborgs).
        if (factory_dict[current_factory].owned_by == 0) and (factory_dict[current_factory].cyborgs_needed >= 0):
            #check adjacent_factory status.
            adjacent_factories = factory_dict[current_factory].adjacent_factories
            #cyborgs needed.
            #factory_cyborg_diff
            #check if adjacent factories are mine
            for adj_factory in adjacent_factories:
                print(["adj_factory",best_move], file=sys.stderr)
                #if adjacent factory is mine.  
                if (factory_dict[adj_factory[0]].owned_by == 1) and (factory_dict[adj_factory[0]].cyborgs_needed < 0):
                    #return origin, destination
                    best_move = [factory_dict[adj_factory[0]].factory_id,factory_dict[current_factory].factory_id]

    return best_move


def find_target_any(factory_dict):
    best_move = False
    for current_factory in factory_dict:
        #if factory is neutral and (n_cyborgs - incoming_cyborgs).
        if factory_dict[current_factory].cyborgs_needed >= 0:
            #check adjacent_factory status.
            adjacent_factories = factory_dict[current_factory].adjacent_factories
            #cyborgs needed.
            #factory_cyborg_diff
            #check if adjacent factories are mine
            for adj_factory in adjacent_factories:
                print(["adj_factory",best_move], file=sys.stderr)
                #if adjacent factory is mine.  
                if (factory_dict[adj_factory[0]].owned_by == 1) and (factory_dict[adj_factory[0]].cyborgs_needed < -10):
                    #return origin, destination and number of cyborgs.     
                    
                    print(["integer of factory distance",adj_factory[1]], file=sys.stderr)
                    
                    
                    dist_prod = int(factory_dict[current_factory].n_production) * int(adj_factory[1])
                    print(["dist_prod",dist_prod], file=sys.stderr)
                    adjusted_cyborgs_needed=int(factory_dict[current_factory].cyborgs_needed + dist_prod + 5)
                                            
                    best_move = [factory_dict[adj_factory[0]].factory_id,
                                factory_dict[current_factory].factory_id,adjusted_cyborgs_needed]

    return best_move


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.



factory_count = int(input())  # the number of factories

#### initialise dictionary of factories
for factory_id in range(factory_count):
    factory_dict[factory_id] = Factory(factory_id)
    #print(["Factories_dict",factory_dict], file=sys.stderr)

link_count = int(input())  # the number of links between factories
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    
    ## add information to factory info. 
    factory_dict[factory_1].adjacent_factories.append((factory_2,distance))
    factory_dict[factory_2].adjacent_factories.append((factory_1,distance))

    #print(["Factories",factory_dict[factory_1].adjacent_factories], file=sys.stderr)

# game loop
while True:
    turn_counter += 1
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    print(["entity_count",entity_count], file=sys.stderr)
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)

        #if the entity is a factory. update ownership info, cyborgs and production level. 
        if entity_type == "FACTORY":
            factory_dict[entity_id].update_information(arg_1, arg_2, arg_3)
        
        if entity_type == "TROOP":
        #troop logic. arg1 = owner. arg2 = origin arg3 = destination, arg4 = number of cyborgs . arg5 = turns till arrival.
            factory_dict[arg_3].get_incoming_cyborgs(entity_id,arg_1,arg_4,arg_5,turn_counter)



        # arg1 * arg4 == impact on destination factory. 

            #print(["Owned_by",factory_dict[entity_id].owned_by], file=sys.stderr)
            #print(["Factory production",arg_3], file=sys.stderr)


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    #print output. 
    best_move=find_target(factory_dict)
    print(["Best_move",best_move], file=sys.stderr)

    if best_move == False: 
        best_move=find_target_any(factory_dict)
        if best_move == False: 
            output = "WAIT"
        else:
            output = "MOVE" + " " + str(best_move[0]) + " " + str(best_move[1]) + " " + str(best_move[2]) 
    else:
        output = "MOVE" + " " + str(best_move[0]) + " " + str(best_move[1]) + " " + str(10) 

    print(["Best_move",best_move], file=sys.stderr)
    print(output)

    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs
