import json
import click 

def checkProfile(profile_path):
    try:
        with open(profile_path, 'rb') as profile_path:
            profileData = json.loads(profile_path.read().decode("utf-8","ignore"))
    except:
        click.echo("The profile given is not a valid JSON file")
        return False

    if len(profileData) != 2:
        click.echo("The profile must have two entities. They are \"main_entity_type\ and \"properties\"")
        return False

    if profileData.get("main_entity_type") == None:
        click.echo("The profile must contain a \"main_entity_type\" entity")
        return False
    
    if profileData.get("properties") == None:
        click.echo("The profile must contain a \"properties\" entity")
        return False

    if len(profileData.get("properties")) != 3:
        click.echo("The properties array needs to contain 3 separate dictionaries") 
        return False

    if profileData.get("properties")[0].get("minimum") == None:
        click.echo("The dictionary of the first element must contain a \"minimum\" entity")
        return False

    if profileData.get("properties")[1].get("recommended") == None:
        click.echo("The dictionary of the second element must contain a \"recommended\" entity")
        return False

    if profileData.get("properties")[2].get("optional") == None:
        click.echo("The dictionary of the third element must contain a \"optional\" entity")
        return False

    return (checkItems(profileData["properties"][0]["minimum"], "minimum")          and
           checkItems(profileData["properties"][1]["recommended"], "recommended")   and
           checkItems(profileData["properties"][2]["optional"], "optional"))


def checkItems(array, where):
    for item in array:

        if len(item) != 4:
            click.echo("All items must have exactly 4 attributes. They are \"@id\", \"expected_type\", \"description\" and \"cardinality\"")
            return False

        if item.get("@id") == None:
            click.echo("One of the items in the " + where + " property does not have necessary entity \"@id\"")
            return False

        if item.get("expected_type") == None:
            click.echo("Item with id:" + item.get("@id") + " in the " + where + " property does not have necessary entity \"expected_type\"")
            return False

        if item.get("description") == None:
            click.echo("Item with id:" + item.get("@id") + " in the " + where + " property does not have necessary entity \"description\"")
            return False

        if item.get("cardinality") == None:
            click.echo("Item with id:" + item.get("@id") + " in the " + where + " property does not have necessary entity \"cardinality\"")
            return False

        if item.get("cardinality") != "ONE" and item.get("cardinality") != "MANY":
            click.echo("Cardinality of item with @id:\"" + item.get("@id") + "\" can only be either \"ONE\" or \"MANY\"")
            return False

    return True