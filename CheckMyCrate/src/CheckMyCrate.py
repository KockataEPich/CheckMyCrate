#!/usr/bin/python3
from Classes.CheckTheCrate import checkTheCrate
from Classes.ProfileValidation import checkProfile
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

    if checkProfile(profile_path):
        click.echo("Profile is OK")
    else:
        click.echo("Profile is NOT OK")
            
@program.command()
@click.option('-f', 'writeToFile', flag_value=True,
              default=False, help=("This flag determines if the output for the crate should be written in " +
                                   "in a file or displayed in the terminal. Default:Write to terminal"))
@click.argument('crate_path', required=True)
@click.argument('profile_path', required=True)
def cc(crate_path, profile_path, writeToFile):
   """ This command compares the RO-Crate directory against a given profile \n
   The first argument is the path to the crate directory \n
   The second argument is the path to the json profile file"""

   if checkTheCrate(crate_path, profile_path, writeToFile):
       click.echo("\nThis crate abides to the given profile!")
   else:
       click.echo("\nThis crate does NOT conform to the given profile!")



if __name__ == '__main__':
    program()