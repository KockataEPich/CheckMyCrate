# CheckMyCrate
A command line application for validating a RO-Crate object against a JSON profile.

University of Manchester 2021

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Guide](#guide)
  * [Profiles](#profiles)
  * [Crates](#crates)
  * [Commands](#commands)
  * [Tips](#tips)
* [Functionality](#functionality)
  * [Profile Validation](#profile-validation)
  * [Crate Validation](#crate-validation)
* [License](#license)

## Technologies
Project is created with:
* [Python](https://www.python.org/): 3.7
* [Click](https://click.palletsprojects.com/en/7.x/): 7.00
	
## Setup
You will need **pip3** and **python3** for this installation.

Firstly, to get the repository either download the zip or use:

```
$ git clone https://github.com/KockataEPich/CheckMyCrate.git
```

After that you would neet to switch on this branch for this version.

In order to install the application, you firstly need to navigate to the
**src** folder containing the main **CheckMyCrate.py** class and the file called **setup.py**. After that
you need to execute:

```
$ pip3 install --editable .
```
After that is finished you can use the main command:

```
$ cmc 
```

Considering that everything has gone OK, after executing the above command you should see the following:

```
Usage: cmc [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cc  This command compares the RO-Crate directory against a given profile...
  pc  This command accepts a profile path and validates that it is
      following...
```

**NOTE:** So far this installation process has been tested and it works with python3 and pip3. As of now I cannot guarantee 
that it will work with just python or pip even though it might.


Alternatively, you can start the application using the conventional python3 script if all the libraries needed for the project are imported.
If that is the case then the class that needs to be started is **CheckMyCrate.py**. 

## Guide
The functionality of the application is achieved through the use of two main components:
- Profiles
- Crates

#### Profiles

A profile is a JSON file which contains the information which the crate will be verified on.

The structure resembles a tree in which the root entity has sub properties and each property can have its own sub properties.

A property can have the following attributes:
- **"property"** - The keyword itself that the program would be looking for.
- **"marginality"** - How important it is for the property to be present. Can only be **MUST**/**SHOULD**/**COULD**
- **"description"** - The description of the entity. This is only used for feedback purposes in case it is missing in the crate.
- **"cardinality"** - Can only be **ONE** or **MANY**. An item with cardinality of **ONE** cannot have a list or dictionary as a value.
- **"expected_value"** - Can only be a list which contains values that we might be looking for in that particular entity. it is combined with **"match_pattern"** to verify values.
- **"match_pattern"** - Can only be **at_least_one**/**at_least_all**/**as_literal**. It gives the instruction on how the values in list pointed by **"expected_value"** keyword can be used to determine a match: 
	 - **at_least_one** - In order for the value to pass it needs to contain at least one of the elements inside.
	 - **at_least_all** - All of the elements inside the **"expected_value"** list need to be contained in the value
	 - **as_literal** - The whole of **"expected_value"** list is taken and transfored into a string. It is then compared to the actual value as a string (including characters such as "\[" and "," )
- **"property_list"** - Can only be a list containing dictionaries. This is the continuation of the cycle. Every property inside the property_list repeats the same process as outlined above. 

<details>
  <summary>Representation of the Computational Workflow Bioschema Profile from https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE/ with only
	  the MUST marginality entities being included
</summary>
  
  ```
  {
    "property_list": [
        {
            "marginality": "MUST",
            "property": "mainEntity",
            "description": "the main entity",
            "property_list": [
                {
                    "marginality": "MUST",
                    "property": "@id",
                    "property_list": [
                        {
                            "property": "@type",
                            "marginality": "MUST",
                            "match_pattern": "at_least_all",
                            "expected_value": [ "File", "SoftwareSourceCode", "ComputationalWorkflow" ]
                        },

                        {
                            "property": "programmingLanguage",
                            "marginality": "MUST",
                            "property_list": [
                                {
                                    "marginality": "MUST",
                                    "property": "@id",
                                    "property_list": [
                                        {
                                            "property": "@type",
                                            "marginality": "MUST",
                                            "expected_value": [ "ComputerLanguage", "Text" ],
                                            "match_pattern": "at_least_one"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "property": "sdPublisher",
            "marginality": "MUST",
            "cardinality": "ONE",
            "property_list": [
                {
                    "property": "@id",
                    "marginality": "MUST",
                    "property_list": [
                        {
                            "property": "@type",
                            "marginality": "MUST",
                            "expected_value": [
                                "Organization",
                                "Person"
                            ],
                            "match_pattern": "at_least_one"
                        }
                    ]
                }
            ]
        },
        {
            "property": "license",
            "marginality": "MUST"
        },

        {
            "property": "dateCreated",
            "marginality": "MUST",
            "cardinality": "ONE"
        },

        {
            "property": "name",
            "marginality": "MUST"
        },

        {
            "property": "url",
            "marginality": "MUST",
            "cardinality": "ONE"
        },

        {
            "property": "version",
            "marginality": "MUST",
            "cardinality": "ONE"
        },

        {
            "property": "output",
            "marginality": "MUST"
        },

        {
            "property": "input",
            "marginality": "MUST"
        },

        {
            "property": "creator",
            "marginality": "MUST"
        }
    ]
}
  ```
  
</details>

#### Crates
A crate directory is defined by a **ro-crate-metadata** JSON file inside it. You can learn
more about Research Object Crates by reading the comprehensive guide on the RO-Crate website: https://www.researchobject.org/ro-crate/

#### Commands

Currently, the crate has two commands.

The first one takes a single argument which is a profile file and checks if it follows the appropriate structure.
This way a profile creator does not need to test it against a specific crate.

The way the function is invoked is:

```
$ cmc pc path/to/profile/file
```

The output is displayed on the terminal.

the second takes two arguments:
- crate directory
- profile file

This is where the **ro-crate-metadata.json** file is being validated against the profile file 
The function is:

```
$ cmc cc path/to/crate/directory path/to/profile/file
```

**NOTE:** The crate path is the whole directory not the **ro-crate-metadata.json** file.

The cc command has a single flag:
- **-f** - This flag tells the application to write the feedback on a file **output.txt** instead of on the terminal itself. The default state is write on terminal.

examples:
```
$ cmc cc -f path/to/crate/directory path/to/profile/file

```
All of this information can be found by using the the **--help** option on the respective command

#### Tips
1. A good way to follow through the feedback is to write it on a file and then use a text editor 
to search for the word **MUST**. In this way you will be able to see all the constraints that are
problematic


## Functionality
There are some intricacies to the way the program validates a crate and a profile which will be specified here.

#### Profile Validation
The profile needs to have a specific structure in order to get accepted:
- **"match_pattern"** and **"expected_value"** MUST exist together. One cannot be written without the other
- **"property_list"** and the **"match_pattern"** and **"expected_value"** due are mutualy exclusive. A value cannot be verified when **"property_list"** expects from the 
entity to be a dictionary.
- **"property"** and **"marginality"** are the only mandatory attributes a property dictionary MUST contain. Everything else can be ommited.
- The starting root profile entity can only contain the **"property_list"** and nothing else. The starting point of this is represented as the **"./"** entity inside the crate which serves as the starting point of all checks. From there on the tree cycle explained above begins.
- Two entities with the same parent cannot have the same value of the **"property"** keyword.


#### Crate Validation
- If a property in the profile contains the attribute **"property_list"** and in the crate it is a string, then it will be checked if this value refers to something inside the crate. An example for this is the **"sdPublisher"** which has the "**@id**" property. Then it can be written directly as if the "**@id**" is a dictionary even though it justs has a string value because it would be expected that it points to a dictionary inside the crate.
- The program simply traverses the crate with the pathing given in the profile and at each dead end of a branch gives feedback if something is missing/incorrect. Since there are two mains things to check, which are existance and value of a certain
keyword.

- In order for the crate to conform to the profile all the **MUST** requirements must be satisfied. In other words, if there is a **MUST** keyword in the feedback then it will not conform.

- Currently, lists cannot be traversed. They can only be evaluated with the **"expected_value"** keyword for specific values.


## License
Apache License
