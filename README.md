# CheckMyCrate
A command line application for validating a RO-Crate object against a certain profile.


## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Guide](#guide)
	
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
