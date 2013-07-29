autoinstall
===========

A simple script to make installation of deb packages automatic in ubuntu.


Usage
-----------

Run the following command with root privileges:
```python autoinstall.py -i <json-file>```

More information about the usage can be found running the command:
```python autoinstall.py -h```


Json file
------------

The json file passed as input contains the list of packages that will be installed.

The syntax of the file is a simple json array delimited by: [ ] where each item is separated by a comma (,).
Each array's item is delimited by: { } where you must specify the package's name like "name": "package-name". if the package needs to be installed using an external repository you can add the field "repository": "repository-address".

Simple example:
```
[
  {"name": "emacs"},
  {"name": "caffeine", "repository": "ppa:caffeine-developers/ppa"}
]
```

More example can be found in the files: test.json and mylist.json


Requirements
-------------

* software-properties-common (contains 'add-apt-repository' command):
  it should be there, if not ```sudo apt-get install software-properties-common```

* Python:
  it should be there, if not ```sudo apt-get install python```

* jsonpickle: ```pip install jsonpickle```

* termcolor: ```pip install termcolor```
