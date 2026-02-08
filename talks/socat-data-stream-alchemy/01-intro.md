# Why Socat?

## The Digital Gardena Adapter
<figure>
    [![](gardena-adapter.jpg){width="50%" height="50%"}](https://pixabay.com/images/download/hose-pieces-402563_1920.jpg)
    <figcaption align = "center" front="small"><a href="https://pixabay.com/users/stux-12364/">stux</a></figcaption>
</figure>

::: notes
**Adapt**

- Convert between different transport mechanisms 
- Adapt: Bridge incompatible protocols e.g., TCP to UDP, serial to socket
- Expose TCP based service via UDP
- Create quick network services for testing or debugging (echo service)
- Expose hardware interfaces (e.g. serial ports) over the network
- Decouple networking code from business/application logic

**Filter**

**Transform**

- Transform: encryption, protocol conversion (bin2json)

**Aggregate**

**Isolate**

- Develop

Example tftp where exchange init is on port 69 but for futher operation
ports are "randomized"

https://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol
see operation

Use Cases

- `tcp <-> UDP`
- `Serial <-> TCP/UDP`
- `Process <-> Network`
- `SHELL <-> Network`
:::

