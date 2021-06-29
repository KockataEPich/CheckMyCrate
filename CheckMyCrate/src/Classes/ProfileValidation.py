import json
import click
from os import path

def ValidateProfileJSONFileAndReturnTheDataObject(profile_path):
    try:
        checkIfProfilePathLeadsToAFile(profile_path)
        profileData = extractDataFromJsonProfile(profile_path)
        validateProfileData(profileData)
        return profileData
    except ValueError as e:
        raise ValueError(e)



def checkIfProfilePathLeadsToAFile(profile_path):
   if not path.isfile(profile_path):
       raise ValueError("Invalid profile path")



def extractDataFromJsonProfile(profile_path):
    with open(profile_path, 'rb') as profile_path:
         profileData = json.loads(profile_path.read().decode("utf-8","ignore"))

    return profileData



def validateProfileData(profileData):
    validateRoot(profileData)
    checkForProperty_ListExistanceAndContinueRecursively(profileData)



def validateRoot(profileData):
    if len(profileData) != 1:
        raise ValueError("Root entity MUST have only the \"property_list\" entity")

    if profileData.get("property_list") == None:
        raise ValueError("Root entity MUST have only the \"property_list\" entity")  



def checkForProperty_ListExistanceAndContinueRecursively(propertyData):
    
    if propertyData.get("property_list") == None:
        return

    seenPropertiesOnThisEntity = {}

    if not isinstance(propertyData.get("property_list"), list):
        raise ValueError("All \"property_list\" properties MUST be a list")

    parentPropertyName = getTheCorrectParrentPropertyName(propertyData)

    for property in propertyData.get("property_list"):
        try:
            validateIndividualSubEntities(property, parentPropertyName)
            ensurePropertyIsUniqueInThisEntityAndAddItToDictionaryIfItIs(property, parentPropertyName, seenPropertiesOnThisEntity)
        except ValueError as e:
            raise ValueError(e)



def getTheCorrectParrentPropertyName(propertyData):
    return propertyData.get("property") if propertyData.get("property") != None  else "root"



def validateIndividualSubEntities(property, parentPropertyName):
    ensureTheEntityContainsOnlyTheRightAttributes(property)
    ensurePropertyKeywordExistanceAndProperUse(property, parentPropertyName)
    ensureMarginalityKeywordExistanceAndProperUse(property)
    ensureProperUseOfCardinalityKeyword(property)
    ensureProperUseOfMatch_PatternKeyword(property)
    ensureProperUseOfDescriptionKeyword(property)
    ensureProperUseOfExpected_ValueKeyword(property)
    checkForProperty_ListExistanceAndContinueRecursively(property)
           
              
    

def ensurePropertyIsUniqueInThisEntityAndAddItToDictionaryIfItIs(property, parentPropertyName, seenPropertiesOnThisEntity):
    if seenPropertiesOnThisEntity.get(property.get("property")) != None:
       raise ValueError("Property \"" + parentPropertyName + "\" has two properties with the same \"property\" keyword with value \"" + property.get("property") + "\"")
    
    seenPropertiesOnThisEntity[property.get("property")] = True



def ensureTheEntityContainsOnlyTheRightAttributes(property):
    if not isinstance(property, dict):
        raise ValueError("All properties must be a dictionary")
    
    acceptedKeywords = { 
        "property"       : True,
        "cardinality"    : True, 
        "description"    : True,
        "marginality"    : True,
        "property_list"  : True,
        "match_pattern"  : True,
        "expected_value" : True
    }

    for key in property.keys():
        if acceptedKeywords.get(key) == None:
            raise ValueError("Attribute " + key + " is not recognised")


def ensurePropertyKeywordExistanceAndProperUse(propertyData, parentPropertyName):
    if propertyData.get("property") == None:
        raise ValueError("Item with parent property \"" + parentPropertyName + "\" does not contain the mandatory \"property\" attribute")

    if not isinstance(propertyData.get("property"), str):
        raise ValueError("Item with property \"" + propertyData.get("property") + "\" MUST have a string type as a value")



def ensureMarginalityKeywordExistanceAndProperUse(propertyData):
    if propertyData.get("marginality") == None:
        raise ValueError("Attribute \"marginality\" is missing in property " + propertyData.get("property"))

    if propertyData.get("marginality") != "MUST" and propertyData.get("marginality") != "SHOULD" and propertyData.get("marginality") != "COULD":
        raise ValueError("Attribute \"marginality\" in property \"" + propertyData.get("property") + "\" can only have either \"MUST\"/\"SHOULD\"/\"COULD\" as a value")


def ensureProperUseOfCardinalityKeyword(propertyData):
     if propertyData.get("cardinality") != None and propertyData.get("cardinality") != "ONE" and propertyData.get("cardinality") != "MANY":
        raise ValueError("Attribute \"cardinality\" in property \"" + propertyData.get("property") + "\" can only have \"ONE\" or \"MANY\" as a value")



def ensureProperUseOfMatch_PatternKeyword(propertyData):
    if  propertyData.get("expected_value") == None and propertyData.get("match_pattern") != None:
        raise ValueError("Attribute \"match_pattern\" in property \"" + propertyData.get("property") + "\" is not appropriate since attribute" +
                         " \"expected_value\" is missing")

    if propertyData.get("match_pattern") != None and propertyData.get("match_pattern") != "at_least_one" and propertyData.get("match_pattern") != "as_literal" and propertyData.get("match_pattern") != "at_least_all":
        raise ValueError("Attribute \"match_pattern\" in property \"" + propertyData.get("property") + "\" can only have \"at_least_one\" or \"as_literal\" or \"at_least_all\" as a value")



def ensureProperUseOfDescriptionKeyword(propertyData):
    if propertyData.get("description") != None and not isinstance(propertyData.get("description"), str):
        raise ValueError("Attribute \"description\" in property \"" + propertyData.get("property") + "\" MUST have a string as a value")



def ensureProperUseOfExpected_ValueKeyword(propertyData):
   
    if propertyData.get("expected_value") == None:
        return

    if propertyData.get("property_list") != None:
        raise ValueError("Attribute \"expected_value\" in property \"" +
                        propertyData.get("property") + "\" is not appropriate as the \"property_list\" keyword inside the "
                                                     + "entity implies that the value of the property is expected to bе "
                                                     + "a dictionary")
    
    if not isinstance(propertyData.get("expected_value"), list):
        raise ValueError("Attribute \"expected_value\" in property \"" + propertyData.get("property") + 
                         "\" has inappropriate value. It MUST be a list")

    if propertyData.get("expected_value") != None and propertyData.get("match_pattern") == None:
         raise ValueError("Attribute \"expected_value\" in property \"" + propertyData.get("property") + 
                         "\" MUST have attribute \"match_pattern\" set correctly")

    