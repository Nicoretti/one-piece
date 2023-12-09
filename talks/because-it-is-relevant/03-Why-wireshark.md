# Why Wireshark?

## General Perspective

* Application/Network Trobuleshooting
* Network Optimization
* Security Analysis
* Quality Assurance
* Protocol Analysis

::: notes
- Network Engenieering
    - Network Trobuleshooting
    - Network Optimization
- Security Analysis
    - Find credentails & unprotected data
    - Suspicious traffic
        - Monitoring
        - Auditing
- Reverse Engenieering
- Application Troubleshooting
    - Client & Server
    - One part of next section
- Qualtiy Assurance
    - Function properly
    - Performance expectations are meet
:::


## Developer Perspective

* Implementation [¹](https://www.samba.org/ftp/tridge/misc/french_cafe.txt)
* Testing & Debugging
* Performance Analysis & Optimizations
* Security Analysis

::: notes
* Implementation
    - Protcol
    - Network communication
    - Understand Implementations
    - Protocol != Network .. Communication
    - Reverse Engenieering underrstanding
    - SAMBA ¹ "French Cafe techique"
* Testing
    - Extracting failure scenario payload/data
    - Regression Test
    - Integration testing
    - Performance test response time
    - protocol compliance
* Performance Analysis & Optimizations
    - Identify bottleneck
        - Client app
        - Server app
        - protocol(s)
        - network
        the nagle issue
* Security Analysis
    - Have a look what gets transfered
- Protocol Implementation
    - Visualize & Undestand the protocol
        - behavior
        - format
        - etc.
    - Understanding other implementations
    - Debugging 
    - Validate Implementation 
- Performance Analysis
    - identify bottleneck client/server/protocol/network
    Testing
    - Extract test case data from actual error
    - Validate protcol flow
:::

## Real Life Example's


### Debugging a WSS-Protocol

<figure>
    ![](software-stack.png){width="50%" height="50%"}
</figure>

::: notes
* Debugging to zoomed in (to much details, higher level conversation is relevant)
* Glue layers etc. make it hard to get the conversation
* Make sure only required test is run
* Start tracing
* filter/extract wss conversation
* cli for encoding/decoding packets
:::


### 
💻 Client
```{.JSON .numberLines}
{
    "command": "createPreparedStatement", 
    "sqlText": "INSERT INTO autoinc_pk DEFAULT VALUES"
}
```

🖥️  Server
```{.JSON .numberLines}
{   "status":"ok",
    "responseData": {
        "statementHandle":16,
        "results":[
            {"resultType":"rowCount","rowCount":0}
        ],
        "numResults":1
    }
}
```

### 

💻 Client
```{.JSON .numberLines}
{
    "command": "executePreparedStatement", "statementHandle": 16,
    "numColumns": 0, "numRows": 3, "columns": [], "data": []
}
```

🖥️  Server
```{.JSON .numberLines}
{
    "status":"error",
    "exception":
    {   
        "text":"Invalid parameter rows received. (Session: ...)",
        "sqlCode":"00000"
    }
}
```

::: notes
* Multilayerd Debugging of WSS conversation
    - Debugging Prtocol in a huge stack with third party elements
* Other Examples
    - Client connection timeout, in the connection queue
        * Example client timeout which wasn't network related
        * truth is on the wire
    - Nagle and Rate Limits algorithm and delyaed ack
        * https://www.extrahop.com/company/blog/2016/tcp-nodelay-nagle-quickack-best-practices/
        * http://www.stuartcheshire.org/papers/nagledelayedack/
:::

