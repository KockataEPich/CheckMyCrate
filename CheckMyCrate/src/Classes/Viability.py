import os.path
from Classes.ProfileValidation import checkProfile
import click
from os import path
import json

def isItViable(crate_path, profile_path):

   # Checking if the profile is path is valid
   if not os.path.isfile(profile_path):
       click.echo("Invalid profile path")
       click.echo("Use --help for more information")
       return False

   if not checkProfile(profile_path):
       return False

   # Checking if the RO-Crate path is viable
   if not os.path.isdir(crate_path):
       click.echo("Invalid RO-Crate path")
       click.echo("Use --help for more information")
       return False

   if not os.path.isfile(crate_path + "/ro-crate-metadata.json") and not os.path.isfile(crate_path + "/ro-crate-metadata.jsonld"):
       click.echo("The directory does not contain the essential \"ro-crate-metadata.json/jsonld\" which means it is not a valid RO-Crate directory")
       click.echo("Use --help for more information")
       return False

   if os.path.isfile(crate_path + "/ro-crate-metadata.json"):
        json_path = crate_path + "/ro-crate-metadata.json"
   else:
        json_path = crate_path + "/ro-crate-metadata.jsonld"

   try:
        with open(json_path, 'rb') as json_path:
            crateData = json.load(json_path)
   except:
        click.echo("The ro-crate-metadata.json file is not a valid JSON file")
        return False


   return crateData
