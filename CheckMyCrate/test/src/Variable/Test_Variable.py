import unittest
from src.Variable.Variable import Variable
from src.Constraint.Constraint import Constraint

class Test_Variable(unittest.TestCase):
    def test_init_variable(self):

        variable = Variable("Main Workflow")

        self.assertEquals(variable.name, "Main Workflow")
        self.assertEquals(variable.id, None)
        self.assertEquals(variable.referedToBy, None)

        commands = ["MUST_REFER" , "$Crate", "Main Workflow", "mainEntity"]
        constraint = Constraint(commands)

        variable.addConstraint(constraint)
        self.assertTrue(constraint in variable.constraintList)


if __name__ == '__main__':
    unittest.main()
