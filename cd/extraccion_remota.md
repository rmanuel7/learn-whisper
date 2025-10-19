# Extracción remota (Pull-based deployment)

Este método, donde el servidor se encarga de clonar/extraer los cambios y construir el código, es extremadamente común y a menudo más simple de gestionar permisos y rutas, ya que todo ocurre bajo el contexto del usuario SSH remoto.

> [!NOTE]
> *   El servidor de producción debe tener el **SDK de .NET instalado** (no solo el *runtime*)
> *   Consume recursos de CPU y memoria en cada despliegue para compilar el código.

> [!TIP]
> #### Workflow Actualizado: Manejo de Permisos SCP
> *   El usuario SSH debe pertenecer al grupo del servicio
> *   Permite al propietario y al grupo escribir y ejecutar
>     
>     ```sh
>     sudo chmod -R 775 /var/www/auditorai/storage
>     ```


<br/>

## Workflow de Despliegue

Usaremos la acción `appleboy/ssh-action` para descargar la versión de código necesaria directamente en un repositorio local del servidor (`/home/SSH_USERNAME/.deploy/...`) con los comandos `git fetch` y `git checkout`.

```yml
name: Despliegue CD - Storing API (Ubuntu + Apache)

on:
  push:
    tags:
      - 'storing-v*'
  workflow_dispatch: 

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest

    env:
      PUBLISH_TARGET: /var/www/auditorai/storage
      REPO_PATH: .deploy/reincar-auditorai
      SERVICE_NAME: auditorai-storingapi

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
            echo "1. Accediendo al directorio del repositorio..."
            cd ${{ env.REPO_PATH }}

            echo "2. Extrayendo código para el tag: ${{ github.ref_name }}"
            git fetch --tags
            git checkout ${{ github.ref_name }}

            echo "3. Restaurando dependencias y publicando..."
            dotnet restore src/Services/Storing/Storing.API/

            echo "4. Eliminando contenido antiguo de ${{ env.PUBLISH_TARGET }}..."
            find ${{ env.PUBLISH_TARGET }} -mindepth 1 -delete

            echo "5. Publicamos directamente al destino..."
            dotnet publish src/Services/Storing/Storing.API/ -c Release -o ${{ env.PUBLISH_TARGET }}

            echo "6. Reiniciando servicio: ${{ env.SERVICE_NAME }}"
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
