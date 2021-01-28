# Class which varifies if there isn't a more appropriate varible for the constraint
import src.Keyword_Management.ConstraintAndVariableManagement as ConVarMng

#TODO
def verifyVariable(variable, constraint, crate):
    variable.addConstraint(constraint)
    
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

    variable.id = idWithSatisfiedMax
    variable.constraintList.remove(constraint)
    if idWithSatisfiedMax == savedInitialId:
        return True
    else:
        return False



def numberOfConstraintsSatisfied(variable):
    numberOfSatisfied = 0

    for constraint in range(len(variable.constraintList)):
        if variable.constraintList[constraint].satisfied:
            numberOfSatisfied += 1

    return numberOfSatisfied





def updateVariableConstraints(variable, crate):
  for constraint in variable.constraintList:
      ConVarMng.VerifyConstraint(variable, constraint, crate, True)


