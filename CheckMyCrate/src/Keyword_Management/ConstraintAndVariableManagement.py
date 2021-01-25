from src.Variable.Variable import Variable
from src.Constraint.Constraint import Constraint

def attachConstraintsToVariables(crate, commands):
        if commands[1] not in crate.maps.keys():

            variable = Variable(commands[1])
            constraint = Constraint(commands)

            attachVariableToId(variable, constraint, crate)

            variable.addConstraint(crate, constraint)
            crate.maps[commands[1]] = variable
        else:
            constraint = Constraint(commands)
           # if verifyVariableAndConstraint(crate, constraint, variable_map[commands[1]]):
            variable_map[commands[1]].addConstraint(constraint)
        

# Attaches variable to constraint, it can be either satisfied in that variable or not
def attachVaraibleToId(variable, constraint, crate):
    entityIsFound = False


    if constraint.commands[0] == "MUST_REFER":
        constraint.option = "MUST"

        if constraint.commands[2] not in crate.maps.keys():
          refferedToVariable = Variable(constraint.commands[2])
          crate.maps[constraint.commands[2]] = refferedToVariable

        for item in crate.graph.keys():

            if constraint.commands[3] in graph[item].keys():
                entityIsFound = True

                if "@id" in graph[item][constraint.commands[3]]:
                    variable.id = graph[item]["@id"]

                    
                    resolveDispute(crate.maps[crate.maps[constraint.commands[2]]],  graph[item][constraint.commands[3]]["@id"])

                    if graph[item][constraint.commands[3]]["@id"] not in crate.graph[item].keys():
                        constraint.errorMessage = print("The", constraint.commands[2], "is refered to with", constraint.commands[3],
                                            "properly, however it is MUST be present in the graph itself as well.")
                        constraint.self_satisfied = False

                    
                else:
                    constraint.errorMessage = print("The", constraint.commands[2], "is refered to with", constraint.commands[3],
                                   "inproperly in", constraint.commands[1],"as it does not have \"@id\" key.")
                    constraint.self_satisfied = False

        if not entityIsFound:
             constraint.errorMessage = print("Entity", constraint.commands[3], constraint.option,"exist in",constraint.commands[1],"and refer to",constraint.commands[2])
             constraint.self_satisfied = False
  
        variable.addConstraint(constraint)




# Checks if the new constraint added matches the variable or it is a wrong one
def verifyVariableAndConstraint(crate, constraint, variable):
    ...



def resolveIdDispute():
    ...