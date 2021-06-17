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

        for property in profileData.get("property_list"):
            validateIndividualSubEntities(property, "root")
    except ValueError as e:
        raise ValueError(str(e))

def validateRoot(profileData):
    if len(profileData) != 1 and len(profileData) != 0:
        raise ValueError("Root entity MUST have only the \"property_list\" entity")

    if profileData.get("property_list") == None:
        raise ValueError("Root entity MUST have only the \"property_list\" entity")

# TODO No Same Properties on the same depth
def validateIndividualSubEntities(profileData, parentPropertyName):
    try:
        ensureTheEntityContainsOnlyTheRightAttributes(profileData)
        ensurePropertyKeywordExistanceAndProperUse(profileData, parentPropertyName)
        ensureMarginalityKeywordExistanceAndProperUse(profileData)
        #ensureProperUseOfUsageKeyword(profileData)
        ensureProperUseOfCardinalityKeyword(profileData)
        ensureProperUseOfMatch_PatternKeyword(profileData)
        checkForProperty_ListExistanceAndContinueRecursively(profileData)
        ensureProperUseOfDescriptionKeyword(profileData)
        ensureProperUseOfExpected_ValueKeyowrd(profileData)
        
    except ValueError as e:
        raise ValueError(str(e))

def ensureTheEntityContainsOnlyTheRightAttributes(profileData):
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

    for key in profileData.keys():
        if acceptedKeywords.get(key) == None:
            raise ValueError("Item " + key + " is not allowed to exist")

def ensurePropertyKeywordExistanceAndProperUse(profileData, parentPropertyName):
    if profileData.get("property") == None:
        raise ValueError("Item with parent property \"" + parentPropertyName + "\" does not contain the mandatory \"property\" attribute")

    if not isinstance(profileData.get("property"), str):
        raise ValueError("Item with property \"" + profileData.get("property") + "\" MUST have a string type as a value")

def ensureMarginalityKeywordExistanceAndProperUse(profileData):
    if profileData.get("marginality") == None:
        raise ValueError("Attribute \"marginality\" is missing in property " + profileData.get("property"))

    if profileData.get("marginality") != "MUST" and profileData.get("marginality") != "SHOULD" and profileData.get("marginality") != "COULD":
        raise ValueError("Attribute \"marginality\" in property \"" + profileData.get("property") + "\" can only have either MUST/SHOULD/COULD as a value")

#def ensureProperUseOfUsageKeyword(profileData):
#    if profileData.get("usage") != None:
#        if profileData.get("usage") != "list" and profileData.get("usage") != "list_of_linkers" and profileData.get("usage") != "linker":
#            raise ValueError("Attribute \"marginality\" in property " + profileData.get("property") + " can only have list/linker/linstLinker as a value")

def ensureProperUseOfCardinalityKeyword(profileData):
     if profileData.get("cardinality") != None and profileData.get("cardinality") != "ONE" and profile.get("cardinality") != "MANY":
        raise ValueError("Attribute \"cardinality\" in property \"" + profileData.get("property") + "\" can only have ONE or MANY as a value")

def ensureProperUseOfMatch_PatternKeyword(profileData):
    if  profileData.get("expected_value") == None and profileData.get("match_pattern") != None:
        raise ValueError("Attribute \"match_pattern\" in property \"" + profileData.get("property") + "\" is not appropriate since attribute" +
                         " \"expected_value\" has not been set correctly")

    if profileData.get("match_pattern") != None and profileData.get("match_pattern") != "for_one" and profileData.get("match_pattern") != "for_all":
        raise ValueError("Attribute \"match_pattern\" in property \"" + profileData.get("property") + "\" can only have for_one or for_all as a value")

def checkForProperty_ListExistanceAndContinueRecursively(profileData):
    if profileData.get("property_list") != None:
        for property in profileData.get("property_list"):
            validateIndividualSubEntities(property, profileData.get("property"))

def ensureProperUseOfDescriptionKeyword(profileData):
    if profileData.get("description") != None and not isinstance(profileData.get("description"), str):
        raise ValueError("Attribute \"description\" in property \"" + profileData.get("property") + "\" MUST have a string as a value")

def ensureProperUseOfExpected_ValueKeyowrd(profileData):
   
    if profileData.get("expected_value") == None:
        return

    if profileData.get("property_list") != None:
        raiseValueError("Attribute \"expected_value\" in property \"" + profileData.get("property") + "\" is not appropriate as the \"property_list\" keyword " + 
                                                                               "inside the entity implies that the value of the property is expected to be a dictionary")

    if isinstance(profileData.get("expected_value"), dict) or isinstance(profileData.get("expected_value"), list):
        raise ValueError("Attribute \"expected_value\" in property \"" + profileData.get("property") + "\" has inappropriate value. It cannot be a list or a dictionary")