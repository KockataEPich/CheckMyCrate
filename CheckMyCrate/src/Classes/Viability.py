import os.path
from src.Classes.ProfileValidation import checkProfile
import click
from os import path
import json

# Method which checks if the given paths are viable
# crate and profile paths
def isItViable(crate_path, profile_path):

   # Checking if the profile is path is valid
   if not os.path.isfile(profile_path):
       click.echo("Invalid profile path")
       click.echo("Use --help for more information")
       return False

   # Checking if the profile file is a valid json profile
   profileData = checkProfile(profile_path)
   if not profileData:
       return False

   # Checking if the RO-Crate path is viable
   if not os.path.isdir(crate_path):
       click.echo("Invalid RO-Crate path")
       click.echo("Use --help for more information")
       return False

   # Checking if there is a ro-crate-metadata.json or ro-crate-metadata.jsonld
   # file in the specified crate directory
   if not os.path.isfile(crate_path + "/ro-crate-metadata.json") and not os.path.isfile(crate_path + "/ro-crate-metadata.jsonld"):
       click.echo("The directory does not contain the essential \"ro-crate-metadata.json/jsonld\" which means it is not a valid RO-Crate directory")
       click.echo("Use --help for more information")
       return False

   # Get the actual path to the json
   if os.path.isfile(crate_path + "/ro-crate-metadata.json"):
        json_path = crate_path + "/ro-crate-metadata.json"
   else:
        json_path = crate_path + "/ro-crate-metadata.jsonld"

   # Get the prepared crate data
   crateData = readAndPrepareCrateGraph(json_path)

   if not crateData:
       return False

   return [crateData, profileData]


# Method that transforms the crateData into usable dictionary
def readAndPrepareCrateGraph(json_path):
    # Check if it is a valid JSON file
    try:
        with open(json_path, 'rb') as json_path:
            crateData = json.load(json_path)
    except:
        click.echo("The ro-crate-metadata.json file is not a valid JSON file")
        return False

    # Get the graph contets
    crateData = crateData.get("@graph") 

    crateGraph = {}

    # Transform the graph contents into usable dictionary where
    # the key for each element is its @id
    for item in crateData:
        crateGraph[item.get("@id")] = item

    return crateGraph
