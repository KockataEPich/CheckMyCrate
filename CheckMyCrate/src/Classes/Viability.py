import os.path
import src.Classes.ProfileValidation as PV
from os import path

def isItViable(crate_path, profile_path):

   # Checking if the profile is path is valid
   if os.path.isfile(profile_path) == False:
       click.echo("Invalid profile path")
       click.echo("Use --help for more information")
       return False

   # Checking if the RO-Crate path is viable
   if os.path.isdir(crate_path) == False:
       click.echo("Invalid RO-Crate path")
       click.echo("Use --help for more information")
       return False

   if os.path.isfile(crate_path + "/ro-crate-metadata.json") == False and os.path.isfile(crate_path + "/ro-crate-metadata.jsonld") == False:
       click.echo("The directory does not contain the essential \"ro-crate-metadata.jsonld\" which means it is not a valid RO-Crate directory")
       click.echo("Use --help for more information")
       return False


   return PV.checkProfile(profile_path)
