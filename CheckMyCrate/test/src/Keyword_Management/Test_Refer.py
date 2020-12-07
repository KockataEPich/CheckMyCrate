import unittest
import json 
import src.Keyword_Management.Refer as Refer
from src.Crate.Crate import Crate 


class Test_Refer(unittest.TestCase):

    def test_does_it_refer(self):
        crate = Crate("test/sample/","test/sample/ro-crate-metadata.json")

        is_it_okay = Refer.does_it_refer("$Crate", "Main Workflow", "mainEntity", crate.graph, crate.vertices, crate.maps, False)
        assert(is_it_okay)

if __name__ == '__main__':
    unittest.main()
