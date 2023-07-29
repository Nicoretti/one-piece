# Day 3 Training

* Cesar Cipher CLI
  * base func
  * flags library
  * arguments
  * input/output methods (scanner, reader, writer, ...)
* [Deep Dive into Go Package](https://app.pluralsight.com/library/courses/go-packages-deep-dive/table-of-contents)
  * Note: 1,1-1,2 speed
  * Note: good points about naming!
  * Rating:  
* [The Go Standard Library](https://app.pluralsight.com/library/courses/go-standard-library/table-of-contents)
  * Note: 1,2 speed
  * Note: just covers a couple of modules/packages
  * Rating: meh, on the side in the background stop and replay on interesting stuff

## Noteworthy

* Packages
    * match folder name
    * main can be everywhere
    * init function
      * called after/during module initialization
      * multiple once per file possible
      * order is not determined
      * not explicitly callable
    * tls package contains a tool to create self-signed certs
    * Aliasing packages
    * Import for side effect
    * Internal packages
    * Relative imports (not needed anymore)
* Vendor directories
* Logging
* Trace Logger for performance analysis etc.
