Contributing
====

## Description
This document explains procedures to setup development environment for this package.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Package Structure](#package-structure)
4. [Test](#test)
5. [Build for Distribution](#build-for-distribution)
6. [Style Guides](#style-guides)
7. [Example: Add supported language](#example-add-supported-language)

## Prerequisites
- OS Platform: Mac OSX
- Python version: 3.0+

## Setup 
```shell script
# Decompress archived package.
$ tar xvzf nlu-annotation-helper-x.y.z.tar.gz
$ cd nlu-annotation-helper
# Create virtual environment and activate
$ python -m venv ./venv
$ source ./venv/bin/activate
# Install dependencies 
$ pip install -e .[dev]
```

## Package Structure
```
├── src  # Source files
│   └── nlu_annotation_helper  # Module root
│       ├── annotate_utterance.py  # Command class to process annotation 
│       ├── blugolden_writerhelper.py  # Helper class to read NIF(json), write BluGoldens file
│       ├── cli.py  # Main class to be called by command line
│       └── interpretation.py  # Model class to describe interpretation attribute in NIF
│ 
├── tests  # Test files
│   ├── conftest.py  # pytest configuration
│   ├── test_annotate_utterance.py  # Test methods for annotate_utterance.py
│   ├── test_blugolden_writerhelper.py  # Test methods for blugoldens_writerhelper.py
│   └── test_interpretation.py  # Test methods for interpretation.py
│
├── .gitignore
├── CONTRIBUTING.md
├── DEVELOPMENT.md                
├── MANIFEST.in               
├── README.md                
└── setup.py  # Configuration to setup. This defines dependencies.
```

##  Test
```shell script
# Run tests
$ pytest tests/
```
 
## Build for Distribution
```shell script
# Build source distribution package
$ python setup.py sdist
# Confirm generated package
$ ls dist/
nlu-annotation-helper-x.y.z.tar.gz
```

## Style Guides
Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).

## Example: Add supported language
This section explains practical steps to add supported language as an example.
As of version 1.0.0, nlu-annotation-helper supports Japanese and Spanish only.
In this section, you're adding English supports.

1. Open `annotate_utterance.py`.
2. At the bottom, define new class named `AnnotateEnglishUtterance`. Following is the skeleton code.
3. At line 63, modify statement as follows. `instance.set_next(AnnotateSpanishUtterance()).set_next(AnnotateEnglishUtterance())`
4. Add definition of `AnnotateEnglishUtterance` to `__init__.py`.
5. Open `test_annotate_utterance.py`
6. Add `test_annotate_en` methods at the bottom. Following is the skeleton code.
7. Run tests and confirm all pass.
8. Install updates which you made via pip. Command: `$ pip install -U .[dev]`
9. Execute nlu-annotation-helper. `$ nlu-annotation-helper --json <path_to_json> --lang en`
10. See results.

annotate_utterance.py
```python
#
# (~~ existing code above ~~)
#

class AnnotateEnglishUtterance(AnnotateUtterance):
    """
    AnnotateEnglishUtterance provides annotation process for English.
    """

    def __init__(self):
        super().__init__()

    def can_annotate(self, lang: str) -> bool:
        # TODO: Determine whether a given language can be processed or not. 
        return

    def execute(self, uttr: str, slot_values: dict) -> (str, list):
        # TODO: Process annotation in English. 
        return
```

test_annotate_utterance.py
```python
#
# (~~ existing code above ~~)
#
@mark.parametrize("actual_args, expected", [
    (
        # Utterance with labelled tokens only
        {"uttr": "turn off tv", "slot_values": {"ActionTrigger": "turn", "ActionTrigger": "off","DeviceType": "tv", "Appliance": "tv"}},
        ("turn|ActionTrigger off|ActionTrigger tv|DeviceType", ['ActionTrigger', 'DeviceType'])
    )
])
def test_annotate_es(actual_args, expected):
    instance = AnnotateEnglishUtterance()
    actual = instance.execute(**actual_args)

    assert actual == expected
```

*EOD*
