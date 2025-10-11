> [!WARNING]
> All stable feature flags must be enabled after completing an upgrade

Ejecuta el siguiente comando para habilitar todas las banderas de características estables:

```sh
sudo rabbitmqctl enable_feature_flag all
```

> [!NOTE]
> Ejecutar `sudo rabbitmqctl enable_feature_flag all` no causará ningún problema ni efecto negativo.
