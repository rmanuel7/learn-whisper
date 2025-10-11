> [!WARNING]
> ### "guest" user can only connect from localhost​

El usuario `guest` solo tiene permitido el acceso a través de conexiones locales (`localhost`) y no puede conectarse de forma remota para evitar problemas de seguridad, ya que es un usuario con credenciales conocidas por defecto (`guest`/`guest`).

<br/>

## Permitir acceso remoto al usuario guest (solo para desarrollo)

Esta opción es **altamente desaconsejada en entornos de producción** debido a que abre una gran vulnerabilidad de seguridad. Solo úsala si estás en un entorno de desarrollo seguro o para pruebas. 

### Edita el archivo de configuración de RabbitMQ `/etc/rabbitmq/rabbitmq.conf`.

Puedes usar un editor de texto como vim o nano:

```sh
sudo nano /etc/rabbitmq/rabbitmq.conf
```

> [!NOTE]
> El archivo de configuración de RabbitMQ `/etc/rabbitmq/rabbitmq.conf` **no se crea** durante la instalacion.

### Añade la siguiente línea al final del archivo:

```ini
loopback_users.guest = false
```

### Reinicia el servicio de RabbitMQ para que los cambios surtan efecto:

```sh
sudo systemctl restart rabbitmq-server
```
