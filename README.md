> Written with [StackEdit](https://stackedit.io/).

![Alt Text](https://mindful-unicorn-vro2dw-dev-ed--c.documentforce.com/sfc/dist/version/renditionDownload?rendition=ORIGINAL_Gif&versionId=0685w00000QjZ9c&operationContext=DELIVERY&contentId=05T5w00001Rtpwg&page=0&d=/a/5w0000022qYY/h9tKJ5WTw3jyeKcAYAqVoo.JVXZ7t.DMICXgqscPkdI&oid=00D5w000004ChOL&dpt=null&viewId=)

Flujo del programa
===================

El flujo del programa hace referencia al orden en que se ejecutan las instrucciones, en el caso del programa creado para FarmaSoft se utilizaron sentencias que garantizan el cumplimiento de las necesidades solicitadas por al empresa. 

Las sentencias así como los módulos utilizados hacen que el archivo main.py  sea de flujo **NO SECUENCIAL**, es decir, el programa no se ejecuta de inicio a fin instrucción tras instrucción.

Se comienza con el llamado de los módulos necesarios para el correcto arranque en Python seguido de clases en las cuales se han creado los métodos que son utilizados en la parte final del código donde se utiliza el potencial de **Flask**.

Los datos son enviados a archivos .html escritos en código **HTML, CSS, Bootstrap y Jinja2**. Los archivos .HTML se han escrito de modo secuencial. Se han utilizado ciclo for para la creación de tablas en algunas de las solicitudes de consulta de FarmaSoft

Los .HTML envían mediante flask, información introducida por el usuario en pantalla y es recibido por python para el procesamiento según el código.

Para la entrega final el programa ha sido dotado con 3 nuevas carácterísticas y funcionalidades particulares.

> -Se puede crear nuevas cuentas para un manejo personalizado de la información
> -Se puede realizar cambio de contrasena
> -Se puede realizar la exportación de la información de las consultas en formato .csv

Finalmente todo es desplegado en las plantillas utilizando interfaz gráfica Boorstrap en los exploradores.

```sequence
Python-->Flask: render_templante
Flask->WEB: Bootstrap
Flask-->Python: variables {{ url_for }}
```
Estructura del programa:
-------------

Para la estructura del programa se han utilizado instrucciones:

####De declaración:
 Donde se han asignado las variables necesarias para la correcta ejecución del programa de gestión
####De entrada:
 Solicita al usuario vía pantalla y dada la interface flask-python el análisis de la información en el código
####De salida: 
Despliegue de la información tratada como consulta en el explorador
####Compuestas: 
Al existir interacción entre python y flask, este último sirviendo como subprograma a python para el uso html
####De salto condicional: 
Utilizadas tanto en python como en los archivos .html para el correcto funcionamiento del sistema de gestión

Se han utilizado elementos auxiliares, como contadores, bucles necesarios para el análisis de datos en las consultas El programa se define de **tipo gestión**, caracterizado por el manejo de gran cantidad de datos y pocos cálculos.

Los lenguajes de programación utilizados han sido:
+ Python
+ html5
+ CSS
+ JinJa2

Cómo se usa el programa
-------------
> - Se inicia el programa por termina.
> - Iniciará el servidor http://127.0.0.1:5000/
> - Llevará al usuario a la página principal dando la bienvenida
> - El usuario podrá ingresar al sistema con su nombre y contraseña
> - Se mostrarán en la pantalla de inicio las últimas ventas de la empresa
> - Están habilitados en la cinta de la página web links para 4 consultas

#####Productos por clientes

> - El usuario podrá ingresar el nombre exacto del cliente en mayúsculas y mostrará la información 
> - Si el nombre es erróneo no mostrará ninguna información
> - El usuario puede ingresar en mayúscula 3 letras o más del nombre cliente y se desplegará una lista donde podrá utilizar el nombre para realizar la consulta
> - Al finalizar la consulta el usuario puede realizar la descarga de la información en un archívo .csv
#####Clientes por productos
> - El usuario podrá ingresar el nombre exacto del producto en mayúsculas y mostrará la información
> - Si el nombre es erróneo no mostrará ninguna información
> - El usuario puede ingresar en mayúscula 3 letras o más del nombre del producto y se desplegará una lista donde podrá utilizar el nombre para realizar la consulta
> - Al finalizar la consulta el usuario puede realizar la descarga de la información en un archívo .csv
#####Productos más vendidos
> - El usuario podrá ingresar el número del rancking que quiere crear
> - Se mostrará una lista con los n productos más vendidos
> - Al finalizar la consulta el usuario puede realizar la descarga de la información en un archívo .csv
#####Mejores clientes
> - El usuario podrá ingresar el número del rancking que quiere crear
> - Se mostrará una lista con los n clientes que más compras hicieron dado el precio 
cerrar sesión
> - Al finalizar la consulta el usuario puede realizar la descarga de la información en un archívo .csv
> - Cerrará la sesión iniciada por el usuario

Qué clases se diseñaron y por qué
-------------

	Se crearon 4 clases.

###class Login():
	utilizada para solicitar la información por servidor al usuario
###class References():
	Utilizado para almacenar variables utilizadas para analizar las consultas realizas por el usuario

Ambas son las clases relacionadas directamente con los métodos GET y POST en Flask

###class FileCheck():
Utilizado para el análisis generar de las restricciones solicitadas por el cliente en cuanto al manejo de la información

	Presenta aparte de su método constructor los siguientes métodos:	
	
**lenthRecord:** Revisa si la cantidad de columnas del csv son correctas:
**orderFields:** Indica al programa en qué columna se ha colocado cada uno de los valores según la columna
**productIdValue:** Revisa si el valor de código no es vacio
**quantityValue:** Revisa que ningún valor de cantidad sea un valor no entero
**priceValue:** Revisa que ninguna valor de precio sea un valor no decimal

###class GeneralConsults():
Utilizado para el análisis generar de las consultas solicitadas por el cliente en cuanto al manejo de la información:

	Presenta aparte de su método constructor los siguientes métodos:

**productsPerClient:** Lista todos los productos que compró un cliente
**clientsPerProduct:** Lista todos los clientes que compraron un producto
**n_MostSelledProducts:** Generar una lista de los n productos más vendidos
**n_ClientsExpendedMoreMoney:** Generar una lista de los n mejores clientes dado el precio de sus compras
		









