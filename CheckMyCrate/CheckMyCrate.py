
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
@click.argument('schema_instance', type=click.File('r'), required=True)
@click.argument('schema_validation', type=click.File('r'), required=True)
def schema_validator(schema_instance, schema_validation):
    """This command reads a json schema from a file and validates it against a schema"""
    chunk1 = {}
    chunk2 = {}
  
    chunk1 = json.loads(schema_instance.read())

    chunk2 = json.loads(schema_validation.read())

    try:
        validate(instance=chunk1, schema=chunk2)
        click.echo('The input json is valid against the scheme')
    except:
        click.echo('The input json is invalid against the scheme')



    click.echo(chunk1)

    click.echo(chunk2)


    
@program.command()
@click.argument('dir_path', required=True)
def root_check(dir_path):
    """ This command checks if the RO-Crate directory follows the accepted structure """
    
    print(dir_path)
   

    isRO_Crate_So_Far = False;
    isRO_Crate_missing_something = False;
    missingRecommendedFiles = ''

    if os.path.isdir(dir_path) == False:
         click.echo("Path does not lead to a directory or a zip file and thus invalid.")
    else:
         file = dir_path + "/ro-crate-metadata.jsonld"
         file2 = dir_path + "/ro-crate-metadata.json"
         print(file)
         if os.path.isfile(file) or os.path.isfile(file2):
              isRO_Crate_So_Far = True;
         else:
              click.echo("File ro-crate-metadata.json/ld MUST be present")

         file = dir_path + "/ro-crate-preview.html"
         if os.path.isfile(file) == False:
              isRO_Crate_missing_something = True
              missingRecommendedFiles += " ro-crate-preview.html "
              

    if isRO_Crate_So_Far == False:
        click.echo("This Crate does not fulfill the requirements")
    else:
        click.echo("This is valid RO-Crate")
        if isRO_Crate_missing_something:
            click.echo("The following files are not required but are missing and are recommended:")
            click.echo(missingRecommendedFiles)
            
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

           #print(graph)
           #print()
           #print(vertices)

           constraintBegins = False

           constraint_list = []
           current_constraint = ""
           

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
                     
                       is_it_okay = does_it_refer(commands[1], commands[2], commands[3], graph, vertices, maps, False)
                   elif commands[0] == "MUST_CONTAIN":
                       
                       is_it_okay = does_it_contain(commands[1], commands[2], commands[3], commands[4], graph, vertices, maps, False)
                   elif commands[0] == "IF_COULD_CONTAIN":
          
                       is_if = True
                       is_it_okay = does_it_contain(commands[1], commands[2], commands[3], commands[4], graph, vertices, maps, True)
          

# This function checks something is contained in the graph using the correct entity
def does_it_contain(thing_that_refers, thing_that_is_referred_to, the_entity_it_refers_with, what_the_entity_must_have, 
                                                                                             graph, vertices, maps, is_it_COULD) -> bool:
   entity_is_found = False
   is_found = False

   if thing_that_refers != "$Crate":
       if thing_that_refers in maps.keys():
           if the_entity_it_refers_with in vertices[graph[maps[thing_that_refers]]].keys():
               entity_is_found = True
               
              
               if json.dumps(vertices[graph[maps[thing_that_refers]]][the_entity_it_refers_with]) == what_the_entity_must_have:
                   is_found = True
               else:
                   if is_it_COULD:
                       print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                         ", however it COULD have ", what_the_entity_must_have, " value.")

                   else:
                       print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                         ", however it MUST have ", what_the_entity_must_have, " value.")
   else:
       thing_that_refers = "Crate"
       for item in vertices.values():
           if the_entity_it_refers_with in item.keys() and json.dumps(item[the_entity_it_refers_with]) == what_the_entity_must_have:
               entity_is_found = True
                
               maps[thing_that_is_referred_to] = item["@id"]

               if json.dumps(item[the_entity_it_refers_with]) == what_the_entity_must_have:
                   is_found = True
               else:
                   if is_it_COULD:
                       print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                         ", however it COULD have ", what_the_entity_must_have, " value.")

                   else:
                       print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                         ", however it MUST have ", what_the_entity_must_have, " value.")
                  
   if entity_is_found == False:
       if is_it_COULD:
           print(thing_that_is_referred_to, " COULD exist in ", thing_that_refers, "via", the_entity_it_refers_with, what_the_entity_must_have)
       else:
           print("Entity ", the_entity_it_refers_with, " MUST exist in ", thing_that_refers)

   if entity_is_found and is_found:
       return True
   else:
       return False
               

# This function checks something is being refered in the graph using the correct entity
def does_it_refer(thing_that_refers, thing_that_is_referred_to, the_entity_it_refers_with, graph, vertices, maps, is_it_COULD) -> bool:
   entity_is_found = False
   is_found = False
   if thing_that_refers == "$Crate":
       thing_that_refers = "Crate"
       for item in vertices.values():
           if the_entity_it_refers_with in item.keys():
               entity_is_found = True
              

               maps[thing_that_is_referred_to] = item[the_entity_it_refers_with]["@id"]
               if item[the_entity_it_refers_with]["@id"] in graph.keys():
                   is_found = True
               else:
                   print("The ", thing_that_is_referred_to, " is refered to with ", the_entity_it_refers_with,
                           " properly in", thing_that_refers,"however it is MUST be present in the graph itself as well.")
   else:
        if thing_that_refers in maps.keys():
           if the_entity_it_refers_with in vertices[graph[maps[thing_that_refers]]].keys():
               entity_is_found = True
               maps[thing_that_is_referred_to] = vertices[graph[maps[thing_that_refers]]][the_entity_it_refers_with]["@id"]
               if vertices[graph[maps[thing_that_refers]]][the_entity_it_refers_with]["@id"] in graph.keys():
                   is_found = True
               else:
                   print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                           "properly, however it is MUST be present in the graph itself as well.")
                   
  
   if entity_is_found == False:
       print("Entity ", the_entity_it_refers_with, " MUST exist in ",thing_that_refers)
                     
   if entity_is_found and is_found:
       return True
   else:
       return False


              
 

@program.command()
@click.argument('profile_path', required=True)
def check_my_profile(crate_path, profile_path):
   """This validates if the profile follows the appropriate syntax"""

   if os.path.isfile(profile_path) == False:
       click.echo("Profile file could not be found")
       click.echo("Use --help for more information")
   else:
       profile_validate()


def profile_validate():
    OpenedBracket = False
    
   # with open(profile_path) as f:
      #     for line in f:
         #      for c in line:
           #        if c != "{" and OpenedBracket == False
                    

def check_file(path_file, crate_path) -> bool:
    path_to_file = crate_path + path_file

    if os.path.isfile(path_to_file):
       return True
    else:
       return False

def check_dir(path_file, crate_path) -> bool:
    path_to_file = crate_path + path_file

    if os.path.isdir(path_to_file):
       return True
    else:
       return False

def check_string(path_file, crate_path, string_to_search) -> bool:
   path_to_file = crate_path + path_file

   with open(path_to_file, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
   return False

if __name__ == '__main__':
    program()