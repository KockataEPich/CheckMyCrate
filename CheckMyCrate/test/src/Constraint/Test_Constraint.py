import unittest
from src.Constraint.Constraint import Constraint
from src.Keyword_Management.ConstraintAndVariableManagement import verifyVariableAndConstraint

class Test_Constraint(unittest.TestCase):
    def test_constraint_class_init(self):
        commands = ["MUST_REFER", "$Crate", "Main Worklfow", "mainEntity"]
        constraint = Constraint(commands)
        assert(commands, constraint.commands)
        assert(constraint.satisfied, True)
        assert(errorMessage, "")
        
        constraint.option = "COULD"
        assert(constraint.option, "COULD")
        
        constraint.message = "Not satisfied"

        assert(constraint.message, "Not satisfied")

if __name__ == '__main__':
    unittest.main()
