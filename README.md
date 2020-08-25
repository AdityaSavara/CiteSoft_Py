Requires semantic-version library
  -"pip install semantic_version"
  -"https://pypi.org/project/semantic-version/"

For the simplest way to learn how to use CiteSoft, open runExample.py then run it.  Then open the two CiteSoft txt files generated (CiteSoftwareCheckpointsLog.txt and CiteSoftwareConsolidatedLog.txt), and also MathExample.py to see what happened.

Basically, when runExample.py is run, citations are generated in a "Checkpoint" file for the module and for the functions inside MathExample.py. Finally, the citations are consolidated with duplicate entries removed.

There are two types of users of citesoft: dev-users and end-users.

FOR DEV-USERS:
There are are two syntaxes to include citations to their work. The only truly required fields are the unique_id (typically a URL or a DOI) and the software_name. The other valid_optional_fields are encouraged: ["version", "cite", "author", "doi", "url", "encoding", "misc"].  These optional fields are put into kwargs (see MathExample.py for syntax). In this module, all optional fields can be provided as lists of strings or individual strings (such as a list of authors).

1) An "import_cite" which causes a citation to be made when the the module is first imported.
CiteSoft.import_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", write_immediately=True, **kwargs)

2) A "module_call_cite" which causes a citation to be made when a function in the module is actually called.
@module_call_cite(unique_id=MathExample_unique_id, software_name="MathLib Example", **kwargs)

FOR END-USERS:
The end-user may find the CiteSoftwareConsolidatedLog.txt to be convenient, but the authoritative list is the list inside CiteSoftwareCheckpoints.txt (though the checkpoint file may include duplicates). The end-user is responsible for citing ALL software used. To facilitate easy of doing so, the dev-user should call the consolidate command when appropriate (such as at the end of a simulation).

A typical CiteSoft entry looks like below:

-
    timestamp: >-
        2020-08-25T11:43:30
    unique_id: >-
        https://docs.python.org/3/library/math.html
    software_name: >-
        The Python Library Reference: Mathematical functions
    version:
        - >-
            3.6.3 
    author:
        - >-
            Van Rossum, Guido
    cite:
        - >-
            Van Rossum, G. (2020). The Python Library Reference, release 3.8.2. Python Software Foundation.
