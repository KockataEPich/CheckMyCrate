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
        raise ValueError(str(e))



def checkIfProfilePathLeadsToAFile(profile_path):
   if not path.isfile(profile_path):
       raise ValueError("Invalid profile path")



def extractDataFromJsonProfile(profile_path):
    try:
        with open(profile_path, 'rb') as profile_path:
            profileData = json.loads(profile_path.read().decode("utf-8","ignore"))

        return profileData
    except ValueError as e:
        raise ValueError(str(e) + "\n" + "The profile given is not a valid JSON file \n")



def validateProfileData(profileData):
    try:
        validateRoot(profileData)
        checkForProperty_ListExistanceAndContinueRecursively(profileData)
    except ValueError as e:
        raise ValueError(str(e))



def validateRoot(profileData):
    if len(profileData) != 1 and len(profileData) != 0:
        raise ValueError("Root entity MUST have only the \"property_list\" entity")

    if profileData.get("property_list") == None:
        raise ValueError("Root entity MUST have only the \"property_list\" entity")  



def checkForProperty_ListExistanceAndContinueRecursively(propertyData):
    seenPropertiesOnThisEntity = {}

    if propertyData.get("property_list") != None:
        for property in propertyData.get("property_list"):
            try:
                validateIndividualSubEntities(property, propertyData.get("Property"))
                ensurePropertyIsUniqueInThisEntityAndAddItToDictionaryIfItIs(property, propertyData.get("Property"), seenPropertiesOnThisEntity)
            except ValueError as e:
                raise ValueError(str(e))



def validateIndividualSubEntities(property, parentPropertyName):
    try:
        ensureTheEntityContainsOnlyTheRightAttributes(property)
        ensurePropertyKeywordExistanceAndProperUse(property, parentPropertyName)
        ensureMarginalityKeywordExistanceAndProperUse(property)
        #ensureProperUseOfUsageKeyword(property)
        ensureProperUseOfCardinalityKeyword(property)
        ensureProperUseOfMatch_PatternKeyword(property)
        ensureProperUseOfDescriptionKeyword(property)
        ensureProperUseOfExpected_ValueKeyword(property)
        checkForProperty_ListExistanceAndContinueRecursively(property)

    except ValueError as e:
        raise ValueError(str(e))            
              
    

def ensurePropertyIsUniqueInThisEntityAndAddItToDictionaryIfItIs(property, parentPropertyName, seenPropertiesOnThisEntity):
    if seenPropertiesOnThisEntity.get(property.get("property")) != None:
       if parentPropertyName == None:
           parentPropertyName = "root \"./\"";

       raise ValueError("Property \"" + parentPropertyName + "\" has two properties with the same \"property\" keyword with value \"" + property.get("property") + "\"")
    
    
    seenPropertiesOnThisEntity[property.get("property")] = True



def ensureTheEntityContainsOnlyTheRightAttributes(property):
    acceptedKeywords = { 
        "property"       : True,
        "cardinality"    : True, 
        "description"    : True,
        "marginality"    : True,
        #"usage"          : True,
        "property_list"  : True,
        "match_pattern"  : True,
        "expected_value" : True
    }

    for key in property.keys():
        if acceptedKeywords.get(key) == None:
            raise ValueError("Item " + key + " is not allowed to exist")


#TODO property_list value needs to be checked that it is a list and the entities inside neede to be checked that there are dictionaries
def ensurePropertyKeywordExistanceAndProperUse(propertyData, parentPropertyName):
    if propertyData.get("property") == None:
        raise ValueError("Item with parent property \"" + parentPropertyName + "\" does not contain the mandatory \"property\" attribute")

    if not isinstance(propertyData.get("property"), str):
        raise ValueError("Item with property \"" + propertyData.get("property") + "\" MUST have a string type as a value")



def ensureMarginalityKeywordExistanceAndProperUse(propertyData):
    if propertyData.get("marginality") == None:
        raise ValueError("Attribute \"marginality\" is missing in property " + propertyData.get("property"))

    if propertyData.get("marginality") != "MUST" and propertyData.get("marginality") != "SHOULD" and propertyData.get("marginality") != "COULD":
        raise ValueError("Attribute \"marginality\" in property \"" + propertyData.get("property") + "\" can only have either MUST/SHOULD/COULD as a value")

#def ensureProperUseOfUsageKeyword(propertyData):
#    if propertyData.get("usage") != None:
#        if propertyData.get("usage") != "list" and propertyData.get("usage") != "list_of_linkers" and propertyData.get("usage") != "linker":
#            raise ValueError("Attribute \"marginality\" in property " + propertyData.get("property") + " can only have list/linker/linstLinker as a value")



def ensureProperUseOfCardinalityKeyword(propertyData):
     if propertyData.get("cardinality") != None and propertyData.get("cardinality") != "ONE" and propertyData.get("cardinality") != "MANY":
        raise ValueError("Attribute \"cardinality\" in property \"" + propertyData.get("property") + "\" can only have ONE or MANY as a value")



def ensureProperUseOfMatch_PatternKeyword(propertyData):
    if  propertyData.get("expected_value") == None and propertyData.get("match_pattern") != None:
        raise ValueError("Attribute \"match_pattern\" in property \"" + propertyData.get("property") + "\" is not appropriate since attribute" +
                         " \"expected_value\" has not been set correctly")

    if propertyData.get("match_pattern") != None and propertyData.get("match_pattern") != "for_one" and propertyData.get("match_pattern") != "for_all":
        raise ValueError("Attribute \"match_pattern\" in property \"" + propertyData.get("property") + "\" can only have for_one or for_all as a value")



def ensureProperUseOfDescriptionKeyword(propertyData):
    if propertyData.get("description") != None and not isinstance(propertyData.get("description"), str):
        raise ValueError("Attribute \"description\" in property \"" + propertyData.get("property") + "\" MUST have a string as a value")



def ensureProperUseOfExpected_ValueKeyword(propertyData):
   
    if propertyData.get("expected_value") == None:
        return

    if propertyData.get("property_list") != None:
        raiseValueError("Attribute \"expected_value\" in property \"" + propertyData.get("property") + "\" is not appropriate as the \"property_list\" keyword " + 
                                                                               "inside the entity implies that the value of the property is expected to be a dictionary")

    if isinstance(propertyData.get("expected_value"), dict) or isinstance(propertyData.get("expected_value"), list):
        raise ValueError("Attribute \"expected_value\" in property \"" + propertyData.get("property") + "\" has inappropriate value. It cannot be a list or a dictionary")


    