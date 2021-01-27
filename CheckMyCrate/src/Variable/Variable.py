# Variable class represents the human readable names we give in the profile in order to have the output more clear
# Each variable can have multiple constraints

class Variable(object):

    # Constructor
    def __init__(self, givenName):
        
        # The given name by the profile
        self.name = givenName

        # Constraint
        self.constraintList = []

        # ID that this variable is binded to
        self.id = None

        # Who is refering to this variable
        self.referedToBy = None
   
    # Appends a constraint to the list of constraints of this variable
    def addConstraint(self, constraint):
        self.constraintList.append(constraint)
            
    def referedToCheck(self, givenId):
      if self.id != givenId and self.id != None and self.referedToBy != None:
          return -2
      elif self.id != givenId and self.id != None and self.referedToBy == None:
          return -1
      else:
          return 1
        