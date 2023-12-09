# Coping with TLS

## Been There

<figure>
    [![](https-vs-http.jpeg){width="35%" height="35%"}](https://imgflip.com/i/7wj2k4)
    <figcaption align = "center" front="small">
        imgflip.com
    </figcaption>
</figure>

::: notes
What is obvious for us as a user e.g. browser (we want https)
it is not so easy to go for as dev
:::

## 🔓 Decrypting TLS

<figure>
    ![](encrypted-http-connection.png){width="85%" height="85%"}
</figure>

### 💾 Store Session Keys 

* Global

    ```{.zsh}
    export SSLKEYLOGFILE=~/session-keys.txt
    ```

* Local

    ```{.zsh}
    SSLKEYLOGFILE=~/session-keys.txt myApp
    ```

### 📥 Import Session Keys 
![](tls-session-keys-import.png)


### 💰 Profit 

<figure>
    ![](decrypted-http-connection.png){width="85%" height="85%"}
</figure>

## ⚠️ `$SSLKEYLOGFILE` ⚠️

### 🔩 Supported By
- OpenSSL
- libressl
- BoringSSL
- GnuTLS
- wolfSSL
- rusttls


### 🪤 Gotachas

* Custom Contexts
* Compile time switches
* Language specific TrustStores

