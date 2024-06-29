# Konfy

Konfy is a configuration management system for GUI, TUI, REPL, and CLI applications.
It allows applications to load settings from multiple sources such as defaults, 
configuration files, environment variables, and CLI/application arguments while 
ensuring the highest priority value is provided to the user.                    

## Priority Order

Settings are loaded in the following order of priority, from highest to lowest: 

1. CLI / Application arguments                                                  
2. Environment variables                                                        
3. Configuration files:                                                         
    1. Application/Directory-specific config file                                
    2. User configuration file                                                   
    3. Default system configuration file                                         
4. Application defaults                                                         


## Examples

Here's how to use Konfy in a typical application:                               

### Example 1: Basic Usage

#### 1. Default Configuration 
TBD
                                                                                
#### 2. User Configuration
TBD
                                                                                
                                                                                
#### 3. Environment Variables:                                                       
TBD
                                                                                
#### 4. CLI Argument:                                                                
TBD
                                                                                

## Example 2: Python Integration


 ```python
from konfy import ...

TBD
```
                                                                                

### Example 3: Full Configuration

Assume you have an application that supports settings for theme, timeout, and   
verbose mode.                                                                   

#### 1. Default Configuration
TBD
                                                                                
#### 2. User Configuration
TBD
                                                                                
#### 3. Environment Variables
TBD
                                                                                
#### 4. CLI Argument
TBD
                                                                                

The resolved configuration will be:                                             

 • theme: dark (from CLI argument)                                              
 • timeout: 45 (from environment variable)                                      
 • verbose: true (from user configuration)                                      

By following this priority order, Konfy ensures the most relevant and           
user-specified configurations are always applied, making application            
configuration seamless and robust.                                              
