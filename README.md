# Ggit

## Introduction

This is the repository for my thesis project: a rudimentary Version Control System inspired by [Git](https://git-scm.com/) and based on a graph database, precisely [Neo4j](https://neo4j.com/).

This command line tool is implemented in python and relies on Neo4j community server database to store commits, trees and blobs as nodes and to define their relations.

This application is not meant to be used as a production tool, it's an academic project meant to gain a better understanding of how VCSs and graph databases work, and test their efficiency.

## Installing

If you wish to install and test out this tool, you can do it by cloning the repository:

```Bash
$ git clone https://github.com/RiccardoBarbieri/thesis
```

## Usage

To use this application, a pytohn3.10 or above installation is necessary.
It is also necessary for the base folder of the repository to be in your system PATH environment variable.
For example, if you cloned the repository inside `/home/username` folder, `/home/username/thesis` will be created, this is the folder that is necessary to add to PATH.
If you are in a Linux environment, you can accomplish this by adding at the end of the `~/.bashrc` file this line:

```Bash
export PATH=$PATH:"/home/username/thesis"
```

If you are in a Windows environment, just search "environment" in the Start menu and select "Edit the system environment variables", click "Environment Variables" and edit the variable called `Path` adding the path as shown above.

Furthermore requirements must be installed, they can be found in the docs/requirements.txt file, the requirements can be installed using the following command:
```
$ pip install -r requirements.txt
``` 

The main script that drives the whole application is app.py, located under ggit/app, just run the python script and instructions will appear.

Documentation about this project can be found [here](https://thesys.readthedocs.io/en/latest/).

The repository also contains a neo4j community server distribution, it will be copied insied every repository that is created.

This project is still under development.
