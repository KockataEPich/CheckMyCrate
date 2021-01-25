class Constraint(object):
    
    # Enumaration for the words MUST/COULD/SHOULD 
    option = ""

    # Boolean value for knowing if this constraint is satisfied under the variable it is contained
    self.satisfied = True

    # iF self.satisfied == False at the end then errorMessage will printed out in order to get feedback
    errorMessage = ""

    # Constructor
    def __init__(self, givenCommandsList):
        self.commands = givenCommandsList
        


