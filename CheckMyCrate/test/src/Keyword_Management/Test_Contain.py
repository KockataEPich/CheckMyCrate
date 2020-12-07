import src.CheckMyCrate as CheckMyCrate
import src.Keyword_Management.Contain as Contain

import unittest
import json

class Test_Contain(unittest.TestCase):

    def test_does_it_contain(self):
        with open("./test/sample/ro-crate-metadata.json") as json_file:
         data = json.load(json_file)


         vertices = {}
         vertice_number = 0
         graph = {}
           

         for item in data["@graph"]:
             graph[item["@id"]] = vertice_number
             vertices[vertice_number] = item

             vertice_number += 1

         maps = {}

        is_it_okay = Contain.does_it_contain("$Crate", "Main Workflow", "mainEntity", graph, vertices, maps, False, False)
        assert(is_it_okay)

        

   

if __name__ == '__main__':
    unittest.main()


    
