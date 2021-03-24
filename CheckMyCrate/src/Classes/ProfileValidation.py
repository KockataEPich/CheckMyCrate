import json
import click 

def checkProfile(profile_path):
    try:
        with open(profile_path, 'rb') as profile_path:
            profileData = json.loads(profile_path.read().decode("utf-8","ignore"))
    except:
        click.echo("The profile given is not a valid JSON file\n")
        return False

    unique_ids = {}

    if len(profileData) != 2:
        click.echo("The profile must have two entities. They are \"main_entity_type\" and \"properties\"\n")
        return False

    if profileData.get("main_entity_type") == None:
        click.echo("The profile must contain a \"main_entity_type\" entity\n")
        return False
    
    if profileData.get("properties") == None:
        click.echo("The profile must contain a \"properties\" entity\n")
        return False

    if len(profileData.get("properties")) != 3:
        click.echo("The properties array needs to contain 3 separate dictionaries\n") 
        return False

    if profileData.get("properties")[0].get("minimum") == None:
        click.echo("The dictionary of the first element must contain a \"minimum\" entity\n")
        return False

    if profileData.get("properties")[1].get("recommended") == None:
        click.echo("The dictionary of the second element must contain a \"recommended\" entity\n")
        return False

    if profileData.get("properties")[2].get("optional") == None:
        click.echo("The dictionary of the third element must contain a \"optional\" entity\n")
        return False

    return (checkItems(profileData["properties"][0]["minimum"], "minimum", unique_ids)          and
           checkItems(profileData["properties"][1]["recommended"], "recommended", unique_ids)   and
           checkItems(profileData["properties"][2]["optional"], "optional", unique_ids))


def checkItems(array, where, unique_ids):
    for item in array:

        if len(item) != 5:
            click.echo("All items must have exactly 5 attributes. They are \"@id\", \"expected_type\", \"description\", \"cardinality\" and \"value\" \n")
            return False

        if item.get("@id") == None:
            click.echo("One of the items in the " + where + " property does not have necessary entity \"@id\"\n")
            return False

        if(unique_ids.get(item.get("@id"))) != None:
            click.echo("Item with id:" + item.get("@id") + " in the \"" + where + "\" property has already been declared inside the \"" + unique_ids.get(item.get("@id")) + "\" property\n")
            return False

        unique_ids[item.get("@id")] = where

        if item.get("expected_type") == None:
            click.echo("Item with id:" + item.get("@id") + " in the " + where + " property does not have necessary entity \"expected_type\"\n")
            return False

        if item.get("description") == None:
            click.echo("Item with id:" + item.get("@id") + " in the " + where + " property does not have necessary entity \"description\"\n")
            return False

        if item.get("cardinality") == None:
            click.echo("Item with id:" + item.get("@id") + " in the " + where + " property does not have necessary entity \"cardinality\"\n")
            return False

        if item.get("cardinality") != "ONE" and item.get("cardinality") != "MANY":
            click.echo("Cardinality of item with @id:\"" + item.get("@id") + "\" can only be either \"ONE\" or \"MANY\"\n")
            return False

        if item.get("value") == None:
            click.echo("Item with id:" + item.get("@id") + " in the " + where + " property does not have necessary entity \"value\"\n")
            return False

        if not isinstance(item.get("value"), list) and item.get("value") != "NA":
            click.echo("Value of item with id:" + item.get("@id") + " in the " + where + " property must be either an array or \"NA\"")
            return False

    return True