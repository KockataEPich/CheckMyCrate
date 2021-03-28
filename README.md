# CheckMyCrate
A command line application for validating a RO-Crate object against a certain profile.


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

The profile contains 2 main keys:

- **"main_entity_type"** - The value of this keyword is the expected type of the main entity inside the crate object.
- **"properties"** - Has an array of 3 items which contain 3 distinct arrays:
	- **"minimum"**
	- **"recommended"**
	- **"optional"**	

Each of these arrays contains items which match their respective marginality.

Each item has 5 keywords:
- **"@id"** - The id of the entity we are looking for inside the crate.
- **"expected_type"** - The type we expect the entity with the specified id to have.
- **"description"** - The description of the entity. This is only used for feedback purposes in case it is missing in the crate.
- **"cardinality"** - Can only be **ONE** or **MANY**. An item with cardinality of **ONE** cannot have an array as value.
- **"value"** - Can only be **NA** or an array with strings. These strings are the values we expect the value of this entity to contain inside the crate. This would mean that we can ask the keyword **sdPublisher** to have a value which contains one of those strings ["orcid", "otherWebsiteForContextualData"]. If the value is **NA** then the value is not checked at all. 

<details>
  <summary>Profile template</summary>
  
  ```
  {
    "main_entity_type": "YOUR VALUE HERE",
    "properties": [
        {

            "minimum": [
                {
                    "@id": "The entity key",
                    "cardinality": "Cardinality - MANY/ONE",
                    "description": "Description of the entity",
                    "expected_type": "The type of the entity if it is referenced in the graph",
                    "value": "NA"
                },

                {
                    "@id": "The entity2 key",
                    "cardinality": "Cardinality - MANY/ONE",
                    "description": "Description of the entity2",
                    "expected_type": "The type of the entity2 if it is referenced in the graph",
                    "value": "NA"
                }

            ]
        },


        {
            "recommended": [

                {
                    "@id": "The entity key",
                    "cardinality": "Cardinality - MANY/ONE",
                    "description": "Description of the entity",
                    "expected_type": "The type of the entity if it is referenced in the graph",
                    "value": "NA"
                },

                {
                    "@id": "The entity2 key",
                    "cardinality": "Cardinality - MANY/ONE",
                    "description": "Description of the entity2",
                    "expected_type": "The type of the entity2 if it is referenced in the graph",
                    "value": "NA"
                }
            ]
        },

        {
            "optional": [
                {
                    "@id": "The entity key",
                    "cardinality": "Cardinality - MANY/ONE",
                    "description": "Description of the entity",
                    "expected_type": "The type of the entity if it is referenced in the graph",
                    "value": "NA"
                },

                {
                    "@id": "The entity2 key",
                    "cardinality": "Cardinality - MANY/ONE",
                    "description": "Description of the entity2",
                    "expected_type": "The type of the entity2 if it is referenced in the graph",
                    "value": "NA"
                }

            ]
        }

    ]
}
  ```
  
</details>

<details>
  <summary>Representation of the Computational Workflow Bioschema Profile from https://bioschemas.org/profiles/ComputationalWorkflow/0.5-DRAFT-2020_07_21
</summary>
  
  ```
  {
    "main_entity_type": ["File", "SoftwareSourceCode", "ComputationalWorkflow"],
    "properties": [
        {

            "minimum": [
                {
                    "@id": "creator",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],

                    "description": "The creator/author of this CreativeWork. This is the same as the Author property for CreativeWork.",
                    "cardinality": "MANY",
                    "value": "NA"
                },


                {
                    "@id": "dateCreated",
                    "expected_type": [
                        "Date",
                        "DateTime"
                    ],
                    "description": "The date on which the CreativeWork was created or the item was added to a DataFeed.",
                    "cardinality": "ONE",
                    "value": "NA"
                },



                {
                    "@id": "input",
                    "expected_type": "FormalParameter",
                    "description": "an input required to use the workflow (eg. xl spreadsheet, xml file, …)",
                    "cardinality": "MANY",
                    "value": "NA"
                },


                {
                    "@id": "license",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The license of the workflow",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "name",
                    "expected_type": "Text",
                    "description": "The name of the item.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "output",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "The output of the workflow",
                    "cardinality": "MANY",
                    "value": "NA"
                },



                {
                    "@id": "programmingLanguage",
                    "expected_type": "ComputerLanguage",
                    "description": "The computer programming language",
                    "cardinality": "MANY",
                    "value": ["galaxy", "some_other_workflow"]
                },

                {
                    "@id": "sdPublisher",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],
                    "description": "Main workflow description",
                    "cardinality": "MANY",
                    "value": [ "orcid" ]
                },

                {
                    "@id": "url",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "cardinality": "MANY",
                    "description": "Main workflow description",
                    "value": "NA"
                },


                {
                    "@id": "version",
                    "expected_type": [ "CreativeWork", "URL" ],
                    "description": "Main workflow description",
                    "cardinality": "MANY",
                    "value": "NA"
                }
            ]
        },


        {
            "recommended": [
                {
                    "@id": "citation",
                    "cardinality": "MANY",
                    "description": "A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.",
                    "expected_type": [
                        "CreativeWork",
                        "Text"
                    ],
                    "value": "NA"
                },

                {
                    "@id": "contributor",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],
                    "description": "A secondary contributor to the CreativeWork or Event.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "creativeWorkStatus",
                    "expected_type": [
                        "DefinedTerm",
                        "Text"
                    ],
                    "description": "The status of a creative work in terms of its stage in a lifecycle. Example terms include Incomplete, Draft, Published, Obsolete. Some organizations define a set of terms for the stages of their publication lifecycle.",
                    "cardinality": "ONE",
                    "value": "NA"
                },

                {
                    "@id": "description",
                    "expected_type": "Text",
                    "description": "A description of the item.",
                    "cardinality": "ONE",
                    "value": "NA"
                },

                {
                    "@id": "funding",
                    "expected_type": "Grant",
                    "description": "A description of the item.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "hasPart",
                    "expected_type": "CreativeWork",
                    "description": "Indicates an item or CreativeWork that is part of this item, or CreativeWork (in some sense). Inverse property: isPartOf.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "isBasedOn",
                    "expected_type": [
                        "CreativeWork",
                        "Product",
                        "URL"
                    ],
                    "description": "A resource from which this work is derived or from which it is a modification or adaption. Supersedes isBasedOnUrl.",
                    "cardinality": "ONE",
                    "value": "NA"
                },

                {
                    "@id": "keywords",
                    "expected_type": "Text",
                    "description": "Keywords or tags used to describe this content. Multiple entries in a keywords list are typically delimited by commas.",
                    "cardinality": "ONE",
                    "value": "NA"
                },

                {
                    "@id": "maintainer",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],
                    "description": "A maintainer of a Dataset, software package (SoftwareApplication), or other Project. A maintainer is a Person or Organization that manages contributions to, and/or publication of, some (typically complex) artifact. It is common for distributions of software and data to be based on “upstream” sources. When maintainer is applied to a specific version of something e.g. a particular version or packaging of a Dataset, it is always possible that the upstream source has a different maintainer. The isBasedOn property can be used to indicate such relationships between datasets to make the different maintenance roles clear. Similarly in the case of software, a package may have dedicated maintainers working on integration into software distributions such as Ubuntu, as well as upstream maintainers of the underlying work.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "producer",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],
                    "description": "The person or organization who produced the workflow.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "publisher",
                    "expected_type": [
                        "Organization",
                        "Person"
                    ],
                    "description": "The publisher of the creative work.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "runtimePlatform",
                    "expected_type": "Text",
                    "description": "Runtime platform or script interpreter dependencies (Example - Java v1, Python2.3, .Net Framework 3.0). Supersedes runtime.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "softwareRequirements",
                    "expected_type": [
                        "Text",
                        "URL"
                    ],
                    "description": "Component dependency requirements for application. This includes runtime environments and shared libraries that are not included in the application distribution package, but required to run the application (Examples: DirectX, Java or .NET runtime). Supersedes requirements.",
                    "cardinality": "MANY",
                    "value": "NA"
                },

                {
                    "@id": "targetProduct",
                    "expected_type": "SoftwareApplication",
                    "description": "Target Operating System / Product to which the code applies. If applies to several versions, just the product name can be used.",
                    "cardinality": "MANY",
                    "value": "NA"
                }


            ]
        },


        {
            "optional": [
                {
                    "@id": "subjectOf",
                    "expected_type": [ "File", "SoftwareSourceCode", "ComputationalWorkflow" ],
                    "description": "Main workflow description",
                    "cardinality": "ONE",
                    "value": "NA"
                },
                {
                    "@id": "alternateName",
                    "expected_type": "Text",
                    "description": "An alias for the item",
                    "cardinality": "MANY",
                    "value": "NA"
                },
                {
                    "@id": "conditionsOfAccess",
                    "expected_type": "Text",
                    "description": "Conditions that affect the availability of, or method(s) of access to, an item. Typically used for real world items such as an ArchiveComponent held by an ArchiveOrganization. This property is not suitable for use as a general Web access control mechanism. It is expressed only in natural language.For example “Available by appointment from the Reading Room” or “Accessible only from logged-in accounts “.",
                    "cardinality": "ONE",
                    "value": "NA"
                },
                {
                    "@id": "dateModified",
                    "expected_type": [
                        "Date",
                        "DateTime"
                    ],
                    "description": "The date on which the CreativeWork was most recently modified or when the item’s entry was modified within a DataFeed.",
                    "cardinality": "ONE",
                    "value": "NA"
                },
                {
                    "@id": "datePublished",
                    "expected_type": "Date",
                    "description": "Date of first broadcast/publication.",
                    "cardinality": "ONE",
                    "value": "NA"
                },

                {
                    "@id": "encodingFormat",
                    "expected_type": [
                        "Text",
                        "URL"
                    ],
                    "description": "Media type typically expressed using a MIME format (see IANA siteand MDN reference) e.g. application/zip for a SoftwareApplication binary, audio/mpeg for .mp3 etc.).In cases where a CreativeWork has several media type representations, encoding can be used to indicate each MediaObject alongside particular encodingFormat information.Unregistered or niche encoding and file formats can be indicated instead via the most appropriate URL, e.g. defining Web page or a Wikipedia/Wikidata entry. Supersedes fileFormat.",
                    "cardinality": "MANY",
                    "value": "NA"
                },
                {
                    "@id": "identifier",
                    "expected_type": [
                        "PropertyValue",
                        "Text",
                        "URL"
                    ],
                    "description": "The identifier property represents any kind of identifier for any kind of Thing, such as ISBNs, GTIN codes, UUIDs etc. Schema.org provides dedicated properties for representing many of these, either as textual strings or as URL (URI) links.",
                    "cardinality": "MANY",
                    "value": ["awpajwpfijapwf" ,"workflowhub.eu" ]
                },

                {
                    "@id": "image",
                    "expected_type": [ "File", "ImageObject" ],
                    "description": "An image of the item. This can be a URL or a fully described ImageObject",
                    "cardinality": "MANY",
                    "value": "NA"
                }
            ]
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

The cc command has 2 flags:
- **-f** - This flag tells the application to write the feedback on a file **output.txt** instead of on the terminal itself. The default state is write on terminal.
- **-v** - This flag tells the application to continue giving feedback even if the main entity type is not appropriate. The default state is don't continue.

examples:
```
$ cmc cc -f path/to/crate/directory path/to/profile/file

$ cmc cc -v path/to/crate/directory path/to/profile/file

$ cmc cc -fv path/to/crate/directory path/to/profile/file
```
All of this information can be found by using the the **--help** option on the respective command

#### Tips
1. A good way to follow through the feedback is to write it on a file and then use a text editor 
to search for the word **MUST**. In this way you will be able to see all the constraints that are
problematic


## Functionality
There are some intricacies to the way the program validates a crate and a profile which will be specified here.

#### Profile Validation
The profile needs to have a specific structure in order to get accepted. The position of the keywords does not matter, however
the three marginality arrays need to be in in this exact order:

1. **"minimum"**
2. **"recommended"**
3. **"optional"**

Another point of interest is that no entity can be omitted. 

There can be no two **"@id"** inside the profile with the same value.

#### Crate Validation

1. After checking that the crate has the right main entity, the program searches through the 
crate entity defined by **@id** of **"./"** for the specified keyword in the profile. If it doesn't find it,
CheckMyCrate scans the main entity defined by the **mainEntity** keyword. If it is not present in either,
no further searches are conducted and the entity is assumed to be missing.

2. When evaluating the marginality arrays against the crate, every item in their corresponding array is assigned the following marginality:
	- **"minimum"** - **MUST**
	- **"recommended"** - **SHOULD**
	- **"optional"** - **COULD**
	
	In order for the crate to conform to the profile all the **MUST** requirements must be satisfied. In other words, if there is a **MUST** keyword in the feedback then it will not conform.

	Items from the **"recommended"** and **"optional"** arrays do not impact conformity if they are not present, however if they are they **MUST** follow given requirements in the profile. Basically, if the profile has an item in the **"optional"** array that has an **"image"** id and type **"painting"** then if the **"image"** keyword is indeed present in the crate but does not have the specified type, the output will produce a **MUST** problem and conclude that the crate does **NOT** conform even if all the items in the **"minimum"** array are satisfied. If the keyword **image** was not present then it will not produce a **MUST** problem and it will not impact conformity.


3. When validating inside a crate, and the value of a specific keyword is an array inside the crate, the only check that is done is if the cardinality of the item in the profile allows it. As of now there is not functionality to loop through array values and validate the items inside them.


4. If the **"value"** keyword is not **"NA"** in the profile, then the profile creator assumes that a contextual data with an **"identifier"** keyword is expected inside the specified item.  If the item keyword is found in the crate and the value of that keyword is just plain string, then that string is checked if it contains one of the values specified in the profile. If the value is a dictionary which leads to another item in the graph of the crate, then the program will look for the **"identifier"** keyword and compare the values to that.


## License
Apache License
