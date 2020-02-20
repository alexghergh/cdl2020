# CDL 2020

This is my submission for the [CDL 2020](https://cdl.rosedu.org/).

## Getting started

### Prerequisites

**Python3.8+ is required for the software to run.** To install Python3.8, see [this](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/).

Check that indeed you installed it correctly by running:

`ls -l /usr/local/bin/python*`

One of the executables listed should be `/usr/local/bin/python3.8`. That is the correct version that we will be using.

### Installing

#### 1. Create a directory for the project

After successfully installing Python3.8 or a higher version, open a command line and create a directory in which we will store the project:

`mkdir -p /home/<user>/cdl2020`

where `<user>` should be replaced with your username. If you do not know your username, type:

`whoami`

at the command line.

Change the directory to the one we created above:

`cd /home/<user>/cdl2020`

#### 2. Clone the repository

Now, we need to clone the repository by running:

`git clone https://github.com/alexghergh/cdl2020.git`

and change the directory to it:

`cd cdl2020`

#### 3. Working with a virtual environment

At this point, it is _recommended_ to create a virtual environment in which to run the code, so the system doesn't get polluted with the Python packages we are about to install. If you dont't want to do this, skip to number **4**.

**Note:** If you are running on a computer without sudo privileges, this step is **necessary**.

To create a virtual environment, simply type:

`python3.8 -m venv env`

then activate it:

`source env/bin/activate`

**Note:** To deactivate it when you are done, simply type:

`deactivate`

#### 4. Installing the requirements

Install the requirements for the project:

`pip install -r requirements.txt`

#### 5. Running the project

Everything should be done; you can simply run the program by typing:

`python main.py`

or:

`python3.8 main.py`

if you did not create a virtual environment.

**Important:** If you chose to work with a virtual environment, you need to activate and deactivate every time you run the python executable. To do this, refer to number **3**.

## How to use

If a file named `files.txt` exists, the program will scan it and will add all the file names in it to the index (assuming that no errors arise during the scan).

For the program to recognize file names, you have to have one file name per line.

Example `files.txt`:

```
# Everything starting with a # is a comment and is ignored
main.py
model/index.py
# This file lacks permissions so it won't be scanned
/etc/shadow
# This file doesn't exist
not_a_file
        # also a comment
```

Corresponding message from the program for the above `files.txt`:

```
[Success] The file "main.py" was added to index!
[Success] The file "model/index.py" was added to index!
[Error] Permission denied for "/etc/shadow"!
[Error] The file "not_a_file" does not exist!
Query: from && source
Files that matched the query:
```

The output means that both the words `from` and `source` didn't appear in any of the scanned files.

Normal example (without `files.txt`):

```
files.txt was not found, continuing with manual file addition.
File to add to index (or simply press enter for query): main.py
[Success] The file "main.py" was added to index!
File to add to index (or simply press enter for query): not_a_file.py
[Error] The file "not_a_file.py" does not exist!
File to add to index (or simply press enter for query): 
Query: from && !(source) && (source || file)
Files that matched the query: main.py
```

The output means that we found a match for the query in the file `main.py`.

### Additional configuration through the config.json file

The program supports additional tweaking for the parameters of the index through the `config.json` file.

The parameters that can be changed are:

`remove_stop_words`

This parameter specifies whether stop words should be removed. Stop words are words that don't carry information and are usually irrelevant in the context of a search engine. Such word examples are: 'as', 'so', 'me', 'I', 'am', etc.

Possible values: true, false.

Default: `false`

`stop_words_language`

This parameter changes the language through which the program does stop words removal. Basically if you have a text in english, choose english as the language.

Possible values: english, romanian.

Default: `english`

## Tests

### Code style tests

Currently, Python's 3.8 'walrus operator' is not supported by the code style module, but you can still run it by doing:

`pycodestyle --exclude=<env> .`

in the root of the project, where `<env>` is the environment name (if you followed the instructions, it should be `env`).

**Note:** Notice the **.** (dot) at the end of the command.

This should give you a code style report of the whole project.

## Author

Author: Gherghescu Alexandru (@alexghergh)

## License

This project is licensed under the terms of the MIT license.  
For more details, see [LICENSE.md](LICENSE.md).
