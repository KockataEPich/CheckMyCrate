# This function checks something is being refered in the graph using the correct entity
def does_it_refer(thing_that_refers, thing_that_is_referred_to, the_entity_it_refers_with, graph, vertices, maps, is_it_COULD) -> bool:
    entity_is_found = False
    is_found = False

    option = "MUST"

    if is_it_COULD:
       option = "COULD"

    if the_entity_it_refers_with in graph[maps[thing_that_refers]].keys():
        entity_is_found = True

        if "@id" in graph[maps[thing_that_refers]][the_entity_it_refers_with]:

            if not graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"] in maps.values():
                maps[thing_that_is_referred_to] = graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"]

                if graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"] in graph.keys():
                     return True
                else:
                     print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                                            "properly, however it is MUST be present in the graph itself as well.")
            else:
                if verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, id):
                    if graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"] in graph.keys():
                        return True
                    else:
                        print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                                            "properly, however it is MUST be present in the graph itself as well.")
                else:
                    maps[thing_that_is_referred_to] = maps[thing_that_is_referred_to] = graph[maps[thing_that_refers]][the_entity_it_refers_with]["@id"]
                   
        else:
            print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                                   "inproperly in", thing_that_refers,"as it does not have \"@id\" key.")
                


    if entity_is_found == False:
        print("Entity", the_entity_it_refers_with, option,"exist in",thing_that_refers,"via",the_entity_it_refers_with)
                    
    return False

def verifyIfTheyAreTheSame(thing_that_is_referred_to, maps, id):
    for string, identity in maps.items():
        if identity == id and string == thing_that_is_referred_to:
            return True

    maps = maps.pop(string)
    return False