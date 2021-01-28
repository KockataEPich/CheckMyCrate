import unittest
import src.Variable.VerifyVariable as VerVar
from src.Variable.Variable import Variable
from src.Constraint.Constraint import Constraint
from src.Crate.Crate import Crate

class Test_VerifyVariable(unittest.TestCase):

    def test_updateVariableConstraints(self):
      
        crate = Crate("test/sample/")

        variable = Variable("Main Workflow")
        variable.id = "Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga"
        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])
        variable.addConstraint(constraint)
        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Main Workflow Diagram", "image"])
        variable.addConstraint(constraint)

        constraint = Constraint(["MUST_REFER" , "Main Workflow", "qkwofkqwfq", "image121ewwwsswqq"])
        constraint.satisfied = True
        variable.addConstraint(constraint)

        #TODO constraint = Constraint(["MUST_CONTAIN", "Main Workflow", "@type")
        #variable.addConstraint(constraint)

        VerVar.updateVariableConstraints(variable, crate)

        self.assertTrue(variable.constraintList[0].satisfied)
        self.assertTrue(variable.constraintList[1].satisfied)
        self.assertFalse(variable.constraintList[2].satisfied)

       
    def test_verifyVariable(self):
        crate = Crate("test/sample/")

        variable = Variable("Main Workflow")
        variable.id = "MC_WF.png"

        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])
        variable.addConstraint(constraint)

        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Main Workflow Diagram", "image"])
        variable.addConstraint(constraint)

        constraint = Constraint(["MUST_REFER" , "Main Workflow", "qkwofkqwfq", "image121ewwwsswqq"])
        constraint.satisfied = True

        self.assertFalse(VerVar.verifyVariable(variable, constraint, crate), "It does attach it properly to the id with the most constraints satisfied")

        self.assertEquals(variable.id, "Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga", "it does not find the id with the most constraints properly")
        self.assertFalse(constraint.satisfied)
 
        #TODO need to add contains



if __name__ == '__main__':
    unittest.main()
