import unittest
import json 
import src.Keyword_Management.Refer as Refer


class Test_Refer(unittest.TestCase):

    def test_does_it_refer(self):

        with open("sample/ro-crate-metadata.json") as json_file:
         data = json.load(json_file)


         vertices = {}
         vertice_number = 0
         graph = {}
           

         for item in data["@graph"]:
             graph[item["@id"]] = vertice_number
             vertices[vertice_number] = item

             vertice_number += 1

         maps = {}

        is_it_okay = Refer.does_it_refer("$Crate", "Main Workflow", "mainEntity", graph, vertices, maps, False)
        assert(is_it_okay)

if __name__ == '__main__':
    unittest.main()
