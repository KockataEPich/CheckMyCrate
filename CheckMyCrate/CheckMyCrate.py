
import click
from jsonschema import validate
import json
import os.path
from os import path
import zipfile


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
    

if __name__ == '__main__':
    program()