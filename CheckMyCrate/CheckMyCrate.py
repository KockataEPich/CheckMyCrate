
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
    print('Welcome')

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

   # Stop the program if the paths are no specified properly
   if isItViable:
   

       must_constraint_list = []
       can_constraint_list = []

       keyword = ""
       path_file = ""

       startOfConstraint = False;
       startOfPath = False;

       with open(profile_path) as f:
           for line in f:
               for c in line:

                   if c == "}":
                       if check_file(path_file,crate_path) == False:
                           if keyword == "MUST":
                               must_constraint_list.append(path_file)

                           if keyword == "CAN":
                               can_constraint_list.append(path_file)
              
                       startOfConstraint = False;
                       startOfPath = False;
                       keyword = ""
                       path_file = ""

                   if startOfPath:
                       path_file += c

                   if c == ":":
                       startOfPath = True
                       startOfConstraint = False

                   if startOfConstraint:
                       keyword += c
     
                   if c == "{":
                       startOfConstraint = True

       total_constraint_number_errors = len(must_constraint_list) + len(can_constraint_list)

       click.echo("A total of number of constraints are not satisfied by this crate for this profile " +
              str(total_constraint_number_errors))

       click.echo("\n Must have files missing:")

       for element in must_constraint_list:
           click.echo("    " + element)

       click.echo("\n Can have files missing:")
       for element in can_constraint_list:
           click.echo("    " + element + "\n")


def check_file(path_file, crate_path) -> bool:
    path_to_file = crate_path + path_file

    if os.path.isfile(path_to_file):
       return True
    else:
       return False


if __name__ == '__main__':
    program()