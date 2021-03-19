#!/usr/bin/python3
import Classes.CheckTheCrate as CTC
import Classes.ProfileValidation as PV
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

    if PV.checkProfile(profile_path):
        click.echo("Profile is OK")
    else:
        click.echo("Profile is NOT OK")
            
@program.command()
@click.argument('crate_path', required=True)
@click.argument('profile_path', required=True)
def cc(crate_path, profile_path):
   """ This command compares the RO-Crate directory against a given profile \n
   The first argument is the path to the crate directory \n
   The second argument is the path to the json profile file"""
   click.echo("Validating the crate against the profile...")

   if CTC.checkTheCrate(crate_path, profile_path):
       click.echo("This crate abides to the given profile!")
   else:
       click.echo("This crate does NOT abides to the given profile!")



if __name__ == '__main__':
    program()