from src.Constraint.Constraint import Constraint
class ReferConstraint(Constraint):

     def __init__(self, givenVariableSource, givenVariableTarget, the_entity_it_refers_with):
        super().__init__(givenVariableSource)
        self.varibaleTarget = givenVariableTarget
        self.entity = the_entity_it_refers_with


        """description of class"""


