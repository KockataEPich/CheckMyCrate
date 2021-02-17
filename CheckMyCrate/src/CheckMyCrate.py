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
    
    mapCrateAndWorklfow = checkIfIndeedWorkflowCrate(crateData)
    if isinstance(mapCrateAndWorklfow, int):
        return False

    # JSON arrays with their respective cardinality
    indexOfCrate = next(iter(mapCrateAndWorklfow))

    indexOfWorkflow = mapCrateAndWorklfow[indexOfCrate]


    minimumCardinalityArray = profileData["properties"][0]["minimum"]
    recommendedCardinalityArray = profileData["properties"][1]["recommended"]
    optionaCardinalityArray = profileData["properties"][2]["optional"]

    print(indexOfCrate)
    print(indexOfWorkflow)




    
    
    

    return True


        
    

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
                                 return {position : position2}
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