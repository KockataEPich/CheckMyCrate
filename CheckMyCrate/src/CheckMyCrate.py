import src.Keyword_Management.Refer as Refer
import src.Keyword_Management.Contain as Contain

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

   # Stop the program if the paths are no specified properly
   if isItViable:
       
       if os.path.isfile(crate_path + "/ro-crate-metadata.json") == True:
           json_path = crate_path + "/ro-crate-metadata.json"
       else:
           json_path = crate_path + "/ro-crate-metadata.jsonld"

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

           

           constraint_list = getConstraintList(profile_path)
   
           #print(constraint_list)

           maps = {}
           is_if = False
           is_it_okay = True

           for item in constraint_list:
               commands = item.split("~")

               #print(commands)
              
               if is_if and is_it_okay == False:
                   print()
                   is_if = False
               else:
                   if commands[0] == "MUST_REFER":
                     
                       is_it_okay = Refer.does_it_refer(commands[1], commands[2], commands[3], graph, vertices, maps, False)
                   elif commands[0] == "MUST_CONTAIN":
                       
                       is_it_okay = Contain.does_it_contain(commands[1], commands[2], commands[3], commands[4], graph, vertices, maps, False)
                   elif commands[0] == "IF_COULD_CONTAIN":
          
                       is_if = True
                       is_it_okay = Contain.does_it_contain(commands[1], commands[2], commands[3], commands[4], graph, vertices, maps, True)       

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

@program.command()
@click.argument('profile_path', required=True)
def check_my_profile(crate_path, profile_path):
   """This validates if the profile follows the appropriate syntax"""

   if os.path.isfile(profile_path) == False:
       click.echo("Profile file could not be found")
       click.echo("Use --help for more information")
   else:
       profile_validate()


#def profile_validate():
   # OpenedBracket = False
    
   # with open(profile_path) as f:
      #     for line in f:
         #      for c in line:
           #        if c != "{" and OpenedBracket == False
                   

if __name__ == '__main__':
    program()