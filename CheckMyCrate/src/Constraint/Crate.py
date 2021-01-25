# Object file for the crate
import json
from src.Variable.Variable import Variable
import os.path
from os import path

class Crate(object):


    def __init__(self, crate_path):

        if os.path.isfile(crate_path + "/ro-crate-metadata.json") == True:
           json_path = crate_path + "/ro-crate-metadata.json"
        else:
           json_path = crate_path + "/ro-crate-metadata.jsonld"


        with open(json_path) as json_file:
           data = json.load(json_file)
              
        if "@graph" in data.keys():

        # Takes @id and gives the structure of the item that has the @id
             graph = {}

              
             for item in data["@graph"]:
                  graph[item["@id"]] = item

             maps = {}
             crateVariable = Variable("$Crate")
             crateVariable.id = graph["ro-crate-metadata.json"]["about"]["@id"]
             maps["$Crate"] = crateVariable

             self.path = crate_path
             self.json_path = json_path
             self.data = data
             self.graph = graph
             self.maps = maps
             



