import unittest

from src.Crate.Crate import Crate
import src.CheckMyCrate as CMC
class Test_CheckMyCrate(unittest.TestCase):
    def test_isItViable(self):
        self.assertTrue(CMC.isItViable("test/sample/", "test/profile_library/test_refer_basic.txt"))
        self.assertFalse(CMC.isItViable("test/sample/", "test/profile_library/test_refer_basfwefic.txt"))
        self.assertFalse(CMC.isItViable("test/Constraint/", "test/profile_library/test_refer_basic.txt"))



    def test_getConstraintList(self):
        commandList = CMC.getConstraintList("test/profile_library/test_ro_crate_1.1_basic1.txt")

        self.assertEquals(commandList[0][0], "MUST_REFER")
        self.assertEquals(commandList[0][1], "$Crate")
        self.assertEquals(commandList[0][2], "Main Workflow")
        self.assertEquals(commandList[0][3], "mainEntity")

        self.assertEquals(commandList[1][0], "MUST_CONTAIN")
        self.assertEquals(commandList[1][1], "Main Workflow")
        self.assertEquals(commandList[1][2], "@type")
        self.assertEquals(commandList[1][3], "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]")

        self.assertEquals(commandList[2][0], "MUST_REFER")
        self.assertEquals(commandList[2][1], "Main Workflow")
        self.assertEquals(commandList[2][2], "Type of Programming Language")
        self.assertEquals(commandList[2][3], "programmingLanguage")

        self.assertEquals(commandList[3][0], "IF_COULD_CONTAIN")
        self.assertEquals(commandList[3][1], "Main Workflow Diagram")
        self.assertEquals(commandList[3][2], "@type")
        self.assertEquals(commandList[3][3], "[\"File\", \"ImageObject\", \"WorkflowSketch\"]")

        self.assertEquals(commandList[4][0], "MUST_REFER")
        self.assertEquals(commandList[4][1], "Main Workflow")
        self.assertEquals(commandList[4][2], "Main Workflow Diagram")
        self.assertEquals(commandList[4][3], "image")
        
    def test_refers_only(self):
        self.assertTrue(CMC.checkTheCrate("test/sample/", "test/profile_library/test_refer_basic.txt"))

    def test_contains_only(self):
        self.assertTrue(CMC.checkTheCrate("test/sample/", "test/profile_library/test_contain_basic.txt"))
        
    def test_mixed(self):
        self.assertTrue(CMC.checkTheCrate("test/sample/", "test/profile_library/test_ro_crate_1.1_basic1WithoutIFAndSpecify.txt"), "It doesn't work when everything is only contain and refer")
        self.assertTrue(CMC.checkTheCrate("test/sample/", "test/profile_library/test_ro_crate_1.1_basic2.txt"), "It doesn't work when everything is combined")
        

if __name__ == '__main__':
    unittest.main()
