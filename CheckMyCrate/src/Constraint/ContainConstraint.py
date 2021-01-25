from src.Constraint.Constraint import Constraint
class Contain(Constraint):

    def __init__(self, givenVariable, the_entity_it_refers_with, what_the_entity_must_have):
        super().__init__(givenVariable)
        self.entityKey = the_entity_it_refers_with
        self.entityValue = what_the_entity_must_have
    """description of class"""


