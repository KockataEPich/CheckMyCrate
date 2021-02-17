import json
import src.Variable.VerifyVariable as VerVar

# This function checks something is contained in the graph using the correct entity
def does_it_contain(thing_that_is_referred_to, the_entity_it_refers_with, what_the_entity_must_have, 
                                                                                             graph, vertices, maps, is_it_COULD) -> bool:
    option = "MUST"

    if is_it_COULD:
        option = "COULD"

    for item in vertices.values():
        if the_entity_it_refers_with in item.keys() and json.dumps(item[the_entity_it_refers_with]) == what_the_entity_must_have:
            if item["@id"] not in maps.values():
                maps[thing_that_is_referred_to] = item["@id"]
                return True
            else:
                if verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, item["@id"]):
                    return True
           
    print(thing_that_is_referred_to, option, "exist in", thing_that_is_referred_to, "via", the_entity_it_refers_with, what_the_entity_must_have)

    return False



def verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, id):
    for string, identity in maps.items():
        if identity == id and string == thing_that_is_referred_to:
            return True
    
    return False



###################################### NEW IMPLEMENTATION #############################################################


def searchForContain(variable, constraint, crate):
    for item in crate.graph.values():

        # If we find the variable and it does indeed have the appropriate value we assume that we have found the desired id
        if constraint.commands[2] in item.keys() and json.dumps(item[constraint.commands[2]]) == constraint.commands[3]:
            variable.id = item["@id"]
            constraint.satisfied = True
            return True

   
    constraint.errorMessage = constraint.commands[1] + " " + constraint.option + " contain entity " + constraint.commands[2] + " with value " + constraint.commands[3]
    constraint.satisfied = False
    return False



def verifyContain(variable, constraint, crate, inTheLoop):
    
    if constraint.commands[2] in crate.graph[variable.id].keys() and json.dumps(crate.graph[variable.id][constraint.commands[2]]) == constraint.commands[3]:
        constraint.satisfied = True
        return True
    elif not inTheLoop and variable.referedToBy == None:
        variable.addConstraint(constraint)
        VerVar.verifyVariable(variable, crate)
        variable.constraintList.remove(constraint)
        return constraint.satisfied

    constraint.errorMessage = constraint.commands[1] + " " + constraint.option + " contain entity " + constraint.commands[2] + " with value " + constraint.commands[3]
    constraint.satisfied = False
    return False