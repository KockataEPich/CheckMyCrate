import click
import json

def checkCrateType(crateData, expected_type):
    for position, item  in enumerate(crateData):
        if item["@id"] == "./":
            if item.get("mainEntity") == None:
                click.echo("The entity \"mainEntity\" MUST exist in the crate")
                return -1
            elif item["mainEntity"].get("@id") == None:
                click.echo("The key \"mainEntity\" exists, however it is not refercing the main entity properly")
                return -1
            else:
                for position2, item2 in enumerate(crateData):
                    if item2.get("@id") == item["mainEntity"].get("@id"):
                        if item2.get("@type") != None:
                            print(expected_type)
                            if json.dumps(item2.get("@type")) in expected_type:  
                                 return item["mainEntity"].get("@id")
                            else:
                                 click.echo("The main entity @type has value: " + json.dumps(item2.get("@type")) + " but it MUST have a value of: " + json.dumps(expected_type))
                                 return -1
                        else:
                            click.echo("The main entity needs to have a @type keyword")
                            return -1


                click.echo("The main entity needs to be present in the graph as well")
                return -1


    click.echo("Crate entity \"./\" inside the JSON file does not exist")
    return -1
  