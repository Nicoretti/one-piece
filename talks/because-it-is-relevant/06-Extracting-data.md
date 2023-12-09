# Extracting Data
## 🧦 Objects

### Export Type(s)

<figure>
    ![](export-objects.png){width="70%" height="70%"}
</figure>

### Save Object(s)


<figure>
    ![](exporting-objects.png){width="85%" height="85%"}
</figure>

## 🔑 Credentials

### Credentials Menu
<figure>
    ![](credentials-menu.png){width="85%" height="85%"}
</figure>

<figure>
    ![](credentials-listing.png){width="85%" height="85%"}
</figure>

### More Details
<figure>
    ![](credentails-details.png){width="85%" height="95%"}
</figure>


## 📦 Payloads & Streams

### GUI
<figure>
    ![](tcp-conversation.png){width="85%" height="95%"}
</figure>

### Export
<figure>
    ![](export-bytes.png){width="85%" height="95%"}
</figure>

### Copy

<figure>
    ![](copy-bytes.png){width="85%" height="95%"}
</figure>


### CLI

```zsh
tshark -r ~/trace.pcapng -T ek tcp.stream eq 1 | jq 
```


```json
{
  "timestamp": "1692958244468",
  "layers": { 
    "frame": { ... },
    "eth":   { ... },
    "ip":    { ... },
    "tcp":   { ... },
    "data": {
      "data_data_data": "53:45:4d:4d:53:20:54:4f:20:57:4f:52:4b:21:0a",
      "data_data_len": "15"
    }
  }
}
```
