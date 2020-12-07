import json


# This function checks something is contained in the graph using the correct entity
def does_it_contain(thing_that_refers, thing_that_is_referred_to, the_entity_it_refers_with, what_the_entity_must_have, 
                                                                                             graph, vertices, maps, is_it_COULD) -> bool:
   entity_is_found = False
   is_found = False

   if thing_that_refers == "$Crate":
       thing_that_refers = "Crate"
       for item in vertices.values():
           if the_entity_it_refers_with in item.keys() and json.dumps(item[the_entity_it_refers_with]) == what_the_entity_must_have:
               entity_is_found = True
                
               maps[thing_that_is_referred_to] = item["@id"]

               if json.dumps(item[the_entity_it_refers_with]) == what_the_entity_must_have:
                   is_found = True
               else:
                   if is_it_COULD:
                       print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                         ", however it COULD have ", what_the_entity_must_have, " value.")

                   else:
                       print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                         ", however it MUST have ", what_the_entity_must_have, " value.")

   elif thing_that_refers in maps.keys():
       if the_entity_it_refers_with in vertices[graph[maps[thing_that_refers]]].keys():
           entity_is_found = True
               
              
       if json.dumps(vertices[graph[maps[thing_that_refers]]][the_entity_it_refers_with]) == what_the_entity_must_have:
           is_found = True
       else:
           if is_it_COULD:
               print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                                                     ", however it COULD have ", what_the_entity_must_have, " value.")

           else:
               print("Entity ", the_entity_it_refers_with, " exists in ", thing_that_refers , 
                         ", however it MUST have ", what_the_entity_must_have, " value.")       
                  
   if entity_is_found == False:
       if is_it_COULD:
           print(thing_that_is_referred_to, " COULD exist in ", thing_that_refers, "via", the_entity_it_refers_with, what_the_entity_must_have)
       else:
           print(thing_that_is_referred_to, " MUST exist in ", thing_that_refers, "via", the_entity_it_refers_with, what_the_entity_must_have)

   if entity_is_found and is_found:
       return True
   else:
       return False