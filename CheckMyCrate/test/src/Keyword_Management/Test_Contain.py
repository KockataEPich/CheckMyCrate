import src.CheckMyCrate as CheckMyCrate
import src.Keyword_Management.Contain as Contain
import src.Keyword_Management.Refer as Refer
import src.Keyword_Management.ConstraintAndVariableManagement as ConVarMng
from src.Constraint.Constraint import Constraint
from src.Variable.Variable import Variable
import unittest
import json

from src.Crate.Crate import Crate

class Test_Contain(unittest.TestCase):

    def test_searchContain(self):
            crate = Crate("test/sample/")

            variable = Variable("Main Workflow")
            constraint = Constraint(["MUST_CONTAIN" , "Main Workflow", "@type", "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"])

            self.assertTrue(Contain.searchForContain(variable, constraint, crate))
            variable.addConstraint(constraint)
            crate.maps["Main Workflow"] = variable

            constraint =  Constraint(["COULD_CONTAIN" , "Main Workflow Diagram", "@type", "[\"File\", \"ImageObject\", \"WorkflowSketch\"]"])

            self.assertTrue(Refer.searchForRefer(crate.maps["$Crate"], constraint, crate))
            assert(is_it_okay)

    def test_checkContain(self):
            crate = Crate("test/sample/")

            variable = Variable("Main Workflow")
            constraint = Constraint(["MUST_REFER" , "Main Workflow", "Type of Programming Language", "programmingLanguage"])

            self.assertTrue(Refer.searchForRefer(variable, constraint, crate))
            variable.addConstraint(constraint)
            crate.maps["Main Workflow"] = variable

            constraint = Constraint(["MUST_CONTAIN" , "Main Workflow", "@type", "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]"])

            self.assertTrue(Contain.verifyContain(variable, constraint, crate))

if __name__ == '__main__':
    unittest.main()


    
