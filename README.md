# Project name
## Chronos Sistema de Notas Inteligente
Stanalone Project
## Version 
0.1
## Description

Webapp escrita en python, Flask con conexion a una base de datos alojada en mariadb esta webapp se puede gestionar lo siguiente:
Usuarios
Alumnos
Maestros - Profesores 
Notas 
Emitir Boletas - Certificados Notas 

## Requerimientos e instalación 

Se recomienda un entorno virtual. 

## configurando el entorno virtual 

```bash
python -m virtualenv venv
```

## activando el entorno virtual en windows (cmd)

```bash
.\venv\Scripts\activate.bat
```

## activando el entorno virtual en windows (powershell)

```bash
.\venv\Scripts\Activate.ps1
```

## activando el entorno virtual en linux

```bash
source ./venv/bin/activate
```

## instalado las dependencias

```bash
pip install -r requirements.txt
```

## iniciando la webapp 

```bash
python src/main.py
```

> [!NOTE]
> Antes de ejecutar la webapp se debe crear una base de datos llamada ams y agregar y restaurar los datos del siguiente backup
> el parametro -p se utiliza para colocar la contraseña en caso de que el usuaro root la tenga configurada de lo contrario e puede omitir

Desde una consola de comandos de windows 
```bash
mariadb -u root -p ams < ams240804_0322.sql
```

Desde una consola de powershell
```bash
Get-Content ams240705.db | mariadb -u root -p ams
```

> [!NOTE]
> La ip por la cual se puede acceder a la web app es la del servidor el puerto 5000 y el puerto 3006 para el servidor de mariadb.


```bash
ejemplo 11.0.0.1:5000
```


### en siguiente url muesta la vista del login 

http://11.0.0.3:5000/main




> [!TIP] 
> verificar que la webapp esta en ejecucion 

### Documentación adicional 

En el siguiente apartado, se puede ver la documentacion mas detallada de la WEBAPP.

[Documentación detallada](DETAILS.md)
