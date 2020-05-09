NLU Annotation Helper
====

## Description
Manual annotation work is time consuming. **NLU annotation helper** reduces manual work in annotation.

**NLU annotation helper** is a command line tool to partially automate annotation.
Here is the basic steps to annotate an example utterance.

Example utterance(Japanese): テレビを消して (Turn off tv.)
1. Tokenize. 
    - Tokenized: テレビ を 消して
2. Decide domain and intent.
    - Domain: HomeAutomation
    - Intent: TurnOffApplianceIntent
3. Label tokens with slot names.
    - Labelled tokens:
        - テレビ|DeviceType
        - 消して|ActionTrigger

[NLUConsole](https://nluconsole-prod-pdx.pdx.proxy.amazon.com/) tokenize and label given utterances in [NIF format](https://wiki.labcollab.net/confluence/display/Doppler/NIF+-+NLU+Interpretation+Format).

NLU annotation helper converts NIF format to BluGoldens format.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#installation)
3. [Contributing](#contributing)
4. [Credits](#credits)
5. [Licencing](#licencing)
3. [Change Log](#change-log)

## Installation
**Requirements:**
- OS Platform: Mac OSX
- Python version: 3.0+

```
$ tar xvzf nlu-annotation-helper-x.y.z.tar.gz
$ cd nlu-annotation-helper
$ pip install .
```

## Usage
```
# nlu-annotation-helper --json <path_to_json> (--lang <lang_code>)
```
- input:
    - --json: Required. Provide a path to json file which [NLUConsole - Bulk Processing](https://nluconsole-prod-pdx.pdx.proxy.amazon.com/ui/bulkProcessing) generates.
    - --lang: Optional. Provide a language code. e.g. ja, es, ...etc.
              This tool will process a json file by a given language. 
              This tool will automatically detect the language if this argument is not provided. 
- output: 
    - fud/: Generate BluGoldens files under this directory. For details regarding fud directory structure, refer [fud](https://code.amazon.com/packages/BluGoldens/trees/mainline/--/Alexa/ja/ja-JP/test/fud) directory in BluGoldens package.

**Supported language:** \* As of v1.1.1. 
  - Japanese
  - Spanish 
  
## Contributing
See CONTRIBUTING.md.

## Credits
- [Masashi Kurita](maskurit@amazon.co.jp) (QAE, [Alexa International Quality](https://wiki.labcollab.net/confluence/display/AIQ/Alexa+International+Quality+%28AIQ%29+Home) JP)

## Licencing
For Amazon internal use only.

All rights served. 

## Change Log

- v1.0.0:
    - Initial release.
- v1.1.0:
    - Support Spanish. 

*EOD*