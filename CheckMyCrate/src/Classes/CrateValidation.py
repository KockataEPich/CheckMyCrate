import json
import os 
def compareTheCrate(array, crateGraph, crateId, workflowID, option):

    f = open("output.txt", "a")
    isItOkay = True

    for item in array:
        if crateGraph[crateId].get(item.get("@id")) != None:
            if isinstance(crateGraph[crateId].get(item.get("@id")), dict):
                itemID = crateGraph[crateId].get(item.get("@id")).get("@id")
                if crateGraph.get(itemID) != None:
                    if crateGraph.get(itemID).get("@type") != None:
                        if crateGraph.get(itemID).get("@type") == item.get("expected_type") or crateGraph.get(itemID).get("@type") in item.get("expected_type"):
                            ...
                        else:
                            f.write(item.get("@id") + "needs to reference an item of type " + json.dumps(item.get("expected_type")))
                            isItOkay = False
                    else:
                        f.write("@type must exist in the item which is referenced by " + item.get("@id"))
                        isItOkay = False
                else:
                    f.write("The entity which references the item ID is present, however the item itself does not exist in the graph " +  item.get("@id"))
                    isItOkay = False

            elif isinstance(crateGraph[crateId].get(item.get("@id")), list) and  item.get("cardinality") == "ONE":
                f.write(item.get("@id") + " entity has cardinality of ONE so it cannot be a list \n")
                isItOkay = False



        elif crateGraph[workflowID].get(item.get("@id")) != None:
            if isinstance(crateGraph[workflowID].get(item.get("@id")), dict):
                itemID = crateGraph[workflowID].get(item.get("@id")).get("@id")
                if crateGraph.get(itemID) != None:
                    if crateGraph.get(itemID).get("@type") != None:
                        if crateGraph.get(itemID).get("@type") == item.get("expected_type") or crateGraph.get(itemID).get("@type") in item.get("expected_type"):
                            ...
                        else:
                            f.write(item.get("@id") + " needs  to reference an item of type " + json.dumps(item.get("expected_type")))
                            isItOkay = False
                    else:
                        f.write("@type must exist in the item which is referenced by " + item.get("@id"))
                        isItOkay = False
                else:
                    f.write("The entity which references the item ID is present, however the item itself does not exist in the graph " + item.get("@id"))
                    isItOkay = False
        else:
            f.write("Property: " + json.dumps(item.get("@id")) + " " + option + " exist in the crate with expected @type " + json.dumps(item.get("expected_type")) + " \n" + "Description: " + item.get("description") + "\n\n")
            isItOkay = False

    return isItOkay