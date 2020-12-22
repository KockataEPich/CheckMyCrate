import json


# This function checks something is contained in the graph using the correct entity
def does_it_contain(thing_that_is_referred_to, the_entity_it_refers_with, what_the_entity_must_have, 
                                                                                             graph, vertices, maps, is_it_COULD) -> bool:
    option = "MUST"

    if is_it_COULD:
        option = "COULD"

    for item in vertices.values():
        if the_entity_it_refers_with in item.keys() and json.dumps(item[the_entity_it_refers_with]) == what_the_entity_must_have:
            if item["@id"] not in maps.values():
                maps[thing_that_is_referred_to] = item["@id"]
                return True
            else:
                if verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, item["@id"]):
                    return True
           
    print(thing_that_is_referred_to, option, "exist in", thing_that_is_referred_to, "via", the_entity_it_refers_with, what_the_entity_must_have)

    return False



def verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, id):
    for string, identity in maps.items():
        if identity == id and string == thing_that_is_referred_to:
            return True
    
    return False