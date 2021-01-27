from src.Variable.Variable import Variable
from src.Constraint.Constraint import Constraint
import src.Keyword_Management.Refer as Refer


# Method for distributing variables to ids and constraints to variables
def attachConstraintsToVariables(crate, commands):

        # If we have never seen this variable we need to search for it and assume it if we find somehing that satisfies it
        if commands[1] not in crate.maps.keys():

            variable = Variable(commands[1])
            constraint = Constraint(commands)

            
            VerifyConstraintAndAttachVariableToId(variable, constraint, crate)

            variable.addConstraint(constraint)
            crate.maps[commands[1]] = variable
        # Else if we have seen it we verify it and add it to the variable
        else:
            constraint = Constraint(commands)
            VerifyConstraint(crate.maps[commands[1]], constraint, crate, False)
            crate.maps[commands[1]].addConstraint(constraint)
        

# Attaches variable to constraint, it can be either satisfied in that variable or not
def VerifyConstraintAndAttachVariableToId(variable, constraint, crate):

    if constraint.commands[0] == "MUST_REFER":
        constraint.option = "MUST"
        Refer.searchForRefer(variable, constraint, crate)

    if constraint.commands[0] == "COULD_REFER":
        constraint.option = "COULD"
        Refer.searchForRefer(variable, constraint, crate)

    if constraint.commands[0] == "SHOULD_REFER":
        constraint.option = "SHOULD"
        Refer.searchForRefer(variable, constraint, crate)


# When the variable has already been attached to an ID and we are checking if that is the correct variable - id combination, give the appropriate messages
def VerifyConstraint(variable, constraint, crate, inTheLoop):
    if constraint.commands[0] == "MUST_REFER":
        constraint.option = "MUST"
        Refer.verifyRefer(variable, constraint, crate, inTheLoop)

    if constraint.commands[0] == "COULD_REFER":
        constraint.option = "COULD"
        Refer.verifyRefer(variable, constraint, crate, inTheLoop)

    if constraint.commands[0] == "SHOULD_REFER":
        constraint.option = "SHOULD"
        Refer.verifyRefer(variable, constraint, crate, inTheLoop)



# Checks if the new constraint added matches the variable or it is a wrong one
# TODO
def verifyVariableAndConstraint(crate, constraint, variable):
    ...


# TODO
def resolveIdDispute():
    ...