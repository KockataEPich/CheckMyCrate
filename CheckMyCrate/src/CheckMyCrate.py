#!/usr/bin/python3
import sys
sys.path.append('../')
from src.Classes.CrateAgainstProfileValidation import compareCrateToProfileSpecification
from src.Classes.ProfileValidation import ValidateProfileJSONFileAndReturnTheDataObject
import click


@click.group()
def program():
    click.echo('Welcome to CheckMyCrate! \n')



@program.command()
@click.argument('profile_path', required=True)
def pc(profile_path):
    """ This command accepts a profile path and validates that it is following the correct structure \n
    The first and only argument is the path to the json profile file"""
    click.echo("Checking the profile....")

    try:
        ValidateProfileJSONFileAndReturnTheDataObject(profile_path)
        click.echo("Profile is OK")
    except Exception as e:
        click.echo(str(e))
        click.echo("Profile is NOT OK")


   
@program.command()
@click.option('-f', 'writeToFile', flag_value=True,
              default=False, help=("This flag determines if the output for the crate should be written in " +
                                   "in a file or displayed in the terminal. Default: write to terminal"))
@click.argument('crate_path', required=True)
@click.argument('profile_path', required=True)
def cc(crate_path, profile_path, writeToFile):
    """ This command compares the RO-Crate directory against a given profile \n
    The first argument is the path to the crate directory \n
    The second argument is the path to the json profile file"""

    try:
        compareCrateToProfileSpecification(crate_path, profile_path, writeToFile)
        click.echo("This crate abides to the given profile!")
    except ValueError as vE:
        click.echo(str(vE))
    except AttributeError as aE:
        click.echo("This crate does NOT conform to the given profile!")

if __name__ == '__main__':
    program()