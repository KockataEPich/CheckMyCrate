from src.Variable.Variable import Variable
import src.Variable.VerifyVariable as VerVar

# This function checks something is being refered in the graph using the correct entity
def does_it_refer(thing_that_refers, thing_that_is_referred_to, the_entity_it_refers_with, graph, vertices, maps, is_it_COULD) -> bool:
    entity_is_found = False
    is_found = False

    option = "MUST"

    if is_it_COULD:
       option = "COULD"

    if the_entity_it_refers_with in graph[maps[thing_that_refers]].keys():
        entity_is_found = True

        if "@id" in graph[maps[thing_that_refers]][the_entity_it_refers_with]:

            if not graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"] in maps.values():
                maps[thing_that_is_referred_to] = graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"]

                if graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"] in graph.keys():
                     return True
                else:
                     print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                                            "properly, however it is MUST be present in the graph itself as well.")
            else:
                if verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, id):
                    if graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"] in graph.keys():
                        return True
                    else:
                        print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                                            "properly, however it is MUST be present in the graph itself as well.")
                else:
                    maps[thing_that_is_referred_to] = maps[thing_that_is_referred_to] = graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"]
                   
        else:
            print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                                   "inproperly in", thing_that_refers,"as it does not have \"@id\" key.")
                


    if entity_is_found == False:
        print("Entity", the_entity_it_refers_with, option,"exist in",thing_that_refers,"via",the_entity_it_refers_with)
                    
    return False

def verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, id):
    for string, identity in maps.items():
        if identity == id and string == thing_that_is_referred_to:
            return True

    maps = maps.pop(string)
    return False













############################## NEW IMPLEMENTATION ###########################################################

# Method used to find an appropriate item in the graph to bind to the variable with the appropriate constraint

def searchForRefer(variable, constraint, crate):

    # Checks if we have exited the loop and didn't find the desired entity
    entityIsFound = False

    # Since MUST_REFER is made of 2 variables, we need to crate this second variable if it is not present yet
    # as it is noted that this variable is referenced by another
    if constraint.commands[2] not in crate.maps.keys():
        refferedToVariable = Variable(constraint.commands[2])
        crate.maps[constraint.commands[2]] = refferedToVariable

    # Search thorough the file to see if some variable has the same entity as requested
    for item in crate.graph.keys():

        # If we find it we assume that this is the desired variable
        if constraint.commands[3] in crate.graph[item].keys():
            entityIsFound = True
            variable.id = crate.graph[item]["@id"]

            # Check if the entity is in the graph
            if "@id" in crate.graph[item][constraint.commands[3]].keys():

                if crate.graph[item][constraint.commands[3]]["@id"] in crate.graph.keys():

                     # If this variable has already been assigned an ID which is different than this one it means that there is something wrong
                        if crate.maps[constraint.commands[2]].referedToCheck(variable) == 1:
                            crate.maps[constraint.commands[2]].referedToBy = variable.name
                            crate.maps[constraint.commands[2]].id = crate.graph[variable.id][constraint.commands[3]]["@id"]
                            constraint.satisfied = True
                            return True
                        elif crate.maps[constraint.commands[2]].referedToCheck(variable) == -1:
                            crate.maps[constraint.commands[2]].id = crate.graph[variable.id][constraint.commands[3]]["@id"]
                            crate.maps[constraint.commands[2]].referedToBy = variable.name
                            VerVar.updateVariableConstraints(crate.maps[constraint.commands[2]], crate)
                            constraint.satisfied = True
                            return True
                            
                        else:
                            constraint.errorMessage = constraint.commands[2] + " is reffered to by " + crate.maps[constraint.commands[2]].referedToBy + " and " \
                                                      + variable.name + " with different id's "
                else: 
                    constraint.errorMessage = "The " + constraint.commands[2] + " is refered to with " + constraint.commands[3] \
                       +  " properly, however it is MUST be present in the graph itself as well."

                    
            else:
                constraint.errorMessage = "The " + constraint.commands[2] + " is refered to with " + constraint.commands[3] \
                    + " inproperly in " + constraint.commands[1]," as it does not have \"@id\" key. "

    if not entityIsFound:
            constraint.errorMessage = "Entity " + constraint.commands[3] + " " + constraint.option + " exist in " \
                                        + " " + constraint.commands[1]   + " and refer to " + constraint.commands[2]
    constraint.satisfied = False
    return False

 # If the variable has already been added to maps and we have a new constraint for it check if the constraint holds 
 # for the current variable
def verifyRefer(variable, constraint, crate, insideTheLoop):
    
    # Checks if we have exited the loop and didn't find the desired entity
    entityIsFound = False

    # Since MUST_REFER is made of 2 variables, we need to crate this second variable if it is not present yet
    # as it is noted that this variable is referenced by another
    if constraint.commands[2] not in crate.maps.keys():
        refferedToVariable = Variable(constraint.commands[2])
        crate.maps[constraint.commands[2]] = refferedToVariable

    # If such entity exists in the variable

    if constraint.commands[3] in crate.graph[variable.id].keys():
         entityIsFound = True
         
         # if @id as entity exists in that given entity as is needed to reference
         if "@id" in crate.graph[variable.id][constraint.commands[3]].keys():
             
             # if the referenced @id is actually present in the file
             if crate.graph[variable.id][constraint.commands[3]]["@id"] in crate.graph.keys():

                 # If this variable has already been assigned an ID which is different than this one it means that there is something wrong
                 if crate.maps[constraint.commands[2]].referedToCheck(variable) == 1:
                      crate.maps[constraint.commands[2]].referedToBy = variable.id
                      crate.maps[constraint.commands[2]].referedToBy = variable.name
                      crate.maps[constraint.commands[2]].id = crate.graph[variable.id][constraint.commands[3]]["@id"]
                      constraint.satisfied = True
                      return True
                 elif crate.maps[constraint.commands[2]].referedToCheck(variable) == -1:
                            crate.maps[constraint.commands[2]].id = crate.graph[variable.id][constraint.commands[3]]["@id"]
                            VerVar.updateVariableConstraints(crate.maps[constraint.commands[2]], crate)
                            constraint.satisfied = True
                            return True
                
                 else:
                      constraint.errorMessage = constraint.commands[2] + " is reffered to by " + crate.maps[constraint.commands[2]].referedToBy + " and " \
                                                + variable.name + " with different id's "

             else: 
                  constraint.errorMessage = "The " + constraint.commands[2] + " is refered to with " + constraint.commands[3] \
                       +  " properly, however it is MUST be present in the graph itself as well."


        # If there is a problem with verifying something it is one of the following:
        # 1. The variable is the correct one and it is indeed not satisfying the constraint
        # 2. The variable that was assumed is not the correct one and we need to try and find the correct one
        # This method is also used when looping through the graph to verify so we need to know if we are inside it or outside it in order
        # to not create infinite loops

         elif not insideTheLoop:
              #TODO
              verifyVariable(variable, constraint, crate)
         else:
             constraint.errorMessage = "The " + constraint.commands[2] + " is refered to with " + constraint.commands[3] \
                    + " inproperly in " + constraint.commands[1]," as it does not have \"@id\" key. "
    elif not insideTheLoop:
         verifyVariable(variable, constraint, crate)
    else:
         if not entityIsFound:
            constraint.errorMessage = "Entity " + constraint.commands[3] + " " + constraint.option + " exist in " \
                                        + " " + constraint.commands[1]   + " and refer to " + constraint.commands[2]

 
    constraint.satisfied = False
    return False
