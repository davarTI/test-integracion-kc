# Test de integración

Para poder testear correctamente la integración entre los diferentes componentes, usaremos [docker-compose](https://docs.docker.com/compose/) que nos permite desplegar todos los componentes en un único despliegue, y [behave](https://behave.readthedocs.io/en/latest/index.html) para los tests de comportamiento.

## Docker compose

Para poder lanzar docker-compose tenemos que especificar las versiones de nuestros componentes (backend y frontend) mediante variables de entorno:

 * **BACKEND_VERSION**: tag del contenedor de nuestro servicio de backend. Use *latest* si quiere usar la última imagen.
 * **FRONTEND_VERSION**: tag del contenendor de nuestro servicio de frontend. Use *lates* si quiere usar la última imagen.

Además, vamos a lanzar un contenedor con base de datos mysql con tablas creadas y filas con valores para los tests.

Por último vamos a levantar un contenedor de *selenium-standalone* con un chrome para poder lanzar los tests de integración en un navegador real.

## Ejecutar los tests

Los tests de comportamiento están escritos en lenguaje natural con _behave_ en Python (ver las diferentes *features* dentro del directorio _features_).

Crearemos un contenedor con los tests y la llamada a behave con los parámetros necesarios. Además, le daremos un periodo de gracia inicial para que todos los servicios
estén disponibles (se podría haber usado un wait-for-it.sh or un docker-compose-wait, pero por simplicidad usaremos un sleep).

## Ejecución de los tests

Lanzaremos los tests de la siguiente manera:

``` bash
docker-compose up --build --abort-on-container-exit
```

veremos una salida de logs en la consola parecida a

``` bash
...
...
...
Feature: shopping ACME stuff # features/shopping.feature:1

  Background: go to main site  # features/shopping.feature:3

  Scenario: count number of items  # features/shopping.feature:6
    Given We are in the main site  # features/steps/shopping.py:6 0.382s
    Then 3 items must be displayed # features/steps/shopping.py:11 0.052s

  Scenario Outline: list current items -- @1.1 Items  # features/shopping.feature:14
    Given We are in the main site                     # features/steps/shopping.py:6 0.093s
    Then "cohete" item must be displayed              # features/steps/shopping.py:17 0.058s

  Scenario Outline: list current items -- @1.2 Items  # features/shopping.feature:15
    Given We are in the main site                     # features/steps/shopping.py:6 0.057s
    Then "dinamita" item must be displayed            # features/steps/shopping.py:17 0.095s

  Scenario Outline: list current items -- @1.3 Items  # features/shopping.feature:16
    Given We are in the main site                     # features/steps/shopping.py:6 0.059s
    Then "yunque" item must be displayed              # features/steps/shopping.py:17 0.126s

  Scenario: shop item                                          # features/shopping.feature:18
    Given We are in the main site                              # features/steps/shopping.py:6 0.077s
    Then We want to buy a "cohete" with "coyote@acme.es" email # features/steps/shopping.py:23 2.952s

1 feature passed, 0 failed, 0 skipped
5 scenarios passed, 0 failed, 0 skipped
10 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m3.952s
```

Behave nos generará el fichero _reports/TESTS-shopping.xml_ con los resultados de los tests en formato *junit* para poder ser parseado en Jenkins/GitlabCI.

## Finalizar la ejecución

Para no dejar contenedores ejecutándose, pararemos los componentes y borraremos las imágenes generadas para evitar conflictos futuros con los siguientes comandos:

`docker-compose rm -f`
