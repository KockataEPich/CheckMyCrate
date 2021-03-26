import click
import json

# Method that checks if the crate has the appropriate mainEntity structure
# and if the main entity type matches the one given from the profile
def checkCrateType(crateGraph, expected_type, verbose):

        if crateGraph.get("./") == None:
            click.echo("Crate entity \"./\" inside the JSON file does not exist")
            return False

        if crateGraph.get("./").get("mainEntity") == None:
            click.echo("The entity \"mainEntity\" MUST exist in the crate")
            return False

        mainEntityId = crateGraph.get("./").get("mainEntity").get("@id");

        if mainEntityId == None:
            click.echo("The key \"mainEntity\" exists, however it is not refercing the main entity with the @id keyword")
            return False 

        if crateGraph.get(mainEntityId) == None:
            click.echo("The main entity needs to be present in the graph as well")
            return False

        if (crateGraph.get(mainEntityId).get("@type") == None or 
                                    expected_type.find(json.dumps(crateGraph.get(mainEntityId).get("@type"))) == -1):
           
           click.echo("The main entity needs to have a @type entity with value: " + expected_type)
           # Depending on the verbose we either continue or we stop
           if not verbose:
               return False
           else:
               click.echo("Comparing the crate pretending that the right type was present...")
               return mainEntityId 

        return mainEntityId
                                 
                    
                            


            