# Transferencia remota (Push-based deployment)

El *workflow* **solo publica la versión etiquetada**, y eliminas toda la complejidad de `git` y `dotnet` en tu servidor Ubuntu.

La forma más limpia de mantener la estrategia de TAG (`storing-v*`):

*   Construir y Publicar en GitHub Actions (donde es rápido y limpio).

*   Usar SSH para la transferencia y el comando final de reinicio.

<br/>

> [!TIP]
> #### Workflow de GitHub Actions Actualizado (storing-deploy.yml)
> **`.NET Runtime instalado en el servidor`**. Esto reduce el tamaño de los archivos que se copian.

> [!TIP]
> #### Workflow Actualizado: Manejo de Permisos SCP
> *   El usuario SSH debe pertenecer al grupo del servicio
> *   Permite al propietario y al grupo escribir y ejecutar
>     
>     ```sh
>     sudo chmod -R 775 /var/www/auditorai/storage
>     ```

<br/>

> [!CAUTION]
> ```sh
> source: "${{ env.DOTNET_ROOT }}/publish/*"
> # output
> tar: empty archive
> ```

> [!CAUTION]
> ```sh
> error: tar: publish: Cannot mkdir: Permission denied
> ```
> #### Análisis del Error Real
> *   Comprime los contenidos de `./publish/` en un archivo `.tar.gz`.
> *   Transfiere ese archivo al servidor remoto.
> *   En el servidor remoto, ejecuta `tar -xzf` para descomprimir el archivo en el directorio de destino (`/var/www/auditorai/storage`).
> *   El usuario de despliegue tiene permisos sobre `/var/www/auditorai/storage`, pero el proceso de `tar` no debería intentar crear una subcarpeta llamada `publish` dentro.
> #### Solucion
> Usar `strip_components: 1`, el proceso de descompresión eliminará el primer directorio (`publish`) y colocará los archivos directamente en el directorio *target* (`/var/www/auditorai/storage`).



<br/>

## Workflow de Despliegue

Usaremos la acción `appleboy/scp-action` para la transferencia de archivos

```yml
name: Despliegue CD - Storing API (Pull Simplificado)

on:
  push:
    tags:
      - 'storing-v*' # Activado por Tags

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    
    env:
      PUBLISH_TARGET: /var/www/auditorai/storage
      SERVICE_NAME: auditorai-storingapi
      LOCAL_PROJECT_DIR: src/Services/Storing/Storing.API

    steps:
      - name: Checkout del Código Fuente (Versión del Tag)
        # Esto descarga el código del tag que disparó el workflow
        uses: actions/checkout@v4

      - name: Configurar Entorno .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x' 

      # --- 1. Construcción y Publicación de la API ---
      - name: Publicar API
        # Publicamos a una carpeta local sencilla (ejemplo: ./publish_output)
        run: |
          dotnet restore ${{ env.LOCAL_PROJECT_DIR }}/
          dotnet publish ${{ env.LOCAL_PROJECT_DIR }}/ -c Release -o ./publish_output /p:UseAppHost=false

      # --- 2. Despliegue a Servidor Ubuntu (Usando SCP para la copia) ---
      - name: Limpiar Directorio Remoto
        # 🚨 Paso SSH CRÍTICO: Borrar el contenido existente antes de copiar
        uses: appleboy/ssh-action@v1.0.1
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: 22
          script: |
            ## Crear y asegurar que el usuario de despliegue puede escribir (grupo 775)
            # sudo mkdir -p ${{ env.PUBLISH_TARGET }}

            echo "Eliminando contenido antiguo de ${{ env.PUBLISH_TARGET }}..."
            find ${{ env.PUBLISH_TARGET }} -mindepth 1 -delete

            # sudo chown -R auditoraidatamanager:auditorai-data ${{ env.PUBLISH_TARGET }}
            # sudo chmod -R 775 ${{ env.PUBLISH_TARGET }}
            
      - name: Copiar Archivos al Servidor vía SCP
        # SCP transfiere los archivos construidos sin la complejidad del git pull remoto
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: 22
          source: "./publish_output/*"
          target: "${{ env.PUBLISH_TARGET }}"
          strip_components: 1

      - name: Reiniciar el Servicio Kestrel (Systemd) vía SSH
        # SSH reiniciar el servicio en Systemd
        uses: appleboy/ssh-action@v1.0.1
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: 22
          # Comando de reinicio limpio
          script: |
            echo "Reiniciando el servicio: ${{ env.SERVICE_NAME }}..."
            sudo systemctl restart ${{ env.SERVICE_NAME }}.service
            echo "Despliegue completado."
```

> [!IMPORTANT]
> #### Pasos de Implementación en el Servidor:
> *   Crea y guarda el archivo: `sudo vim /etc/systemd/system/auditorai-storingapi.service`
> *   Recarga la configuración de Systemd: `sudo systemctl daemon-reload`
> *   Habilita el servicio para que se inicie al arrancar: `sudo systemctl enable auditorai-storingapi.service`
> #### Permisos de Systemctl (Para el Reinicio)
> Configura el usuario SSH (`SSH_USERNAME`) para que pueda ejecutar el reinicio del servicio sin necesidad de contraseña.
> *   Crea un archivo específico para el usuario SSH (`SSH_USERNAME`) en el directorio `/etc/sudoers.d/`
> *   Añade esta línea, reemplazando `SSH_USERNAME` por tu usuario de despliegue:
>     ```ini
>     SSH_USERNAME ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart auditorai-storingapi.service
>     ```


