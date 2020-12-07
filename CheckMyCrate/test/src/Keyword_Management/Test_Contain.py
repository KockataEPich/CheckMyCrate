import src.CheckMyCrate as CheckMyCrate
import src.Keyword_Management.Contain as Contain

import unittest
import json

from src.Crate.Crate import Crate

class Test_Contain(unittest.TestCase):

    def test_does_it_contain(self):
        crate = Crate("test/sample/","test/sample/ro-crate-metadata.json")


        is_it_okay = Contain.does_it_contain("$Crate", "Main Workflow Diagram", "@type", "[\"File\", \"ImageObject\", \"WorkflowSketch\"]", 
                                                                                                           crate.graph, crate.vertices, crate.maps, False)
        assert(is_it_okay)

        

   

if __name__ == '__main__':
    unittest.main()


    
