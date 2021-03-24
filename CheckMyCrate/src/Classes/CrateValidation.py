import json
import os 
import click

def compareTheCrate(array, crateGraph, crateId, mainEntityId, option, whereToWrite):
    isItOkay = 1
    missingSomething = False

    f = ""
    if whereToWrite:
        f = open("output.txt", "a")

    for item in array:
        if crateGraph[crateId].get(item.get("@id")) != None:
            if not searchInId(item, crateGraph, crateId, option, whereToWrite, f):
                isItOkay = -1
        elif crateGraph[mainEntityId].get(item.get("@id")):
            if not searchInId(item, crateGraph, mainEntityId, option, whereToWrite, f):
                isItOkay = -1
        else:
            if whereToWrite:
                f.write("Property: " + json.dumps(item.get("@id")) + " " + option + " exist in the crate with expected @type " + json.dumps(item.get("expected_type")) + " \n" + "Description: " + item.get("description") + "\n\n")
            else:
                click.echo("Property: " + json.dumps(item.get("@id")) + " " + option + " exist in the crate with expected @type " + json.dumps(item.get("expected_type")) + " \n" + "Description: " + item.get("description") + "\n\n")
            missingSomething = True
        
    if missingSomething and isItOkay == 1:
        isItOkay = 0 

    return isItOkay


def searchInId(item, crateGraph, id, option, whereToWrite, f):

    if isinstance(crateGraph[id].get(item.get("@id")), dict):
        itemID = crateGraph[id].get(item.get("@id")).get("@id")

        if not checkIdForCorrectValue(itemID, item, whereToWrite, f):
            return False

        if crateGraph.get(itemID) != None:
            if crateGraph.get(itemID).get("@type") != None:
                if not json.dumps(crateGraph.get(itemID).get("@type")) in json.dumps(item.get("expected_type")):
                    if whereToWrite:
                        f.write("Property: " + item.get("@id") + " MUST reference an item of type " + json.dumps(item.get("expected_type")) + "\n\n")
                    else:
                        click.echo("Property: " + item.get("@id") + " MUST reference an item of type " + json.dumps(item.get("expected_type"))+ "\n\n")
                    return False
            else:
                if whereToWrite:
                    f.write("@type MUST exist in the item which is referenced by " + item.get("@id")+ "\n")
                else:
                    click.echo("@type MUST exist in the item which is referenced by " + item.get("@id")+ "\n")
                return False
        else:
            if whereToWrite:
                f.write("The entity which references the item ID is present, however the item itself MUST also exist in the graph " + item.get("@id") + "\n")
            else:
                click.echo("The entity which references the item ID is present, however the item itself MUST also exist in the graph " + item.get("@id") + "\n")
            return False

    elif isinstance(crateGraph[id].get(item.get("@id")), list):
        
        if item.get("cardinality") == "ONE":
             if whereToWrite:
                f.write("The cardinality of item with @id " + item.get("@id") + " is ONE and thus the value of the key MUST not be a list \n \n")
             else:
                click.echo("The cardinality of item with @id " + item.get("@id") + " is ONE and thus the value of the key MUST not be a list \n \n")
             return False

    else:
        itemID = crateGraph[id].get(item.get("@id"))
        if not checkIdForCorrectValue(itemID, item, whereToWrite, f):
            return False
        

    return True


def checkIdForCorrectValue(itemID, item, whereToWrite, f):
    correctValue = False

    if isinstance(item.get("value"), list):
            for value in item.get("value"):
                if json.dumps(itemID).find(value) != -1:
                    print("not here")
                    correctValue = True
    else:
        correctValue = True

    if not correctValue:
        if whereToWrite:
            f.write("Property: " + item.get("@id") + " MUST reference a value which contains one of these: " + json.dumps(item.get("value")) + "\n\n")
        else:
            click.echo("Property: " + item.get("@id") + " MUST reference a value which contains one of these: " + json.dumps(item.get("value")) + "\n\n")
        return False

    return True