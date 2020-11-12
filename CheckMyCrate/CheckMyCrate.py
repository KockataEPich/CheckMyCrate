
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

   # Stop the program if the paths are no specified properly
   if isItViable:
   
       # Constraint lists for feedback purposes
       must_constraint_list = []
       can_constraint_list = []

       dir_must_missing_list = []
       dir_can_missing_list = []

       must_strings_missing_list = {}
       can_strings_missing_list = {}

       files_for_must_strings_missing_list = {}
       files_for_can_strings_missing_list = {}


       keyword = ""
       path_file = ""

       startOfConstraint = False
       startOfPath = False
       isStringConstraint = False

       # Read constraints and check for them
       with open(profile_path) as f:
           for line in f:
               for c in line:

                   if c == "}":
                       if check_dir(path_file,crate_path) == False:

                           if keyword == "DMUST":
                               dir_must_missing_list.append(path_file)

                           if keyword == "DCAN":
                               dir_can_missing_list.append(path_file)

                       if check_file(path_file,crate_path) == False:
                           if keyword == "FMUST":
                               must_constraint_list.append(path_file)

                           if keyword == "FCAN":
                               can_constraint_list.append(path_file)

                       if keyword == "SCAN" or keyword == "SMUST":
                           file_and_string = path_file.split(":")
                                              
                           if check_file(file_and_string[0], crate_path) == False:
                               if keyword == "SMUST":
                                   files_for_must_strings_missing_list[file_and_string[1]] = file_and_string[0] 
                         
                               if keyword == "SCAN":
                                   files_for_can_strings_missing_list[file_and_string[1]] = file_and_string[0] 
                           else:
                               if check_string(file_and_string[0],crate_path, file_and_string[1]) == False:
                                   if keyword == "SMUST":
                                       must_strings_missing_list[file_and_string[1]] = file_and_string[0] 
                         
                                   if keyword == "SCAN":
                                       can_strings_missing_list[file_and_string[1]] = file_and_string[0]
              
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

       click.echo("Total of number of file constraints are not satisfied by this crate for this profile " +
              str(total_constraint_number_errors))

       click.echo("\n   Must have files missing:")

       for element in must_constraint_list:
           click.echo("      " + element)

       click.echo("\n   Can have files missing:")
       for element in can_constraint_list:
           click.echo("      " + element + "\n")
           
       #############################################################
       click.echo("\nTotal of number of directory constraints are not satisfied by this crate for this profile " +
              str(len(dir_must_missing_list) + len(dir_can_missing_list)))

       click.echo("\n   Must have directories missing:")

       for element in dir_must_missing_list:
           click.echo("      " + element)

       click.echo("\n   Can have directories missing:")
       for element in dir_can_missing_list:
           click.echo("      " + element + "\n")

       ############################################################
       click.echo("\nTotal of number of string constraints are not satisfied by this crate because their file is missing:" +
              str(len(files_for_must_strings_missing_list) + len(files_for_can_strings_missing_list)))

       click.echo("\n")

       for key,value in files_for_must_strings_missing_list.items():
           click.echo("The MUST string:" + key + " is missing because the file:" + value + " could not be found" )

          
       click.echo("\n")
       for key,value in files_for_can_strings_missing_list.items():
           click.echo("The CAN string:" + key + " is missing because the file:" + value + " could not be found" )

       ###################################################################################
       click.echo("\nTotal of number of string constraints are not satisfied by this crate because they are missing from the specified files:" +
           str(len(must_strings_missing_list) + len(can_strings_missing_list)))

       click.echo("\n")

       for key,value in must_strings_missing_list.items():
           click.echo("The MUST string:" + key + " is missing int file:" + value)

       click.echo("\n")
       for key,value in can_strings_missing_list.items():
           click.echo("The CAN string:" + key + " is missing in the file:" + value)


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