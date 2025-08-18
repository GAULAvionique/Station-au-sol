# Enable I2C

```bash
sudo raspi-config
```

-   3 - Interface
-   I4 - I2C
-   Enable I2C `yes`

# Enable UART for GPS

```bash
sudo raspi-config
```

-   3 - Interface
-   I5 - Serial port
-   Sélectionner `No` pour désactiver le shell
-   Sélectionner `yes` pour activer le UART
