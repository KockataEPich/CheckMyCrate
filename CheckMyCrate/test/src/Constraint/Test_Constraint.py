import unittest

from src.Constraint.Constraint import Constraint

#Test for the implementation of class Constraint

class Test_Constraint(unittest.TestCase):
    def test_constraint_class_init(self):

        commands = ["MUST_REFER", "$Crate", "Main Worklfow", "mainEntity"]
        constraint = Constraint(commands)
        self.assertEquals(commands, constraint.commands)
        self.assertFalse(constraint.satisfied)
        self.assertEquals(constraint.errorMessage, "")
        
        constraint.option = "COULD"
        self.assertEquals(constraint.option, "COULD")
        
        constraint.message = "Not satisfied"

        self.assertEquals(constraint.message, "Not satisfied")

if __name__ == '__main__':
    unittest.main()
