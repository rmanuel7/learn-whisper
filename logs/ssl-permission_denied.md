> [!CAUTION]
> ```
> Unhandled exception. System.UnauthorizedAccessException: Access to the path '/etc/ssl/certs/reincar.app.pfx' is denied.
> Oct 18 20:43:55 DESKTOP-DI9J8K3 dotnet[142862]:  ---> System.IO.IOException: Permission denied
> ```

## Pasos para aplicar la solución 

> [!NOTE]
> Para aplicar las correcciones, necesitará permisos de superusuario (`sudo`). 

> [!TIP]
> **`Crear un grupo dedicado para el certificado y luego agregar a los usuarios y servicios que lo necesiten`** a ese grupo es una alternativa limpia y segura, especialmente en entornos más sencillos. 

<br/>

Esta estrategia se basa en el principio de mínimo privilegio: el acceso al certificado se restringe únicamente a aquellos que lo necesitan, sin afectar los permisos del sistema de archivos de manera más amplia. 

### Pasos para crear un grupo para el certificado 

1.  **Crear el nuevo grupo**:  
    Use el comando `groupadd` para crear el grupo. Elija un nombre descriptivo, como `cert-reincar` o `ssl-apps`.
    
    ```
    sudo groupadd cert-reincar
    ```
    
2.  **Agregar los usuarios al nuevo grupo**:  
    Use el comando `usermod -aG` para agregar cada usuario o servicio que necesita el certificado al nuevo grupo. Reemplace `<nombre_de_usuario>` con el nombre del usuario real (por ejemplo, `auditoraidatamanager`). La opción `-aG` añade el usuario a un grupo secundario sin eliminarlo de sus otros grupos.
    
    ```
    sudo usermod -aG cert-reincar auditoraidatamanager
    # Repita para otros usuarios o servicios...
    sudo usermod -aG cert-reincar otro_usuario
    ```
    
3.  **Cambiar el grupo propietario del certificado**:  
    Ahora, cambie el grupo propietario del archivo del certificado al nuevo grupo que acaba de crear.
    
    ```
    sudo chgrp cert-reincar /etc/ssl/certs/reincar.app.pfx
    ```
    
4.  **Otorgar permisos de lectura al grupo**:  
    Esta acción agrega permisos de lectura (`g+r`) al grupo `cert-reincar`, permitiendo que todos los miembros de ese grupo lean el archivo.
    
    ```
    sudo chmod g+r /etc/ssl/certs/reincar.app.pfx
    ```
    
5.  **Verificar la configuración de permisos**:  
    Para confirmar que los cambios se aplicaron correctamente, puede usar el comando `ls -l`.
    
    ```
    ls -l /etc/ssl/certs/reincar.app.pfx
    ```
    
    La salida debería mostrar `root cert-reincar` como propietario y grupo, e incluir un permiso de lectura (`r`) para el grupo. Por ejemplo:
    
    ```
    -rw-r----- 1 root cert-reincar 2433 oct 18 21:51 /etc/ssl/certs/reincar.app.pfx
    ```
    
6.  **Reiniciar el servicio**:  
    Después de cambiar los permisos, reinicie el servicio que utiliza el certificado para que pueda cargar el archivo con los nuevos permisos.
    
    ```
    sudo systemctl restart <nombre_del_servicio>
    ```


> [!NOTE]
> Al cambiar el grupo propietario del certificado a `auditorai-data` y luego otorgar permisos de lectura a ese grupo, le permite al usuario de servicio `auditoraidatamanager` acceder al archivo sin comprometer la seguridad del directorio `/etc/ssl/certs/` ni de otros archivos SSL.

- - -

### ¿Por qué esta solución es mejor? 

*   **Seguridad**: A diferencia de dar permisos de lectura a "todos" los usuarios (`chmod o+r`), esta solución restringe el acceso al certificado únicamente a los miembros del grupo `auditorai-data`. Esto previene el acceso no autorizado al certificado por parte de otros usuarios o servicios en el sistema.
*   **Principio del privilegio mínimo**: Otorga solo los permisos necesarios (lectura) al grupo específico de la aplicación, en lugar de conceder permisos excesivos. 

- - -

### ¿Qué pasa con los certificados que también incluyen claves privadas? 

Si su archivo PFX contiene también la clave privada, la estrategia sigue siendo correcta. Las claves privadas suelen estar en un directorio diferente (`/etc/ssl/private/`) con permisos aún más restringidos (solo para el propietario o un grupo específico y restringido como `ssl-cert`). Para un certificado de tipo PFX, que contiene tanto el certificado como la clave, es crucial que el acceso se limite al grupo de servicio específico, como se hizo aquí. 
