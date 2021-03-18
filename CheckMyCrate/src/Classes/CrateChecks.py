import click
import json
import src.Classes.CrateValidation as CV
import os 

def checkWorkflowCrates(crateData, profileData):

    crateData = crateData.get("@graph") 
    workflowID = checkIfIndeedWorkflowCrate(crateData)

    if isinstance(workflowID, int):
        return False


    crateGraph = {}

    for item in crateData:
        crateGraph[item.get("@id")] = item


    crateId = "./"

    # JSON arrays with their respective cardinality
    minimumMarginalityArray = profileData["properties"][0]["minimum"]
    recommendedMarginalityArray = profileData["properties"][1]["recommended"]
    optionaMarginalityArray = profileData["properties"][2]["optional"]

    if os.path.isfile("output.txt") == True:
        os.remove("output.txt")

    isItOkay = CV.compareTheCrate(minimumMarginalityArray, crateGraph, crateId, workflowID, "MUST")
    CV.compareTheCrate(recommendedMarginalityArray, crateGraph, crateId, workflowID, "SHOULD")
    CV.compareTheCrate(optionaMarginalityArray, crateGraph, crateId, workflowID, "COULD")

    return isItOkay


def checkIfIndeedWorkflowCrate(crateData):
    for position, item  in enumerate(crateData):
        if item["@id"] == "./":
            if item.get("mainEntity") == None:
                click.echo("Main Workflow must be referenced in the crate via mainEntity")
                return -1
            elif item["mainEntity"].get("@id") == None:
                click.echo("The key \"mainEntity\" exists, however it is not refercing the Main Workflow properly")
                return -1
            else:
                for position2, item2 in enumerate(crateData):
                    if item2.get("@id") == item["mainEntity"].get("@id"):
                        if item2.get("@type") != None:
                            if json.dumps(item2.get("@type")) == "[\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]":
                                 return item["mainEntity"].get("@id")
                            else:
                                 click.echo("The main entity type does not have the appropriate value. For it to be a workflow crate it needs to have a type of [\"File\", \"SoftwareSourceCode\", \"ComputationalWorkflow\"]")
                                 return -1
                        else:
                            click.echo("The main entity needs to have a @type keyword")
                            return -1

                click.echo("The Main Workflow needs to be present in the graph as well")
                return -1


    click.echo("Crate entity \"./\" inside the JSON file does not exist")
    return -1
  