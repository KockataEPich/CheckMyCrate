import json
import os 
import click


def compareTheCrate(array, crateGraph, crateId, mainEntityId, option, whereToWrite):
    isItOkay = 1
    missingSomething = False

    global f;
    global writeOut;

    f = ""
    writeOut = whereToWrite

    if whereToWrite:
        f = open("output.txt", "a")

    for item in array:
        # If the entity is in neither the crate nor the main entity 
        if ( crateGraph[crateId].get(item.get("@id")) == None and
           crateGraph[mainEntityId].get(item.get("@id")) == None ):

            writeToProperPlace("Property: " + json.dumps(item.get("@id")) + " " +
                               option + " exist in the crate with expected @type " + 
                               json.dumps(item.get("expected_type")) + " \n" + 
                               "Description: " + item.get("description") + "\n\n")
            # If we enter this if then there is something missing from the array in the crate
            missingSomething = True


        if crateGraph[crateId].get(item.get("@id")) == None:
            if not searchInId(item, crateGraph, mainEntityId):
                isItOkay = -1

        
        if not searchInId(item, crateGraph, crateId):
            isItOkay = -1
        
    if missingSomething and isItOkay == 1:
        isItOkay = 0 

    return isItOkay

# Method which checks
def searchInId(item, crateGraph, id):

    if isinstance(crateGraph[id].get(item.get("@id")), dict):
        itemID = crateGraph[id].get(item.get("@id")).get("@id")

        if crateGraph.get(itemID) == None:
            writeToProperPlace("The entity which references the item ID is present, however the item " +
                                    "itself MUST also exist in the graph " + item.get("@id") + "\n")
            return False

        if crateGraph.get(itemID).get("@type") == None:
            writeToProperPlace("@type MUST exist in the item which is referenced by " + 
                                                                   item.get("@id")+ "\n")
            return False


        if json.dumps(item.get("expected_type")).find(json.dumps(crateGraph.get(itemID).get("@type"))) == -1:
            writeToProperPlace("Property: " + item.get("@id") + " MUST reference an item of type "
                              + json.dumps(item.get("expected_type")) + "\n\n")
            return False

        # TODO assume that by entering a value not being NA, the user expects a contextual data
        if not checkIdForCorrectValue(itemID, item):
            return False
            
    # If it is a list we need to check if the cardinality of the entity allows it
    if isinstance(crateGraph[id].get(item.get("@id")), list):

        if item.get("cardinality") == "ONE":
            writeToProperPlace("The cardinality of item with @id " + item.get("@id") + 
                               " is ONE and thus the value of the key MUST not be a list \n \n")
            return False

    # if it is just a straight up value we need to check if it is appropriate
    if not checkIdForCorrectValue(crateGraph[id].get(item.get("@id")), item):
        return False
        

    return True

# Method which checks if the value is being followed in the entity
def checkIdForCorrectValue(valueToCheck, item):

    if not isinstance(item.get("value"), list):
        return True

    for value in item.get("value"):
        if json.dumps(valueToCheck).find(value) != -1:
            return True

    writeToProperPlace("Property: " + item.get("@id") + " MUST reference a value which contains one of these: " 
                       + json.dumps(item.get("value")) + "\n\n")
    return False


# Method which receives a message and writes it on the proper place
def writeToProperPlace(message):
    if writeOut:
        f.write(message)
    else:
        click.echo(message)