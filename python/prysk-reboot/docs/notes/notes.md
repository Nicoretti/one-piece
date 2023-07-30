!!! Note

    This folder only contains notes and WIP status documents and therefore aren't included
    in the documentation build.


# Ideas

## What can it be used for?
Test setup(s) using/replacing/argument tests based on:
* curl
* httpie
* jetbrains web thingy 
### Why
* don't depend on a proprietary tool
* provide custom checks
* command to restore prepare an environment 

## Extension(s)
* custom input format
* custom diff "check"
* custom patch (x)


## CLI
* Interactive is a CLI switch rather than part of the config/input
* Logging and its settings is part of the cli configuration
* Options for saving and isolation of environment
* Inherit env flag
* Check feature support of specdown, prysk and insta

## Schema & Formats
* Having "no-diff"/"no-expectation" as expectation for an output will remove warnings regarding
  an unchecked output.
* Generic (runtime/target) more flexible but less checks
  just forward arguments

## Engine?

### Runtimes
* Shell
* Python

### Inputs
* stdin

### Outputs
* file
* stdout
* stderr

### Formats/Types
* text
  * encoding
* binary
  * endianess?
* json
  * encoding?
* yaml
  * encoding?
* csv
  * encoding?

### diffs? (diff formats)
* no-diff
* text-diff
* json-diff
* yaml-diff
* csv-diff
* binary-diff

### patch
* patch (std patch)
* binary-patch
* custom-patch

# Customization Example
* HTTP request
* runtime: generic -> httpie
* target: httpie
  * args: 
* impl -> prysk-http-response-diff
* impl -> prysk-http-response-patch
