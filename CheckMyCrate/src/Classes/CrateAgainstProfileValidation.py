from   src.Classes.ProfileValidation import validateProfileJSONFileAndReturnTheDataObject
from   src.Classes.CrateValidation import validateCrateJSONFileAndReturnTheDataObject
import traceback
import click
import json
import os



def compareCrateToProfileSpecification(crate_path, profile_path, writeToFile):
    global crateGraph
    initializeFileIfNeeded(writeToFile)

    try:
        click.echo("Validating crate integrity...")
        crateGraph = validateCrateJSONFileAndReturnTheDataObject(crate_path)
        click.echo("Crate is OK \n")

        click.echo("Validating profile integrity...")
        profileData = validateProfileJSONFileAndReturnTheDataObject(profile_path)
        click.echo("Profile is OK \n")
    except ValueError as e:
        raise ValueError(e)

    global isCrateValid
    isCrateValid = True

    click.echo("Validating the profile specification against the crate...")
    validateEntityLoop(crateGraph.get("./"), profileData)
    
    if not isCrateValid:
        raise AttributeError()



def initializeFileIfNeeded(writeToFile):
    global writeOutToFile, f

    writeOutToFile = False
    if not writeToFile:
        return
    
    if os.path.isfile("output.txt") and writeToFile:
        os.remove("output.txt")

   
    writeOutToFile = True
    print(writeOutToFile)
    f = open("output.txt", "a")



def validateEntityLoop(entity, property):
    if property.get("property_list") == None:
        return

    for currentProperty in property.get("property_list"):
        validateEntity(entity, currentProperty, getCorrectParentPropertyName(entity, property))



def getCorrectParentPropertyName(entity, property):
    
    if property.get("property") == None:
        return "root"

    if property.get("property") == "@id":
        return entity.get("@id")

    return property.get("property")

def validateEntity(currentEntity, property, parentProperty):
    global isCrateValid
    try:
        ensurePropertyExistsInEntity(currentEntity, property, parentProperty)
        ensureValueIsCorrectIfApplicable(currentEntity, property)
        ensureCardinalitIsCorrectIfApplicable(currentEntity, property)
        checkIfPropertyHasSubPropertiesAndLoopIfItDoes(currentEntity, property)
    except ValueError as propertyNotUsedCorrectlyError:
        isCrateValid = False
        writeToProperLocation(str(propertyNotUsedCorrectlyError))
    except AttributeError as propertyNotFoundError:
        if property.get("marginality") == "MUST":
            isCrateValid = False
        writeToProperLocationIfDescription(str(propertyNotFoundError), property)

  

def ensurePropertyExistsInEntity(currentEntity, property, parentProperty):
    if currentEntity.get(property.get("property")) == None:
        raise AttributeError("Property \"" + property.get("property") + "\" " + property.get("marginality") + 
                                             " exist in \"" + parentProperty + "\"")



def ensureValueIsCorrectIfApplicable(currentEntity, property):
    if property.get("expected_value") == None:
        return
    
    if isinstance(currentEntity.get(property.get("property")), dict):
        raise ValueError("Value of property " + property.get("property") + " MUST NOT expected to be a dictionary")

    doMatch_PatternValueCheck(currentEntity, property)



def ensureCardinalitIsCorrectIfApplicable(currentEntity, property):
    if property.get("cardinality") == None:
        return

    if property.get("cardinality") == "ONE" and isinstance(currentEntity.get(property.get("property")), list):
        raise ValueError("Value of property " + property.get("property") + " MUST not be a list since the cardinality " + 
                         "in the profile file is \"ONE\"")
    


def checkIfPropertyHasSubPropertiesAndLoopIfItDoes(currentEntity, property):
    if property.get("property_list") == None:
        return 

    valueOfEntity = currentEntity.get(property.get("property"))

    if isinstance(valueOfEntity, dict):
        validateEntityLoop(valueOfEntity, property)
        return

    if isinstance(valueOfEntity, list):
        raise ValueError("The property " + property.get("property") + " MUST not have a list as value")  
        
    newEntity = crateGraph.get(valueOfEntity)

    if newEntity == None:
        raise ValueError("If Value of property " + property.get("property") + " is not a dictionary, then it MUST" +
                         " point to an entity in the array")

    validateEntityLoop(newEntity, property)



def doMatch_PatternValueCheck(currentEntity, property):
    match_pattern = property.get("match_pattern")
    expectedValue = property.get("expected_value")
    actualValue = currentEntity.get(property.get("property"))
    
    if match_pattern == "at_least_one":
        handleAtLeastOne(expectedValue, actualValue)
    elif match_pattern == "as_literal":
        handleAsLiteral(expectedValue, actualValue, property.get("property"))
    elif match_pattern == "at_least_all":
        handleAtLeastAll(expectedValue, actualValue)


def handleAtLeastOne(expectedValue, actualValue):
    for item in expectedValue:
        if item in actualValue:
            return
    else:
        raise ValueError("Value of property \"" + property.get("property") + "\" is " + json.dumps(actualValue) + 
                                                        " but it MUST contain at least one of " + json.dumps(expectedValue))



def handleAsLiteral(expected_value, actual_value, propertyName):
    
    expectedValue = json.dumps(expected_value)
    actualValue = json.dumps(actual_value)
    
    if expectedValue.find(actualValue) == -1:
        raise ValueError("Value of property \"" + propertyName + "\" is " + actualValue + " but MUST be " + expectedValue)



def handleAtLeastAll(expectedValue, actualValue):
    for item in expectedValue:
        if item not in actualValue:
                raise ValueError("Value of property \"" + property.get("property") + "\" is " + json.dumps(actualValue) + 
                                " but it MUST have all the entities in " + json.dumps(expectedValue))



def writeToProperLocation(message):
    if writeOutToFile:
        f.write("\n")
        f.write(message)
        f.write("\n")
    else:
        click.echo()
        click.echo(message)
        click.echo()



def writeToProperLocationIfDescription(errorMessage, property):
    if property.get("description") == None:
        writeToProperLocation(errorMessage + "\n" + "Description: No description provided in profile for this property")
    else:
        writeToProperLocation(errorMessage + "\n" + "Description: " + property.get("description"))