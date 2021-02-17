# Class which varifies if there isn't a more appropriate varible for the constraint
import src.Keyword_Management.ConstraintAndVariableManagement as ConVarMng

# MEthod that checks all the ids in the graph and sees if there is an id in which more constraints are satisfied
def verifyVariable(variable, crate):
    
    savedInitialId = variable.id
    idWithSatisfiedMax = variable.id
    
    satisfiedMaxSoFar = numberOfConstraintsSatisfied(variable)

    for key in crate.graph.keys():
        print(key)
        variable.id = key
        updateVariableConstraints(variable, crate)
        currentSatisfied = numberOfConstraintsSatisfied(variable)

        if currentSatisfied > satisfiedMaxSoFar:
            idWithSatisfiedMax = key
            satisfiedMaxSoFar = currentSatisfied

    if idWithSatisfiedMax == savedInitialId:
        variable.id = idWithSatisfiedMax
        return True
    else:
        if satisfiedMaxSoFar == 0:
            variable.id = None
            return False
        variable.id = idWithSatisfiedMax
        return False

        #TODO
       # for key in crate.maps.keys():
         #   if crate.maps[key].id == idWithSatisfiedMax:
           #     if satisfiedMaxSoFar > numberOfConstraintsSatisfied(crate.maps[key]) and crate.maps[key].referedToBy != None:
              #       variable.id = idWithSatisfiedMax
                #     crate.maps[key].id = None
                #     for index in range(len(crate.maps[key].constraintList)):
                   #      crate.maps[key].constraintList[index].satisfied = False

                       
               #      verifyVariable(crate.maps[key], crate)
              #  elif satisfiedMaxSoFar < numberOfConstraintsSatisfied(crate.maps[key]) and crate.maps[key].referedToBy != None crate.maps[key].referedToBy != None:



def numberOfConstraintsSatisfied(variable):
    numberOfSatisfied = 0

    for constraint in range(len(variable.constraintList)):
        if variable.constraintList[constraint].satisfied:
            numberOfSatisfied += 1

    return numberOfSatisfied





def updateVariableConstraints(variable, crate):
  for constraint in variable.constraintList:
      ConVarMng.VerifyConstraint(variable, constraint, crate, True)


