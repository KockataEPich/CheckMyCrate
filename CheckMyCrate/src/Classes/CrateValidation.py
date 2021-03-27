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
            # If we enter this if then there is something missing in the crate
            missingSomething = True


        if crateGraph[crateId].get(item.get("@id")) == None:
            if not searchInId(item, crateGraph, mainEntityId):
                isItOkay = -1

        
        elif not searchInId(item, crateGraph, crateId):
            isItOkay = -1
        
    if missingSomething and isItOkay == 1:
        isItOkay = 0 

    return isItOkay

# Method which checks
def searchInId(item, crateGraph, id):

    if isinstance(crateGraph[id].get(item.get("@id")), dict):
        itemID = crateGraph[id].get(item.get("@id")).get("@id")

        if itemID == None:
            writeToProperPlace("The entity " + item.get("@id") + " is present, however there is no \"@id\" " +
                                    "property inside it to reference an item \n")
            return False

        referencedItem = crateGraph.get(itemID)

        if referencedItem == None:
            writeToProperPlace("The entity " + item.get("@id") + " is present, however the item " +
                                    "which it refers to MUST also exist in the graph \n")
            return False

        if referencedItem.get("@type") == None:
            writeToProperPlace("@type MUST exist in the item which is referenced by " + 
                                                                   item.get("@id")+ "\n")
            return False


        if json.dumps(item.get("expected_type")).find(json.dumps(referencedItem.get("@type"))) == -1:
            writeToProperPlace("Property: " + item.get("@id") + " MUST reference an item of type "
                              + json.dumps(item.get("expected_type")) + "\n\n")
            return False

        # TODO assume that by entering a value not being NA, the user expects a contextual data
        return checkContextualEntityForCorrectValue(referencedItem, item)

            
    # If it is a list we need to check if the cardinality of the entity allows it
    if isinstance(crateGraph[id].get(item.get("@id")), list):

        if item.get("cardinality") == "ONE":
            writeToProperPlace("The cardinality of item with @id " + item.get("@id") + 
                               " is ONE and thus the value of the key MUST not be a list \n \n")
            return False

        return True

    # if it is just a straight up value we need to check if it is appropriate

    return  checkIdForCorrectValue(crateGraph[id].get(item.get("@id")), item)

# Method which confirms if the value inside the contextual data matches the profile requirements
def checkContextualEntityForCorrectValue(referencedItem, item):
    
    # If the value in the profile is NA then we skip this check
    if not isinstance(item.get("value"), list):
        return True

    if referencedItem.get("identifier") == None:
        writeToProperPlace("The entity " + item.get("@id") + " is expected to " +
                           "be a contextual entity, which means it MUST have " +
                           "the \"identifier\" keyword \n")
        return False

    if isinstance(referencedItem.get("identifier"), list):
        writeToProperPlace("The entity " + item.get("@id") + " MUST NOT have an entity " +
                           "\"identifier\" with an array as value \n")
        return False

    if isinstance(referencedItem.get("identifier"), str):
        return checkIdForCorrectValue(referencedItem.get("identifier"), item)

    
    if referencedItem.get("identifier").get("@id") == None:
        writeToProperPlace("In entity " + item.get("@id") +  "\"identifier\" MUST contain " +
                            " they keyword \"@id\" \n")
        return False


    return checkIdForCorrectValue(referencedItem.get("identifier").get("@id"), item)



# Method which checks if the value is being followed in the entity
def checkIdForCorrectValue(valueToCheck, item):

    # If the value in the profile is NA then we skip this check
    if not isinstance(item.get("value"), list):
        return True

    

    for value in item.get("value"):
        if json.dumps(valueToCheck).find(value) != -1:
            return True

    writeToProperPlace("Property: " + item.get("@id") + " MUST reference an identifier " +
                       "value which contains one of these: " + json.dumps(item.get("value")) + "\n\n")
    return False


# Method which receives a message and writes it on the proper place
def writeToProperPlace(message):
    if writeOut:
        f.write(message)
    else:
        click.echo(message)