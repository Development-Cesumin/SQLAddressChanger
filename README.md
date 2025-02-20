# Cambio de direcciones - Desarrollo

Este proyecto es una aplicación en Python diseñada para actualizar las direcciones de entrega y facturación de pedidos en una tienda PrestaShop (versión 1.7.7.3). La aplicación se conecta de forma segura a la base de datos mediante un túnel SSH, consulta una vista personalizada y permite actualizar los registros en la tabla de pedidos. Este script se ha hecho exclusivamente para la base de datos de Galileo y losprestashop donde este creada la vista personalizada.

## Características

- **Conexión segura a la base de datos:** Utiliza `sshtunnel` para establecer un túnel SSH y conectarse a la base de datos sin exponerla directamente.
- **Gestión de credenciales:** Emplea un archivo `.env` para manejar de forma segura las credenciales y otros parámetros sensibles, evitando su inclusión en el repositorio.
- **Interfaz interactiva:** Permite al usuario ingresar el ID del pedido, visualizar las direcciones asociadas y seleccionar la que se aplicará.
- **Actualización en PrestaShop:** Ejecuta consultas SQL para actualizar los campos `id_address_delivery` e `id_address_invoice` en la tabla `ps_orders` de PrestaShop.
- **Distribución como ejecutable:** Posibilidad de compilar la aplicación en un ejecutable (.exe) usando PyInstaller para distribuirla sin revelar el código fuente.

## Requisitos

- Python 3.x
- [sshtunnel](https://pypi.org/project/sshtunnel/)
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Development-Cesumin/SQLAddressChanger.git
   cd SQLAddressChanger
   ```

2. **Crear y activar un entorno virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate      # En Linux/Mac
   venv\Scripts\activate         # En Windows
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar el archivo .env:**

   Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura y completa los valores con tus credenciales:

   ```env
   # Configuración SSH
   SSH_HOST=example.com
   SSH_PORT=22
   SSH_USERNAME=root
   SSH_PASSWORD=your_ssh_password

   # Configuración de la base de datos
   DB_HOST=localhost
   DB_PORT=3306
   DB_USERNAME=db_user
   DB_PASSWORD=your_db_password
   DB_NAME=prestashop_db
   ```

   **Importante:** Asegúrate de que el archivo `.env` esté incluido en el `.gitignore` para evitar exponer información sensible.

## Uso

1. **Ejecutar la aplicación:**

   ```bash
   python main.py
   ```

2. **Flujo de la aplicación:**

   - Se te solicitará ingresar el ID del pedido.
   - La aplicación realizará una consulta a la vista `view_order_address` para mostrar todas las direcciones asociadas al pedido.
   - Se mostrará una lista de direcciones con información relevante (como `AddressID`, `Address`, `FirstName` y `LastName`).
   - Elige el número correspondiente a la dirección que deseas aplicar.
   - Confirma la operación para actualizar el pedido en la base de datos.
   - La aplicación mostrará un resumen con los datos actualizados.

## Compilación a .exe

Si deseas distribuir la aplicación como un ejecutable en Windows, sigue estos pasos utilizando PyInstaller:

1. **Instalar PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Generar el ejecutable:**

   ```bash
   pyinstaller --onefile main.py
   ```

   Esto creará un ejecutable en la carpeta `dist/`.

## Estructura del Proyecto

```
cambio-de-direcciones/
│
├── main.py           # Script principal de la aplicación
├── .env              # Archivo de configuración (no incluido en el repositorio, renombra el .env.example)
├── .gitignore        # Archivo para ignorar archivos sensibles y directorios generados
├── requirements.txt  # Lista de dependencias del proyecto
└── README.md         # Este archivo
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

## Contacto

Para dudas, sugerencias o colaboraciones, puedes contactarme a través de [carlos117g@gmail.com](mailto:carlos117g@gmail.com).