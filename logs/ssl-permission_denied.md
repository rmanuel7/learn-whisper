> [!CAUTION]
> ```
> Unhandled exception. System.UnauthorizedAccessException: Access to the path '/etc/ssl/certs/reincar.app.pfx' is denied.
> Oct 18 20:43:55 DESKTOP-DI9J8K3 dotnet[142862]:  ---> System.IO.IOException: Permission denied
> ```

### Pasos para aplicar la solución 

Para aplicar las correcciones, necesitará permisos de superusuario (`sudo`). 

1.  **Cambiar el grupo propietario del archivo del certificado**:  
    Esta acción cambia el grupo del archivo `reincar.app.pfx` al grupo `auditorai-data`.
    
    ```
    sudo chgrp auditorai-data /etc/ssl/certs/reincar.app.pfx
    ```
    
2.  **Otorgar permisos de lectura al grupo**:  
    Esta acción agrega permisos de lectura (`g+r`) al grupo `auditorai-data`, permitiendo que todos los miembros de ese grupo lean el archivo.
    
    ```
    sudo chmod g+r /etc/ssl/certs/reincar.app.pfx
    ```
    
3.  **Verificar la configuración de permisos**:  
    Para confirmar que los cambios se aplicaron correctamente, puede usar el comando `ls -l`.
    
    ```
    ls -l /etc/ssl/certs/reincar.app.pfx
    ```
    
    La salida debería mostrar `root auditorai-data` como propietario y grupo, e incluir un permiso de lectura (`r`) para el grupo. Por ejemplo:
    
    ```
    -rw-r----- 1 root auditorai-data 2433 oct 18 21:51 /etc/ssl/certs/reincar.app.pfx
    ```
    
4.  **Reiniciar el servicio**:  
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
