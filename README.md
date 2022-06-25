# PROGRAMA DE CONSOLIDACIÓN DATOS CAMPAÑA SMS
## Realizado para Empresa Eléctrica Regional Centro sur C.A.

## [**IR A LA APP**](https://consolidado-sms.herokuapp.com/)

Se han implementado técnicas de:

- Procesos ETL
- Expresiones regulares
- Análisis de datos en Python, Servicios web Flask

## Características de la aplicación

- Toma datos de 2 fuentes hasta con cuatro formatos distintos
- Valida números de teléfono, quita caracteres especiales
- Reduce el mensaje para alcanzar el objetivo de 150 caracteres de longitud
- Calcula duración de la suspensión del servicio a partir de cierta parte del mensaje
- Genera como resultado un archivo descargable con formato preestablecido

## Ejecución

Instale las dependencias e inicie el servidor.
Python 3.9 o superior es necesario
```sh
git clone https://github.com/joseleonec/consolidados_sms_centrosur.git
```
```sh
cd consolidados_sms_centrosur
```
```sh
pip install -r requirements.txt
```
```sh
gunicorn app:app 
```

Verifique la implementación navegando a la dirección de su servidor en su navegador preferido.

```sh
127.0.0.1:5000
```
## Licencia

MIT
