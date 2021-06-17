import json
import click 

# Method which checks if the given profile path leads to a valid
# profile file that follows the requirements

def checkProfile(profile_path):
    try:
        profileData = extractDataFromJsonProfile(profile_path)
        validateProfileData(profileData)

        return profileData
    except ValueError as e:
        click.echo(e)
        return False

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

def validateIndividualSubEntities(profileData, parentPropertyName):
    try:
        ensureTheEntityContainsOnlyTheRightAttributes(profileData)
        ensurePropertyKeywordExistanceAndProperUse(profileData, parentPropertyName)
        ensureMarginalityKeywordExistanceAndProperUse(profileData)
        ensureProperUseOfUsageKeyword(profileData)
        ensureProperUseOfCardinalityKeyword(profileData)
        ensurePorperUseOfMatch_PatternKeyword(profileData)
        checkForProperty_ListExistanceAndContinueRecursively(profileData)
    except ValueError as e:
        raise ValueError(str(e))

def ensureTheEntityContainsOnlyTheRightAttributes(profileData):
    acceptedKeywords = { 
        "property"       : True,
        "cardinality"    : True, 
        "description"    : True,
        "marginality"    : True,
        "usage"          : True,
        "property_list"  : True,
        "match_pattern"  : True,
        "expected_value" : True
    }

    for key in profileData.keys():
        if acceptedKeywords.get(key) == None:
            raise ValueError("Item " + key + " is not allowed to exist")

def ensurePropertyKeywordExistanceAndProperUse(profileData, parentPropertyName):
    if profileData.get("property") == None:
        raise ValueError("Item with parent property " + parentPropertyName +
                            " does not contain the mandatory \"property\" attribute")

    if not isinstance(profileData.get("property"), str):
        raise ValueError("Item with property " + profileData.get("property") + " MUST have a string type as a value")

def ensureMarginalityKeywordExistanceAndProperUse(profileData):
    if profileData.get("marginality") == None:
        raise ValueError("Attribute \"marginality\" is missing in property " + profileData.get("property"))

    if profileData.get("marginality") != "MUST" and profileData.get("marginality") != "SHOULD" and profileData.get("marginality") != "COULD":
        raise ValueError("Attribute \"marginality\" in property " + profileData.get("property") + " can only have either MUST/SHOULD/COULD as a value")

def ensureProperUseOfUsageKeyword(profileData):
    if profileData.get("usage") != None:
        if profileData.get("usage") != "list" and profileData.get("usage") != "listLinker" and profileData.get("usage") != "linker":
            raise ValueError("Attribute \"marginality\" in property " + profileData.get("property") + " can only have list/linker/linstLinker as a value")

def ensureProperUseOfCardinalityKeyword(profileData):
     if profileData.get("cardinality") != None and profileData.get("cardinality") != "ONE" and profile.get("cardinality") != "MANY":
        raise ValueError("Attribute \"cardinality\" in property " + profileData.get("property") + " can only have ONE or MANY as a value")

def ensurePorperUseOfMatch_PatternKeyword(profileData):
    if (profileData.get("usage") == None or profileData.get("usage") == "linker" ) and profileData.get("match_pattern") != None:
        raise ValueError("Attribute \"match_pattern\" in property " + profileData.get("property") + " is not appropriate since attribute" +
                         " \"usage\" has not been set correctly with either list or listLinker")

    if profileData.get("match_pattern") != None and profileData.get("match_pattern") != "for_one" and profile.get("match_pattern") != "for_all":
        raise ValueError("Attribute \"match_pattern\" in property " + profileData.get("property") + " can only have for_one or for_all as a value")

def checkForProperty_ListExistanceAndContinueRecursively(profileData):
    if profileData.get("property_list") != None:
        for property in profileData.get("property_list"):
            validateIndividualSubEntities(property, profileData.get("property"))