# Object file for the crate
import json

class Crate(object):


    def __init__(self, crate_path, json_path):
        with open(json_path) as json_file:
           data = json.load(json_file)

        if "@graph" in data.keys():
        # Takes @id and gives the vertice
             graph = {}

        # Takes the vertice and gives the dictionary with information about it
             vertices = {}
             vertice_number = 0

           

             for item in data["@graph"]:
                  graph[item["@id"]] = vertice_number
                  vertices[vertice_number] = item
                  vertice_number += 1

             self.path = crate_path
             self.json_path = json_path
             self.graph = graph
             self.vertices = vertices
             self.maps = {}

