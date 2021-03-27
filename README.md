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

## Technologies
Project is created with:
* Python: 3.7
* Click: 7.00
	
## Setup
In order to install the application, you firstly need to navigate to the
**src** folder containg the main **CheckMyCrate.py** class and the file called **setup.py**. After that
you need to execute:

```
$ pip3 install --editable .
```
After that is finished and considering no errors have popped up you can use the main command:

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
that it will work with just python or pip even though it might

## Guide
The functionality of the application is achieved through the use of two main components:
- Profiles
- Crates

#### Profiles

A profile is a JSON file which contains the information which the crate will be verified on.

The profile contains 2 main keys:

- **"main_entity_type"** - The value of this keyword is the expected type of the main entity inside the crate object.
- **"properties"** - Has an array of 3 items which contain 3 disctinct arrays:
	- **"minimal"**
	- **"recommended"**
	- **"optional"**	

Each of these arrays contains items which match their respective marginality.

Each item has 5 keywords:
- **"@id"** - The id of the entity we are looking for inside the crate.
- **"expected_type"** - The type we expect the entity with the specified id to have.
- **"descrption"** - The description of the entity. This is only used for feedback purposes in case it is missing in the crate.
- **"cardinality"** - Can only be **ONE** or **MANY**. An item with cardinality of **ONE** cannot have an array as value.
- **"value"** - Can only be **NA** or an array with strings. These strings are the values we expect the value of this entity to contain inside the crate. This would mean that we can ask the keyword **sdPublisher** to have a value which contains one of those strings ["orcid", "otherWebsiteForContextualData"]. If the value is **NA** then the value is not checked at all. 

#### Crates


#### Commands


#### Tips
