import unittest
import src.Keyword_Management.ConstraintAndVariableManagement as ConVarMng
import src.CheckMyCrate as CMC
import src.Keyword_Management.Refer as Refer
from src.Constraint.Constraint import Constraint
from src.Variable.Variable import Variable
from src.Crate.Crate import Crate

class Test_ConstraintAndVariableManagemenet(unittest.TestCase):
    def test_attachConstraintsToVariables(self):
        crate = Crate("test/sample/")
        
        commands = ["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"]

        ConVarMng.attachConstraintsToVariables(crate, commands)

        self.assertTrue("Main Workflow" in crate.maps.keys())
        self.assertTrue(crate.maps["Main Workflow"].constraintList[0].satisfied)
        self.assertEquals(crate.maps["Main Workflow"].id, "Galaxy-Workflow-MC_COVID19like_Assembly_Reads.ga")

    def test_VerifyConstraintAndAttachVariableToId(self):
        crate = Crate("test/sample/")

        variable = Variable("Main Workflow")
        constraint = Constraint(["COULD_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])

        ConVarMng.VerifyConstraintAndAttachVariableToId(variable, constraint, crate)

        self.assertEquals(constraint.option, "COULD")
        self.assertTrue(constraint.satisfied)

    def test_VerifyConstraint(self):
        crate = Crate("test/sample/")

        constraint =  Constraint(["MUST_REFER" , "$Crate", "Main Workflow", "mainEntity"])
        self.assertTrue(Refer.searchForRefer(crate.maps["$Crate"], constraint, crate))

        constraint = Constraint(["COULD_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])
        
        ConVarMng.VerifyConstraint(crate.maps["Main Workflow"], constraint, crate, False)

        self.assertEquals(constraint.option, "COULD")
        self.assertTrue(constraint.satisfied)
    


if __name__ == '__main__':
    unittest.main()
