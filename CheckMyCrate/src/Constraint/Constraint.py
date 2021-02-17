# Constraint class
# Constraint is called the entiry format of writing "constraints" in the profile
# They get atteched to variables

class Constraint(object):
    
    # Constructor
    def __init__(self, givenCommandsList):
        # The full commands list
        self.commands = givenCommandsList

        # If the constraint is satisfied under its binded variable
        self.satisfied = False

        # The error message if it isn't satisfied
        self.errorMessage = ""

        # The option argument indicating the MUST/COULD/SHOULD enumeration
        self.option = ""
        
       
