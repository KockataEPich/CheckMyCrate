import src.Keyword_Management.Refer as Refer
import src.Keyword_Management.Contain as Contain
import src.Keyword_Management.Specify as Specify

from src.Crate.Crate import Crate

import click
from jsonschema import validate
import json
import os.path
from os import path
import zipfile
import sys

#class Config(object):

  #  def __init__(self):
    #    self.verbose = False

#pass_config = click.make_pass_decorator(Config, ensure = True)


@click.group()
@click.option('--verbose', is_flag=True)
def program(verbose):
    print('Welcome \n')
            
@program.command()
@click.argument('crate_path', required=True)
@click.argument('profile_path', required=True)
def check_my_crate(crate_path, profile_path):
   """ This command compares the RO-Crate directory against a given profile"""


   # Stop the program if the paths are no specified properly
   if isItViable(crate_path, profile_path):
       
       if os.path.isfile(crate_path + "/ro-crate-metadata.json") == True:
           json_path = crate_path + "/ro-crate-metadata.json"
       else:
           json_path = crate_path + "/ro-crate-metadata.jsonld"


       with open(json_path) as json_path:
           crateData = json.load(json_path)


       with open(profile_path) as profile_path:
           profileData = json.load(profile_path)

       resolution = False

       if profileData["@type"] == "WorkflowCrate":
         resolution = checkWorkflowCrates(crateData, profileData)
       else:
         resolution = checkDataCrates(crateData, profileData)

       if not resolution:
           print("This is not a valid workflow crate")




def checkWorkflowCrates(crateData, profileData):
    #print(profileData["properties"][0]["minimum"])

    #print(crateData)
    crateData = crateData.get("@graph") 
    
    # Return workflowID
    workflowID = checkIfIndeedWorkflowCrate(crateData)

    if isinstance(workflowID, int):
        return False


    crateGraph = {}

    for item in crateData:
        crateGraph[item.get("@id")] = item


    crateId = "./"

    # JSON arrays with their respective cardinality
    minimumMarginalityArray = profileData["properties"][0]["minimum"]
    recommendedMarginalityArray = profileData["properties"][1]["recommended"]
    optionaMarginalityArray = profileData["properties"][2]["optional"]

    compareTheCrate(minimumMarginalityArray, crateGraph, crateId, workflowID, "MUST")
    compareTheCrate(recommendedMarginalityArray, crateGraph, crateId, workflowID, "SHOULD")
    compareTheCrate(optionaMarginalityArray, crateGraph, crateId, workflowID, "COULD")
    
    


                        
            
           # if graph[crateId].get(item.get("@id")).get("@id") != None:
                #prtin("wow")
                


    
    
    

    return True


def compareTheCrate(array, crateGraph, crateId, workflowID, option):

    for item in array:
        if crateGraph[crateId].get(item.get("@id")) != None:
            if isinstance(crateGraph[crateId].get(item.get("@id")), dict):
                itemID = crateGraph[crateId].get(item.get("@id")).get("@id")
                if crateGraph.get(itemID) != None:
                    if crateGraph.get(itemID).get("@type") != None:
                        if crateGraph.get(itemID).get("@type") == item.get("expected_type") or crateGraph.get(itemID).get("@type") in item.get("expected_type"):
                            ...
                        else:
                            (item.get("@id") + " needs  to reference an item of type " + json.dumps(item.get("expected_type")))
                    else:
                        print("@type must exist in the item which is referenced by", item.get("@id"))
                else:
                    print("The entity which references the item ID is present, however the item itself does not exist in the graph", item.get("@id"))



        elif crateGraph[workflowID].get(item.get("@id")) != None:
            if isinstance(crateGraph[workflowID].get(item.get("@id")), dict):
                itemID = crateGraph[workflowID].get(item.get("@id")).get("@id")
                if crateGraph.get(itemID) != None:
                    if crateGraph.get(itemID).get("@type") != None:
                        if crateGraph.get(itemID).get("@type") == item.get("expected_type") or crateGraph.get(itemID).get("@type") in item.get("expected_type"):
                            ...
                        else:
                            print(item.get("@id") + " needs  to reference an item of type " + json.dumps(item.get("expected_type")))
                    else:
                        print("@type must exist in the item which is referenced by", item.get("@id"))
                else:
                    print("The entity which references the item ID is present, however the item itself does not exist in the graph", item.get("@id"))
        else:
            print("Property: ", json.dumps(item.get("@id")), option, "exist in the crate with expected @type", json.dumps(item.get("expected_type")), "\n" + "Description:", item.get("description"), "\n")

  #  print(crateData)
                   





def checkIfIndeedWorkflowCrate(crateData):
    for position, item  in enumerate(crateData):
        if item["@id"] == "./":
            if item.get("mainEntity") == None:
                print("Main Workflow must be referenced in the crate via mainEntity")
                return -1
            elif item["mainEntity"].get("@id") == None:
                print("The key \"mainEntity\" exists, however it is not refercing the Main Workflow properly")
                return -1
            else:
                for position2, item2 in enumerate(crateData):
                    if item2.get("@id") == item["mainEntity"].get("@id"):
                        if item2.get("@type") != None:
                            if json.dumps(item2.get("@type")) == "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]":
                                 return item["mainEntity"].get("@id")
                            else:
                                 print("The main entity type does not have the appropriate value. For it to be a workflow crate it needs to have a type of [\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]")
                                 return -1
                        else:
                            print("The main entity needs to have a @type keyword")
                            return -1

                print("The Main Workflow needs to be present in the graph as well")
                return -1


    print("Crate entity \"./\" inside the JSON file does not exist")
    return -1
  








def isItViable(crate_path, profile_path):

   isItViable = True

   # Checking if the profile is path is valid
   if os.path.isfile(profile_path) == False:
       click.echo("Invalid profile path")
       click.echo("Use --help for more information")
       isItViable = False

   # Checking if the RO-Crate path is viable
   if os.path.isdir(crate_path) == False:
       click.echo("Invalid RO-Crate path")
       click.echo("Use --help for more information")
       isItViable = False

   if os.path.isfile(crate_path + "/ro-crate-metadata.json") == False and os.path.isfile(crate_path + "/ro-crate-metadata.jsonld") == False:
       click.echo("The directory does not contain the essential \"ro-crate-metadata.jsonld\" which means it is not a valid RO-Crate directory")
       click.echo("Use --help for more information")
       isItViable = False

   return isItViable


if __name__ == '__main__':
    program()