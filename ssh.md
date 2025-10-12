# OpenSSH Server

> [!TIP]
> El usuario `deployer` es la pieza clave en el lado del servidor. Cuando alguien intenta conectarse al servidor a través de SSH con ese nombre de usuario, el servidor busca en su archivo `/home/deployer/.ssh/authorized_keys` la clave pública correspondiente.

**Windows**: ` C:\Users\deployer\.ssh\authorized_keys`  
**Ubuntu**: `/home/deployer/.ssh/authorized_keys`

<br/>

### Proceso de conexión

Cuando intentas conectarte de nuevo desde PowerShell:

```sh
ssh -i identity_file deployer@ip_server
```

1. **Tú envías una solicitud:** Le dices al servidor **soy el usuario `deployer` y quiero entrar**.
2. **El servidor te reta:** El servidor busca en tu carpeta `/home/deployer/.ssh/` tu clave pública en `authorized_keys`, genera un mensaje aleatorio y lo cifra con ella. Este mensaje encriptado es un "reto" que le envía al cliente Powershell desde el cual te estas intentando conectar.
3. **Tú demuestras que tienes la llave:** Tu cliente de PowerShell recibe el reto y usa tu clave privada (`-i identity_file`) para descifrarlo.
4. **El servidor te deja entrar:** Una vez que tu cliente de PowerShell ha respondido correctamente, el servidor sabe que tienes la llave privada y te da acceso sin pedirte la contraseña.

> [!NOTE]
> El comando `ssh -i private_key`, **no envía** la clave privada al servidor.  
> Si no usas `-i`, el cliente buscará automáticamente la clave en su ubicación predeterminada, que generalmente es `~/.ssh/id_rsa` o `~/.ssh/id_ed25519`. 

> [!IMPORTANT]
> #### Añade la huella digital en el cliente
> `ssh-keyscan ip_server >> ~/.ssh/known_hosts` se añade a tu archivo `known_hosts` personal.

<br/>

### [SSK Key](https://documentation.ubuntu.com/server/how-to/security/openssh-server/#ssh-keys)

Genera el par de claves (publica y privada) en el cliente, ejecuta el siguente comando:

```sh
ssh-keygen -t ed25519 -C "your_email@example.com"
```

> [!NOTE]
> By default, the public key is saved in the file `~/.ssh/id_<algorithm>.pub`,  
> By default, the private key is saved in the file while `~/.ssh/id_<algorithm>`


Para que el usuario `deployer` pueda conectarse via SSH Key, agrega el contenido de la clave publica `id_ed25519.pub` (`id_rsa.pub` for RSA) en el servidor al que el usuario `deployer` desea conectarse `target_machine:~/.ssh/authorized_keys` ejecutando el sigueinte comando:

```sh
ssh-copy-id deployer@target_machine
```
