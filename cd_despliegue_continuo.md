# CD (Despliegue Continuo)

Configurar un flujo de trabajo de [GitHub Actions](https://docs.github.com/actions) para que, cuando se haga un `push` de un `tag` en la rama `main`, se conecte a mi servidor Ubuntu a través de SSH y ejecute un comando `git pull`.

### Flujo de trabajo

1. **En el servidor Ubuntu:** Ver si el servicio SSH está instalado (SSH Server).
2. **En el servidor Ubuntu:** Generar un par de claves SSH (pública y privada).
3. **En GitHub:** Añadir la clave privada como un secreto del repositorio.
4 **En el servidor Ubuntu:** Añadir la clave pública como una clave de despliegue (Deploy Key).
5. **En GitHub:** Crear el flujo de trabajo de GitHub Actions. 

## [OpenSSH Server](https://documentation.ubuntu.com/server/how-to/security/openssh-server/)

### Ver si el servicio SSH `Client` está instalado

En tu servidor Ubuntu, ejecuta este comando:

```bash
ssh -V
```

> [!NOTE]
> Si te responde algo como `OpenSSH_9.6p1 Ubuntu-3ubuntu13.14, OpenSSL 3.0.13 30 Jan 2024`, entonces **tienes SSH instalado (cliente)**.

### Ver si el servicio SSH `Server` está instalado

En tu servidor Ubuntu, ejecuta este comando:

```bash
sshd -V
```

> [!NOTE]
> Si te responde algo como `OpenSSH_9.6p1 Ubuntu-3ubuntu13.14, OpenSSL 3.0.13 30 Jan 2024`, entonces **tienes SSH instalado (server)**.

> [!IMPORTANT]
> Pero para conectarte a ese servidor, necesitas tener el **servidor SSH (sshd)** en ejecución.


### [SSH keys](https://documentation.ubuntu.com/server/how-to/security/openssh-server/#ssh-keys)

#### Generar una clave SSH en tu servidor 

Conéctate a tu servidor Ubuntu por SSH y ejecuta el siguiente comando para generar un par de claves, utilizando el algoritmo RSA (`-t rsa -b 4096`, para un tamaño de clave de 4096 bits).

```sh
ssh-keygen -t rsa -b 4096 -C "github-action-deploy"
```

> [!NOTE]
> Durante la creación, se le solicitará una frase de contraseña clave, que deberá ingresar para usar esa clave (cada vez o, en su lugar, usar un `ssh-agent(1)`). En este caso, el comentario es `-C "github-action-deploy"`.

> [!IMPORTANT]
> Cuando te pida una frase de contraseña (passphrase), déjala en blanco.

### Configurar la autenticación sin contraseña con la clave pública 

#### Añadir la clave pública: 

La clave pública generada en el paso anterior (`~/.ssh/id_rsa.pub`) debe ser añadida al archivo `~/.ssh/authorized_keys` del usuario con el que te conectarás.

```sh
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

> [!NOTE]
> - Asegúrate de que los permisos de los archivos `~/.ssh` y `~/.ssh/authorized_keys` sean correctos para que SSH no ignore el archivo.
> ```sh
> chmod 700 ~/.ssh
> chmod 600 ~/.ssh/authorized_keys
> ```
> - **Deshabilitar la autenticación por contraseña:** Una vez que la autenticación por clave funcione, puedes deshabilitar el acceso con contraseña en el archivo de configuración de SSH (`/etc/ssh/sshd_config`) para evitar ataques de fuerza bruta.
> - **Limitar el acceso:** Si es posible, restringe las conexiones SSH solo desde las direcciones IP de GitHub Actions. Esto se puede hacer con un cortafuegos (ufw).
> - **Usar un usuario dedicado:** Como se discutió anteriormente, es ideal crear un usuario específico para el despliegue automático, con permisos limitados.


<br/>

## [GitHub Secrets](https://docs.github.com/en/actions/concepts/security/secrets)

Ahora, muestra la clave privada y cópiala. La necesitarás para el siguiente paso. 

```sh
cat ~/.ssh/id_rsa
```

### Agregar la clave privada como un secreto de GitHub 

1. Ve a tu **repositorio** en GitHub.
2. Haz clic en **Settings**.
3. En la barra lateral, en la sección **Security**, haz clic en **Secrets and variables > Actions**.
4. Haz clic en **New repository secret**.
5. **Nombre el secreto** como `SSH_PRIVATE_KEY`.
6. **Pega** el contenido de tu clave privada (lo que copiaste en el paso anterior).  
   Asegúrate de incluir las líneas `-----BEGIN RSA PRIVATE KEY-----` y `-----END RSA PRIVATE KEY-----`. 
7. Crea un secreto llamado **`SSH_HOST`** con la dirección IP o el nombre de host de tu servidor.
8. Crea un secreto llamado **`SSH_USERNAME`** con el nombre del usuario de deploy.

### Agregar la clave pública como una clave de despliegue 

1. En tu servidor, muestra el contenido de tu clave pública:
   ```sh
   cat ~/.ssh/id_rsa.pub
   ```
2. Copia **todo** el contenido.
3. De vuelta en tu repositorio de GitHub, ve a **Settings > Deploy keys**.
4. Haz clic en **Add deploy key**.
5. Nombre la clave con un título descriptivo (por ejemplo, **deploy-server-ubuntu**).
6. Pega el contenido de la clave pública.
7. Marca la casilla **"Allow write access"** si necesitas que el servidor también haga push en el futuro (aunque para un simple pull no es necesario).
8. Haz clic en **Add key**.

###  Crear el flujo de trabajo de GitHub Actions

1. En tu repositorio de GitHub, ve a la pestaña **Actions**.
2. Haz clic en New workflow > **set up a workflow yourself**.
3. Nombra el archivo `deploy-on-tag.yml`.
4. Pega el siguiente código YAML:
   ```yaml
   name: Deploy on Tag
   
   on:
     push:
       tags:
         - 'v*.*.*'  # Escucha cualquier tag que comience con 'v' (ej. v1.0.0)
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
   
       steps:
         - name: Checkout repository
           uses: actions/checkout@v3
   
         - name: Deploy to Server via SSH
           uses: appleboy/ssh-action@v0.1.10
           with:
             host: ${{ secrets.SSH_HOST }}
             username: ${{ secrets.SSH_USERNAME }}
             key: ${{ secrets.SSH_PRIVATE_KEY }}
             port: 22
             script: |
               # Asegúrate de cambiar /ruta/a/tu/proyecto por la ruta real en tu servidor
               cd /ruta/a/tu/proyecto
               git pull
               # Aquí puedes añadir otros comandos, como reiniciar un servicio
               # Por ejemplo: sudo systemctl restart mi-servicio.service
   ```


