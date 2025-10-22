## [Instalación de Asterisk](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/What-to-Download/)

Antes de instalar el software Asterisk, debemos asegurarnos de que nuestro **sistema operativo esté actualizado**, para ello ejecutamos los siguientes comandos:

#### [Update and upgrade packages](https://learn.microsoft.com/en-us/windows/wsl/setup/environment#update-and-upgrade-packages)

We recommend that you regularly update and upgrade your packages using the preferred package manager for the distribution. For Ubuntu or Debian, use the command:

```coffeescript
sudo apt update && sudo apt upgrade
```

#### [Upgrade the package manager database](https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnetcore/practice-troubleshoot-linux/1-2-linux-special-directories-users-package-managers#upgrade-the-package-manager-database)

##### To update the package database on Ubuntu

```coffeescript
sudo apt update
```

> [!NOTE]
> *   The update command **doesn't actually upgrade** any of the installed software packages.
> *   Instead, it updates the package database.

##### To upgrade any of the installed software packages on Ubuntu

```coffeescript
sudo apt upgrade
```

<br/>

### [Downloading Asterisk](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/What-to-Download/)

Browse to [https://downloads.asterisk.org/pub/telephony/asterisk](https://downloads.asterisk.org/pub/telephony/asterisk), select `asterisk-14-current.tar.gz`, and save the file on your file system.

You can also get the latest releases from the downloads page on asterisk.org.

Alternatively, you can use `wget` to retrieve the latest release:

```shell
[root@server:/usr/local/src]# wget https://downloads.asterisk.org/pub/telephony/asterisk/asterisk-14-current.tar.gz
--2017-04-28 15:45:36-- https://downloads.asterisk.org/pub/telephony/asterisk/asterisk-14-current.tar.gz
Resolving downloads.asterisk.org (downloads.asterisk.org)... 76.164.171.238
Connecting to downloads.asterisk.org (downloads.asterisk.org)|76.164.171.238|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 40692588 (39M) [application/x-gzip]
Saving to: ‘asterisk-14-current.tar.gz’

asterisk-14-current.tar.gz 100%[======================================================================>] 38.81M 3.32MB/s in 12s 

2017-04-28 15:45:47 (3.37 MB/s) - ‘asterisk-14-current.tar.gz’ saved [40692588/40692588]
```

> [!NOTE]
> *   Asegúrate de realizar las descargas en `/usr/local/src`.  
> *   `/usr/local/src` parece ser el lugar convencional y este directorio debería estar vacío en una instalación nueva.

<br/>

### 3.1 Programa y dependencias


```coffeescript
sudo apt install wget build-essential subversion
```

> [!IMPORTANT]
> The most important packages the `build-essential` package

> [!NOTE]
> The command `sudo apt install wget build-essential subversion` is used on Debian-based Linux distributions
> (like Ubuntu, Linux Mint) to install three specific packages:
> 
> - `wget`: A command-line utility for retrieving files from the web. 
>    It supports HTTP, HTTPS, and FTP protocols, and can be used to download 
>    single files or recursively download entire websites.
> 
> - `build-essential`: A meta-package containing a collection of essential tools
>    required for compiling software from source code. This typically includes 
>    the GNU C/C++ compiler (GCC/G++), `make`, and other necessary development
>    libraries and headers.
> 
> - `subversion`: A version control system, often referred to as SVN, used for 
>    tracking changes in files and directories, and for managing collaborative 
>    development projects.

<br/>

**Descargamos Asterisk 15.7.1 y descomprimimos** el paquete:

```coffeescript
cd "/usr/local/src/"
```

```coffeescript
sudo wget "http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-15.7.1.tar.gz"
```

```coffeescript
sudo tar zxf "asterisk-15.7.1.tar.gz"
```

> [!NOTE]
> El comando `sudo tar zxf [nombre_del_archivo]` extrae los contenidos de un archivo
> `tar.gz` o `tar.bz2` (o similar):
> 
> - `sudo` para ejecutarlo con permisos de superusuario,
> - `tar` para el programa de archivado,
> - `z` para descompresión con `gzip`,
> - `x` para extraer, y 
> - `f` para especificar el archivo de entrada.

<br/>

### [Configuring Asterisk](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/Prerequisites/Checking-Asterisk-Requirements/#configuring-asterisk)

Now it's time to compile and install Asterisk. Let's change to the directory which contains the Asterisk source code.

```coffeescript
cd "asterisk-15.7.1/"
```

Procedemos a la **instalación de las dependencias** de Asterisk:

```coffeescript
sudo contrib/scripts/get_mp3_source.sh
```

The [`install_prereq`](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/Prerequisites/Checking-Asterisk-Requirements/#using-install_prereq) script is included with every release of Asterisk in the `contrib/scripts` subdirectory. The script has the following options:

*   `test` - print only the libraries to be installed.
*   `install` - install package dependencies only. Depending on your distribution of Linux, version of Asterisk, and capabilities you wish to use, this may be sufficient.
*   `install-unpackaged` - install dependencies that don't have packages but only have tarballs. You may need these dependencies for certain capabilities in Asterisk.

```coffeescript
sudo contrib/scripts/install_prereq install
```

<img width="1350" height="705" alt="ITU-T_Union_Internacional_Telecomunicaciones" src="https://github.com/user-attachments/assets/fc09f3ce-c8d0-42a8-b159-fc1f11e48309" />

> [!NOTE]
> *   **ITU-T** son las siglas en inglés de la **Unión Internacional de Telecomunicaciones - Sector de Normalización de las Telecomunicaciones**.
> *   **57** para Colombia

<br/>

<img width="546" height="111" alt="image" src="https://github.com/user-attachments/assets/cdf9cb66-ecf3-465e-af1d-cdaa6253811f" />

<br/>
<br/>

Next, we'll run a command called ./configure, which will perform a number of checks on the operating system, and get the Asterisk code ready to compile on this particular server.

*   Preparamos el **código para compilar**:

```coffeescript
sudo ./configure
```

*   Una vez finalizado se mostrará lo siguiente:

<img width="803" height="721" alt="image" src="https://github.com/user-attachments/assets/ab9bd912-8561-4942-aca5-de0088eb5c1a" />

<br/>
<br/>
 
### [Using Menuselect](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/Using-Menuselect-to-Select-Asterisk-Options/#using-menuselect)

The next step in the build process is to tell Asterisk which [modules](https://docs.asterisk.org/Fundamentals/Asterisk-Architecture/Types-of-Asterisk-Modules) to compile and install, as well as set various compiler options. These settings are all controlled via a menu-driven system called Menuselect. To access the **Menuselect** system, type:

Seleccionamos los **módulos a compilar**:

```coffeescript
sudo make menuselect
```

<img width="1479" height="789" alt="image" src="https://github.com/user-attachments/assets/e4b45565-9251-4ead-9d9d-fa30f1354bec" />

<br/>
<br/>


 ### [Using the Bundled Version of pjproject](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/Prerequisites/PJSIP-pjproject/#usage)

 *   First, run `./contrib/scripts/install_prereq`.
 *   Building the bundled pjproject **requires the python development libraries** which `install_prereq` installs.
 *   All you have to do now is add the `--with-pjproject-bundled` option to your Asterisk `./configure` command line and remove any other `--with-pjproject` option you may have specified.
 
**Compilamos**:

```coffeescript
sudo make -j2
```

> [!NOTE]
> `make -j$(nproc)` is a powerful shell command used in Linux and other Unix-like systems to significantly speed up the compilation of software. It works by combining three elements: 
> 
> *   `make`: An automation tool that manages the building of executable programs and other files from source code.
> *   `-j`: A `make` command-line option that specifies the **number of jobs** (commands) to run simultaneously.
> *   `$(nproc)`: A command substitution that executes the `nproc` command and passes its output as the argument for the `-j` option. 

<img width="581" height="196" alt="image" src="https://github.com/user-attachments/assets/bf3b403c-e174-42b0-807a-4e182d96a119" />

<br/>
<br/>

 
### [Build and Install Instructions](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/Building-and-Installing-Asterisk/)

Now we can compile and install Asterisk. To compile Asterisk, simply type make at the Linux command line.

**Instalamos** Asterisk:

```coffeescript
sudo make install
```

<img width="565" height="622" alt="image" src="https://github.com/user-attachments/assets/2014ce73-a970-4c76-9e1a-8bad9b9fec67" />

<br/>
<br/>


 ### [Installing Initialization Scripts](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/Installing-Initialization-Scripts/)
 
*   Now that you have Asterisk compiled and installed, **the last step is to install the initialization script, or initscript**.
*   This script starts Asterisk when your server starts, will monitor the Asterisk process in case anything bad happens to it, and can be used to stop or restart Asterisk as well.
*   To install the initscript, use the make config command.

Por último, **instalaremos el script de inicio** y **actualizaremos la memoria caché de las bibliotecas compartidas:**

```coffeescript
sudo make config
```

```coffeescript
sudo ldconfig 
```

<br/>

### [Executing as another User](https://docs.asterisk.org/Operation/Running-Asterisk/?h=user)

#### Creación de un usuario en Asterisk

Como Asterisk se ejecuta como usuario administrador, **crearemos un nuevo usuario** y configuraremos el programa para que se ejecute con el nuevo usuario.

**Crearemos un usuario llamado *asterisk***:

```coffeescript
sudo adduser --system --group --home "/var/lib/asterisk" --no-create-home --gecos "Asterisk PBX" asterisk
```

> [!NOTE]
> * `--system`: Le indica a `adduser` que cree un usuario de sistema para ejecutar servicios y aplicaciones.
> * `--group`: Crea un grupo con el mismo nombre que el usuario (`asterisk`).
> * `--home /var/lib/asterisk`: Establece el directorio de inicio del usuario como `/var/lib/asterisk`.
> * `--no-create-home`: A pesar de que se especifica un directorio de inicio, esta opción le dice al comando que no lo cree automáticamente. El instalador de Asterisk ya habrá creado o creará este directorio más tarde.
> * `--gecos "Asterisk PBX"`: GECOS (o GCOS) es un campo que se usa para almacenar información adicional sobre el usuario, como su nombre completo o un comentario. En este caso, se usa para identificar el propósito del usuario: "Asterisk PBX".
> * `asterisk`: Es el nombre del usuario y del grupo que se van a crear.

<br/>

Abrimos el siguiente archivo y **descomentamos las siguientes líneas**:

```coffeescript
sudo vim "/etc/default/asterisk"
```

> AST_USER="asterisk"\
> AST_GROUP="asterisk"

<img width="812" height="237" alt="image" src="https://github.com/user-attachments/assets/b7cbe86a-b83c-46fc-b6c5-9ae4551c1a6f" />

<br/>
<br/>

**Añadimos nuestro nuevo usuario a los grupos *dialout* y *audio***:

```coffeescript
sudo usermod -a -G dialout,audio asterisk
```

### [Directory and File Structure](https://docs.asterisk.org/Fundamentals/Directory-and-File-Structure/)

The top level directories used by Asterisk can be configured in the [`asterisk.conf`](https://docs.asterisk.org/Configuration/Core-Configuration/Asterisk-Main-Configuration-File) configuration file.

**Cambiamos la** **propiedad de todos los archivos y directorios** de Asterisk para que el usuario pueda acceder a esos archivos:

```coffeescript
sudo chown -R asterisk: /var/{lib,log,run,spool}/asterisk /usr/lib/asterisk /etc/asterisk
```

```coffeescript
sudo chmod -R 750 /var/{lib,log,run,spool}/asterisk /usr/lib/asterisk /etc/asterisk
```

<br/>

### [Running Asterisk as a Service](https://docs.asterisk.org/Operation/Running-Asterisk/#running-asterisk-as-a-service)

The most common way to run Asterisk in a production environment is as a service. Asterisk includes both a `make` target for installing Asterisk as a service, as well as a script - `live_asterisk` - that will manage the service and automatically restart Asterisk in case of errors.

#### Iniciando Asterisk

Para **iniciar Asterisk**:

```coffeescript
sudo /etc/init.d/asterisk start
```

<img width="1318" height="130" alt="image" src="https://github.com/user-attachments/assets/8e12dd07-2be8-462f-a2c7-3751371d48c9" />

<br/>
<br/>


### [Running Asterisk from the Command Line](https://docs.asterisk.org/Operation/Running-Asterisk/#running-asterisk-from-the-command-line)

Para **acceder a las interfaz de comandos de Asterisk (CLI)** ejecutamos (*vvvvvv* es para el modo verboso):

```coffeescript
sudo asterisk -rvvvvvvc
```
o

```coffeescript
$ sudo asterisk -r
```

<img width="774" height="209" alt="image" src="https://github.com/user-attachments/assets/61a84330-2b60-42c2-942e-7626223395b0" />

<br/>
<br/>

Ya solo queda **habilitar el servicio de Asterisk para iniciarse en el arranque**:

```coffeescript
sudo systemctl enable asterisk
```

> [!NOTE]
> Además, podemos usar los siguientes comandos para **iniciar, parar, reiniciar, recargar, forzar la recarga y ver el estado**, respectivamente:
> 
> ```coffeescript
> sudo /etc/init.d/asterisk {start|stop|restart|reload|force-reload|status}
> ```

