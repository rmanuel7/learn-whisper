# SSH Router Port

El log de depuración (`Remote protocol version 2.0, remote software version dropbear_2019.78`) revela una información crucial: 

> [!CAUTION]
> el servidor **no está utilizando OpenSSH**, sino un servidor SSH diferente **llamado Dropbear**.

### Hipótesis sobre la causa raíz

La discrepancia entre la conexión LAN y la WAN sugiere que **estás conectándote a dos servidores SSH diferentes**:

*   **En la LAN:** La conexión va directamente a la máquina Ubuntu, que podría estar ejecutando un servidor OpenSSH por defecto o un servidor Dropbear configurado para conexiones internas.
*   **En la WAN:** La conexión pasa por el router. Algunos routers vienen con un servidor SSH incorporado (a menudo Dropbear) para administración remota. Es posible que el tráfico entrante del puerto 22 sea interceptado por el router y no se redirija a tu servidor Ubuntu.


> [!TIP]
> ### Solución recomendada: Redirigir el tráfico correctamente
> La solución más probable es que necesites configurar correctamente el **reenvío de puertos en tu router** para que el tráfico SSH pase por el router y llegue a tu servidor Ubuntu. 


<br/>

### Análisis de la situación

1.  **Conexión LAN (`192.168.1.3`):** El cliente SSH de Windows se conecta y autentica correctamente, indicando que la clave privada local y la clave pública en `authorized_keys` del servidor coinciden y el proceso funciona.

```sh
OpenSSH_for_Windows_8.1p1, LibreSSL 3.0.2
debug1: Connecting to 192.168.1.3 [192.168.1.3] port 22.
debug1: Connection established.
# debug1: identity file C:\\Users\\ADMIN\\Desktop\\id_rsa type -1
# debug1: identity file C:\\Users\\ADMIN\\Desktop\\id_rsa-cert type -1
# debug1: Local version string SSH-2.0-OpenSSH_for_Windows_8.1
✅ debug1: Remote protocol version 2.0, remote software version OpenSSH_9.6p1 Ubuntu-3ubuntu13.14
✅ debug1: match: OpenSSH_9.6p1 Ubuntu-3ubuntu13.14 pat OpenSSH* compat 0x04000000
debug1: Authenticating to 192.168.1.3:22 as 'rmanuel'
# debug1: SSH2_MSG_KEXINIT sent
# debug1: SSH2_MSG_KEXINIT received
# debug1: kex: algorithm: curve25519-sha256
# debug1: kex: host key algorithm: ecdsa-sha2-nistp256
✅ debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
✅ debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
# debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
# debug1: Server host key: ecdsa-sha2-nistp256 SHA256:S6pwyN+hsTrmQ9xpMDJ+zHT749l9HRPHqUM+b7FuBk8
# debug1: Host '192.168.1.3' is known and matches the ECDSA host key.
# debug1: Found key in C:\\Users\\ADMIN/.ssh/known_hosts:2
# debug1: rekey out after 134217728 blocks
# debug1: SSH2_MSG_NEWKEYS sent
# debug1: expecting SSH2_MSG_NEWKEYS
# debug1: SSH2_MSG_NEWKEYS received
# debug1: rekey in after 134217728 blocks
# debug1: pubkey_prepare: ssh_get_authentication_socket: No such file or directory
# debug1: Will attempt key: C:\\Users\\ADMIN\\Desktop\\id_rsa  explicit
# debug1: SSH2_MSG_EXT_INFO received
✅ debug1: kex_input_ext_info: server-sig-algs=<ssh-ed25519,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256>
✅ debug1: kex_input_ext_info: publickey-hostbound@openssh.com (unrecognised)
✅ debug1: kex_input_ext_info: ping@openssh.com (unrecognised)
debug1: SSH2_MSG_SERVICE_ACCEPT received
✅ debug1: Authentications that can continue: publickey,password
✅ debug1: Next authentication method: publickey
# debug1: Trying private key: C:\\Users\\ADMIN\\Desktop\\id_rsa
✅ debug1: Authentication succeeded (publickey).
✅ Authenticated to 192.168.1.3 ([192.168.1.3]:22).
```

<br/>

2.  **Conexión WAN (`186.123.1.30`):**
    *   La conexión **se establece** (no hay error de `Connection refused`), lo que significa que el reenvío de puertos del router está funcionando.
    *   El servidor se identifica como **`dropbear_2019.78`**. Este es un servidor SSH diferente a OpenSSH, que es el estándar en Ubuntu.
    *   El cliente de Windows OpenSSH **falla en la autenticación por clave** y recurre al método de contraseña, lo que genera el error "Permission denied".

```sh
OpenSSH_for_Windows_8.1p1, LibreSSL 3.0.2
debug1: Connecting to 186.123.1.30 [186.123.1.30] port 22.
debug1: Connection established.
# debug1: identity file C:\\Users\\ADMIN\\Desktop\\id_rsa type -1
# debug1: identity file C:\\Users\\ADMIN\\Desktop\\id_rsa-cert type -1
# debug1: Local version string SSH-2.0-OpenSSH_for_Windows_8.1
💡 debug1: Remote protocol version 2.0, remote software version dropbear_2019.78
⚠️ debug1: no match: dropbear_2019.78
debug1: Authenticating to 186.123.1.30:22 as 'exmpleuser'
# debug1: SSH2_MSG_KEXINIT sent
# debug1: SSH2_MSG_KEXINIT received
# debug1: kex: algorithm: curve25519-sha256
# debug1: kex: host key algorithm: ssh-rsa
⚠️ debug1: kex: server->client cipher: aes128-ctr MAC: hmac-sha2-256 compression: none
⚠️ debug1: kex: client->server cipher: aes128-ctr MAC: hmac-sha2-256 compression: none
# debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
# debug1: Server host key: ssh-rsa SHA256:XyTk/NeNQV/hRG2NFeSnrLOVrhJiRQ+mMgCEYLBrQc8
# debug1: Host '186.123.1.30' is known and matches the RSA host key.
# debug1: Found key in C:\\Users\\ADMIN/.ssh/known_hosts:3
# debug1: rekey out after 4294967296 blocks
# debug1: SSH2_MSG_NEWKEYS sent
# debug1: expecting SSH2_MSG_NEWKEYS
# debug1: SSH2_MSG_NEWKEYS received
# debug1: rekey in after 4294967296 blocks
# debug1: pubkey_prepare: ssh_get_authentication_socket: No such file or directory
# debug1: Will attempt key: C:\\Users\\ADMIN\\Desktop\\id_rsa  explicit
debug1: SSH2_MSG_SERVICE_ACCEPT received
❌ debug1: Authentications that can continue: password
❌ debug1: Next authentication method: password
❌ debug1: read_passphrase: can't open /dev/tty: No such file or directory
❌ exmpleuser@186.123.1.30's password:
```


