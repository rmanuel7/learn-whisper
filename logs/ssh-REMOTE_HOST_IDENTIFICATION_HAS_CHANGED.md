> [!WARNING]
> ## REMOTE HOST IDENTIFICATION HAS CHANGED

Es una medida de seguridad de SSH. Lo que sucedió fue lo siguiente:

1.  En tu primer intento de conexión a la IP pública (`86.3.3.7`), el router interceptó la conexión y te presentó su propia "huella digital" (host key).
2.  **Tu cliente SSH** en Windows guardó esa huella digital en el archivo `known_hosts` para futuras referencias.
3.  Ahora que el router está configurado correctamente, la conexión llega a tu servidor Ubuntu, que tiene una huella digital diferente.
4.  Tu cliente SSH detecta esta discrepancia (la huella guardada no coincide con la nueva) y, por seguridad, detiene la conexión para evitar un posible ataque "Man-in-the-middle".

> [!TIP]
> ### Eliminar la clave antigua
> Debes eliminar la entrada incorrecta del archivo `known_hosts` en tu máquina Windows.
>
> ```powershell
> # Tu cliente SSH powershell
> ssh-keygen -R 86.3.3.7
> ```
