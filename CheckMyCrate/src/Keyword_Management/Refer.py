# This function checks something is being refered in the graph using the correct entity
def does_it_refer(thing_that_refers, thing_that_is_referred_to, the_entity_it_refers_with, graph, vertices, maps, is_it_COULD) -> bool:
   entity_is_found = False
   is_found = False
   if thing_that_refers == "$Crate":
       thing_that_refers = "Crate"
       for item in vertices.values():
           if the_entity_it_refers_with in item.keys():
               entity_is_found = True
              

               maps[thing_that_is_referred_to] = item[the_entity_it_refers_with]["@id"]
               if item[the_entity_it_refers_with]["@id"] in graph.keys():
                   is_found = True
               else:
                   print("The ", thing_that_is_referred_to, " is refered to with ", the_entity_it_refers_with,
                           " properly in", thing_that_refers,"however it is MUST be present in the graph itself as well.")
   else:
        if thing_that_refers in maps.keys():
           if the_entity_it_refers_with in vertices[graph[maps[thing_that_refers]]].keys():
               entity_is_found = True
               maps[thing_that_is_referred_to] = vertices[graph[maps[thing_that_refers]]][the_entity_it_refers_with]["@id"]
               if vertices[graph[maps[thing_that_refers]]][the_entity_it_refers_with]["@id"] in graph.keys():
                   is_found = True
               else:
                   print("The", thing_that_is_referred_to, "is refered to with", the_entity_it_refers_with,
                           "properly, however it is MUST be present in the graph itself as well.")

   if entity_is_found == False:
      print("Entity ", the_entity_it_refers_with, " MUST exist in ",thing_that_refers)
                     
   if entity_is_found and is_found:
       return True
   else:
       return False