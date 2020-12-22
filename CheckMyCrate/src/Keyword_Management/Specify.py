import json
from src.Crate.Crate import Crate

# This method is handling the keyword SPECIFY
def does_it_specify(thing_that_refers, thing_that_is_referred_to, the_entity_it_refers_with, crate, is_it_COULD) -> bool:
    found = False
    option = "MUST" 

    if is_it_COULD:
        option = "COULD"

    if thing_that_refers == "$Crate":
        thing_that_refers = "Crate"
        if the_entity_it_refers_with in crate.vertices[crate.graph["./"]].keys():
            return True
            
    print("The", thing_that_refers,option,"specify",thing_that_is_referred_to,"via",the_entity_it_refers_with)
    return False            