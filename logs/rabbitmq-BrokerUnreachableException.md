> [!CAUTION]
> ```sql
> EventBusRabbitMQ.DefaultRabbitMQPersisterConnection: Warning: RabbitMQ.Client.Exceptions.BrokerUnreachableException: None of the specified endpoints were reachable
> ---> System.AggregateException: One or more errors occurred. (Connection failed, host 192.168.1.3:5672)
> ---> RabbitMQ.Client.Exceptions.ConnectFailureException: Connection failed, host 192.168.1.3:5672
> ---> System.Net.Sockets.SocketException (10060): Se produjo un error durante el intento de conexión ya que la parte conectada no respondió adecuadamente tras un periodo de tiempo, o bien se produjo un error en la conexión establecida ya que el host conectado no ha podido responder.
> ```

> [!TIP]
> Las causas más comunes de este problema son la **configuración del firewall o problemas de _binding_ de red** en la configuración.

<br/>

### Diagnóstico y solución de errores de conexión con RabbitMQ

#### Resumen

El error `RabbitMQ.Client.Exceptions.BrokerUnreachableException` indica que la aplicación cliente no puede establecer una conexión de red con el servidor de RabbitMQ. El código de error `System.Net.Sockets.SocketException (10060)` especifica que el intento de conexión se agotó (timeout) porque el host de destino no respondió. 

#### Contexto del error

*   **Mensaje de error principal:** `None of the specified endpoints were reachable` (Ninguno de los puntos de conexión especificados fue accesible).
*   **Mensaje de error secundario:** `Connection failed, host 192.168.1.3:5672` (Conexión fallida, host 192.168.1.3:5672).
*   **Excepción detallada:** `System.Net.Sockets.SocketException (10060)` (Se agotó el tiempo de espera).

### Diagnóstico del problema

Las posibles razones por las que la conexión falla son:

1.  **Bloqueo por el Firewall:** El firewall está bloqueando el puerto 5672, impidiendo que la conexión desde el cliente llegue al servidor RabbitMQ.
2.  **Problema de _binding_ de red en Docker:** Si RabbitMQ se ejecuta dentro de un contenedor de Docker, es posible que el puerto no se haya expuesto correctamente o que haya una configuración de red incorrecta en Docker Desktop para Windows (utilizado por WSL).
3.  **Servidor RabbitMQ no en ejecución:** El servidor de RabbitMQ no está activo en el host de destino (`192.168.1.3`).

### Soluciones recomendadas

#### Paso 1: Verificar el estado del servidor RabbitMQ

Antes de realizar cambios en la red, asegúrese de que el servidor RabbitMQ se está ejecutando correctamente.

*   **En Docker:** Ejecute `docker ps` en su terminal para verificar que el contenedor de RabbitMQ está en la lista y en estado _Up_.
*   **En WSL (si está instalado directamente):** Ejecute `sudo systemctl status rabbitmq-server` desde la terminal de WSL.

#### Paso 2: Solucionar problemas de firewall en Windows

Es la causa más probable del error.

1.  **Abrir el Firewall de Windows Defender:** Busque "Firewall de Windows Defender con seguridad avanzada" en el menú de inicio de Windows.
2.  **Crear una nueva regla de entrada:**
    *   Haga clic en **"Reglas de entrada"** y luego en **"Nueva regla..."**.
    *   Seleccione el tipo de regla **"Puerto"**.
    *   Elija **"TCP"** y en **"Puertos locales específicos"**, ingrese `5672`.
    *   Seleccione **"Permitir la conexión"**.
    *   Elija los perfiles de red aplicables (por ejemplo, **"Privado"** o **"Dominio"**; evite **"Público"** en entornos de desarrollo).
    *   Asigne un nombre descriptivo a la regla (ej: `RabbitMQ_5672`).
3.  **Intentar conectar de nuevo:** Una vez creada la regla, la conexión desde WSL debería funcionar.

#### Paso 3: Revisar la configuración de _binding_ de red en Docker

Si RabbitMQ está en un contenedor, es esencial que el puerto se exponga correctamente.

*   **Verificar puertos publicados:** Ejecute el comando `docker ps` y revise la columna `PORTS` para confirmar que el puerto `5672` está mapeado. Debería ver una entrada como `0.0.0.0:5672->5672/tcp`. Si solo muestra `127.0.0.1:5672->5672/tcp`, significa que solo se puede acceder desde el localhost del host de Windows, y WSL necesitaría una configuración específica.
*   **Recrear el contenedor con un mapeo de puertos adecuado:** Si no está mapeado correctamente, detenga el contenedor actual y reinícielo con el mapeo de puertos `-p 5672:5672`.

#### Paso 4: Ajustar la configuración de la red en WSL (para escenarios avanzados)

En algunos casos complejos, la red de WSL puede necesitar ajustes.

1.  **Obtener la IP de WSL:** Desde la terminal de WSL, ejecute `ip addr | grep eth0` para encontrar la dirección IP de la interfaz de red.
2.  **Usar la IP de la puerta de enlace predeterminada:** En ciertas configuraciones, el host de Windows es accesible a través de la IP de la puerta de enlace predeterminada de WSL. Ejecute `route -n` en WSL para obtenerla y utilícela en la cadena de conexión del cliente RabbitMQ.
3.  **Reiniciar la red en Windows:** Si el problema persiste, restablezca la configuración de red de Winsock en Windows con el comando `netsh winsock reset` en el símbolo del sistema (con permisos de administrador).

Recomendaciones finales

*   **Para desarrollo:** Usar Docker Compose para definir tanto el servicio de RabbitMQ como el de su aplicación es la forma más limpia, ya que gestiona la red interna de Docker de manera eficiente.
*   **Para producción:** En un entorno de producción, asegúrese de que las reglas del firewall sean lo más restrictivas posible, permitiendo el acceso solo a los servidores que realmente lo necesitan.
*   **Revisar los logs:** Si los pasos anteriores no resuelven el problema, examine los logs de RabbitMQ (`/var/log/rabbitmq/`) en busca de errores específicos al iniciar el servicio.

