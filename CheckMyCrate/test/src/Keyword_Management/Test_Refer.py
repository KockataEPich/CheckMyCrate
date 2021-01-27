import unittest
import json 
import src.Keyword_Management.Refer as Refer
import src.CheckMyCrate as CMC
import src.Keyword_Management.ConstraintAndVariableManagement as ConVarMng
from src.Constraint.Constraint import Constraint
from src.Variable.Variable import Variable

from src.Crate.Crate import Crate 


class Test_Refer(unittest.TestCase):

    def test_mixedRefers1(self):
        crate = Crate("test/sample/")

        variable = Variable("Main Workflow")
        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])

        self.assertTrue(Refer.searchForRefer(variable, constraint, crate))
        variable.addConstraint(constraint)
        crate.maps["Main Workflow"] = variable

        constraint =  Constraint(["MUST_REFER" , "$Crate", "Main Workflow", "mainEntity"])

        self.assertTrue(Refer.searchForRefer(crate.maps["$Crate"], constraint, crate))
        self.assertEquals(variable.referedToBy, "$Crate")


    def test_mixedRefers2(self):
        crate = Crate("test/sample/")

        constraint =  Constraint(["MUST_REFER" , "$Crate", "Main Workflow", "mainEntity"])
        self.assertTrue(Refer.searchForRefer(crate.maps["$Crate"], constraint, crate))

        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])

        self.assertTrue(Refer.searchForRefer(crate.maps["Main Workflow"], constraint, crate))
        self.assertEquals(crate.maps["Main Workflow"].referedToBy, "$Crate")



    def test_searchForRefer(self):
        crate = Crate("test/sample/")

        variable = Variable("Main Workflow")
        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])

        self.assertTrue(Refer.searchForRefer(variable, constraint, crate))
        variable.addConstraint(constraint)
        crate.maps["Main Workflow"] = variable







        
    
    def test_VerifyRefer(self):
        crate = Crate("test/sample/")

        variable = Variable("Main Workflow")
        constraint = Constraint(["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])

        self.assertTrue(Refer.searchForRefer(variable, constraint, crate))
        variable.addConstraint(constraint)
        crate.maps["Main Workflow"] = variable





if __name__ == '__main__':
    unittest.main()
