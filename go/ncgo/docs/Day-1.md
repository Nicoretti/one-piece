# Day 1 Training

* [Go: Getting Started](https://app.pluralsight.com/library/courses/getting-started-with-go/table-of-contents)
  * Note: see day 0
  * Rating: see day 0
* [Creating Custom Data Types with Go](https://app.pluralsight.com/library/courses/creating-custom-data-types-go/table-of-contents)
  * Note: 1,2-1,3 x speed
  * Rating: interesting e.g. embedding types & interfaces ...
* [Deep Dive into Functions](https://app.pluralsight.com/library/courses/deep-dive-go-functions/table-of-contents)
  * Note: 1,2-1,3 x speed
  * Rating: interesting e.g. named return values, closures, receiver types
* A Tour(s) of Go
  * Note: All are nicely done
  * Rating: nice mix between information code and ready to run example


## Noteworthy
* variable definition types (var vs :=)
  * := implicit types only
  * := within function scope only
  * builtin types have default init values 0, false, "" 
* Constants
  * numeric constants take the type needed by context
* Loops
  * For loop(s) only
* If 
  * if with statement ("walrus")
* Switch
  * with statement ("walrus")
  * implicit break after matched case
  * without condition
  * type switches
* Defer 
  * "with", scope cleanup
  * right before return
  * can be stacked
* Arrays
* Slices
  * like rust slice
  * make for create underlying array
  * append -> behaves like a vector
  * range loop idx, copy_of_val
* Maps
  * range loop key, copy_of_val
* Methods 
  * only on local types
  * Receivers / Receiver Types
  * Don't mix receiver types?
* Embedding
* Errors
* Named return values
* Closures
* Concurrency
  * go routines
  * channels / buffered channels
    * range vs value,ok (close)
  * select
  * sync package
* Generics
  * Funcs 
  * Types