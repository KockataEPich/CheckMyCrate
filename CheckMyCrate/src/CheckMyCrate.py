import src.Keyword_Management.Refer as Refer
import src.Keyword_Management.Contain as Contain
import src.Keyword_Management.Specify as Specify
import src.Keyword_Management.ConstraintAndVariableManagement as ConVarMng

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


       crate = Crate(crate_path)

       constraint_list = getConstraintList(profile_path)
   
           #print(constraint_list)

       is_if = False
       is_it_okay = True
       counter = 0

       for item in constraint_list:
           commands = item.split("~")

           ConVarMng.attachConstraintsToVariables(crate, commands)

               #print(commands)
          # if is_if:
          #     counter += 1
         #      if counter > 1:
         #         is_if = False
         #         counter = 0

        #   if is_if and is_it_okay == False:
         #      is_if = False
         #      counter = 0
        #   else:
        #       if commands[0] == "MUST_REFER":   
         #          is_it_okay = Refer.does_it_refer(commands[1], commands[2], commands[3], crate.graph, crate.vertices, crate.maps, False)

           #    elif commands[0] == "COULD_REFER":   
           #        is_it_okay = Refer.does_it_refer(commands[1], commands[2], commands[3], crate.graph, crate.vertices, crate.maps, True)

              # elif commands[0] == "IF_COULD_REFER":  
              #     is_if = True
              #     is_it_okay = Refer.does_it_refer(commands[1], commands[2], commands[3], crate.graph, crate.vertices, crate.maps, True)

               #elif commands[0] == "MUST_CONTAIN":
               #    is_it_okay = Contain.does_it_contain(commands[1], commands[2], commands[3], crate.graph, crate.vertices, crate.maps, False)
              
              # elif commands[0] == "IF_COULD_CONTAIN":
              #     is_if = True
               #    is_it_okay = Contain.does_it_contain(commands[1], commands[2], commands[3], crate.graph, crate.vertices, crate.maps, True) 
               
              # elif commands[0] == "COULD_CONTAIN":
               #    is_it_okay = Contain.does_it_contain(commands[1], commands[2], commands[3], crate.graph, crate.vertices, crate.maps, True) 
                   
            #   elif commands[0] == "MUST_SPECIFY":
              #     is_it_okay = Specify.does_it_specify(commands[1], commands[2], commands[3], crate, False)


       # Print every constraint's error message where appropriate
       for key in crate.maps.keys():
           for item in range(len(crate.maps[key].constraintList)):
               if not crate.maps[key].constraintList[item].satisfied:
                  print(crate.maps[key].constraintList[item].errorMessage)

                   
# Is used to get the constraint list of the commands
def getConstraintList (profile_path):
   current_constraint = ""
   constraint_list =[]
   constraintBegins = False

   with open(profile_path) as f:
              for line in f:

                  if line.strip() == "}":
                      constraintBegins = False
                      current_constraint = current_constraint.replace("\n", "")
                      constraint_list.append(current_constraint)
                      current_constraint = ""

                   
                  if constraintBegins:
                       current_constraint += line



                  if line.strip() == "{":
                      constraintBegins = True

   return constraint_list

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