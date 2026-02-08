# Demo

::: notes
- Reverse Shell & Bind Shell: TBD
- Serial log with socat and systemd: TBD
- [virtserial](https://gist.github.com/Nicoretti/adc15ca6de05747666fa9721fde0e38e)
- Serial-Log Duplication: TBD
    ```shell
    socat -d -d system:"python virtserial.py",pty  PTY,raw,link=/tmp/pty500
    ```
- Mapping Serial to Unix socket a serial to unix socket
:::

## Serial over TCP over UDP

1. Serial <-> TCP-Server
2. TCP-Client <-> UDP-Server
3. UDP-Server <-> UDP-Client

## Test Server for Custom Protocol(s)

### Binary Protocol

```
+-----------+-------------------+-----------------------+
| **Byte**  | **Description**   | **Values**            |
+-----------+-------------------+-----------------------+
| Byte 0    | Transformation    | 0x00: None            |
|           |                   | 0x01: Upper           |
|           |                   | 0x02: Lower           |
+-----------+-------------------+-----------------------+
| Byte 1    | Length            | 0-255 (Single byte)   |
+-----------+-------------------+-----------------------+
| Bytes 2+  | String Data       | Raw ASCII/UTF-8 bytes |
+-----------+-------------------+-----------------------+
```

### Example Packet

**Input:** "hello" → Uppercase

| Field | Value | Hex |
| :--- | :--- | :--- |
| **Transformation** | Uppercase | `0x01` |
| **Length** | 5 | `0x05` |
| **String** | "hello" | `68 65 6C 6C 6F` |

### JSON Decoder

Input:

```
Payload: 0x01 0x05 0x68 0x65 0x6C 0x6C 0x6F
```

Output:

```json
{
  "Transformation": "Upper",
  "String": "hello"
}
```

### JSON Encoder

Input:

```json
{
  "Transformation": "Upper",
  "String": "hello"
}
```

Output:

```
Payload: 0x01 0x05 0x68 0x65 0x6C 0x6C 0x6F
```

### Server Application

1. `Decode (decode.py)`
2. `Transform (server.py)`
3. `Encode (encode.py)`

::: notes

Pitfalls:
- Interpreter buffering

::: 
