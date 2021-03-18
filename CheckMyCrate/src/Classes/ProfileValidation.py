import json

def checkProfile(profile_path):
    try:
        with open(profile_path, 'rb') as profile_path:
            profileData = json.loads(profile_path.read().decode("utf-8","ignore"))
    except:
        click.echo("The profile given is not a valid JSON file")
        return False

    if profileData["@type"] == None:
        click.echo("The profile must contain a \"@type\" entity")
        return False

    if profileData["@type"] != "WorkflowCrate" and dataOfProfile["@type"] != "DataCrate":
        click.echo("The value of the \"@type\" entity must be either \"WorkflowCrate\" or \"DataCrate\"")
        return False
    
    if profileData["properties"] == None:
        click.echo("The profile must contain a \"properties\" entity")
        return False

    if len(profileData["properties"]) != 3:
        click.echo("The properties array needs to contain 3 separate dictionaries") 
        return False

    if profileData["properties"][0]["minimum"] == None:
        click.echo("The dictionary of the first element must contain a \"minimum\" entity")
        return False

    if profileData["properties"][1]["recommended"] == None:
        click.echo("The dictionary of the second element must contain a \"recommended\" entity")
        return False

    if profileData["properties"][2]["optional"] == None:
        click.echo("The dictionary of the third element must contain a \"optional\" entity")
        return False

    for item in profileData["properties"][0]["minimum"]:

        if len(item) != 4:
            click.echo("All items must have exactly 4 attributes. They are \"@id\", \"expected_type\", \"description\" and \"cardinality\"")
            return False

        if item.get("@id") == None:
            click.echo("One of the items in the \"minimum\" property does not have necessary entity \"@id\"")
            return False
        if item.get("expected_type") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"minimum\" property does not have necessary entity \"expected_type\"")
            return False

        if item.get("description") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"minimum\" property does not have necessary entity \"description\"")
            return False

        if item.get("cardinality") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"minimum\" property does not have necessary entity \"cardinality\"")
            return False

        if item.get("cardinality") != "ONE" and item.get("cardinality") != "MANY":
            click.echo("Cardinality of item with @id:\"" + item.get("@id") + "\" can only be either \"ONE\" or \"MANY\"")
            return False


    for item in profileData["properties"][1]["recommended"]:

        if len(item) != 4:
            click.echo("All items must have exactly 4 attributes. They are \"@id\", \"expected_type\", \"description\" and \"cardinality\"")
            return False

        if item.get("@id") == None:
            click.echo("One of the items in the \"recommended\" property does not have necessary entity \"@id\"")
            return False
        if item.get("expected_type") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"recommended\" property does not have necessary entity \"expected_type\"")
            return False

        if item.get("description") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"recommended\" property does not have necessary entity \"description\"")
            return False

        if item.get("cardinality") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"recommended\" property does not have necessary entity \"cardinality\"")
            return False

        if item.get("cardinality") != "ONE" and item.get("cardinality") != "MANY":
            click.echo("Cardinality of item with @id:\"" + item.get("@id") + "\" can only be either \"ONE\" or \"MANY\"")
            return False

    for item in profileData["properties"][2]["optional"]:

        if len(item) != 4:
            click.echo("All items must have exactly 4 attributes. They are \"@id\", \"expected_type\", \"description\" and \"cardinality\"")
            return False

        if item.get("@id") == None:
            click.echo("One of the items in the \"optional\" property does not have necessary entity \"@id\"")
            return False

        if item.get("expected_type") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"optional\" property does not have necessary entity \"expected_type\"")
            return False

        if item.get("description") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"optional\" property does not have necessary entity \"description\"")
            return False

        if item.get("cardinality") == None:
            click.echo("Item with id:", item.get("@id"), "in the \"optional\" property does not have necessary entity \"cardinality\"")
            return False

        if item.get("cardinality") != "ONE" and item.get("cardinality") != "MANY":
            click.echo("Cardinality of item with @id:\"" + item.get("@id") + "\" can only be either \"ONE\" or \"MANY\"")
            return False

    return True
