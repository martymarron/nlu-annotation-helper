NLU Annotation Helper
====
## Overview
Manual annotation work is time consuming. NLU annotation helper reduces manual work in annotation.

## Description
This is a command line tool to partially automate annotation.
Here is the basic steps to annotate an example utterance.

Example utterance(Japanese): テレビを消して (Turn off tv.)
1. Tokenize. 
    - Tokenized: テレビ を 消して
2. Decide domain and intent.
    - Domain: HomeAutomation
    - Intent: TurnOffApplianceIntent
3. Fill slots.
    - Slots:
        - テレビ|DeviceType
        - 消して|ActionTrigger

[NLUConsole](https://nluconsole-prod-pdx.pdx.proxy.amazon.com/) helps to retrieve these results, and provides results in [NIF format](https://wiki.labcollab.net/confluence/display/Doppler/NIF+-+NLU+Interpretation+Format).

NLU annotation helper converts NIF format to BluGoldens format.

So that example utterance can be tested in [dory Testing](https://wiki.labcollab.net/confluence/display/Doppler/Setting+up+Testing+in+Dory#SettingupTestinginDory-type:DATA_GOLDENS).

## Requirement
- OS Platform: Mac OSX
- Python version: 3.0+

## Install
```
# Mac OSX
$ tar xvzf nlu-annotation-helper-1.0.0.tar.gz
$ cd nlu-annotation-helper
$ pip install .
```

## Usage
```
# nlu-annotation-helper <json_path>
```
- input:
    - json_path: Required. Provide a path to json file which is [NLUConsole - Bulk Processing](https://nluconsole-prod-pdx.pdx.proxy.amazon.com/ui/bulkProcessing)
- output: 
    - qa_test/: Create BluGoldens files under this directory. For details regarding qa_test directory structure, refer [qa_test](https://code.amazon.com/packages/BluGoldens/trees/mainline/--/Alexa/ja/ja-JP/test/qa_test) directory in BluGoldens package.

## Limitation
- Supported language for annotation: Japanese 

## Author
[Masashi Kurita](maskurit@amazon.co.jp) (QAE, [Alexa International Quality](https://wiki.labcollab.net/confluence/display/AIQ/Alexa+International+Quality+%28AIQ%29+Home))


