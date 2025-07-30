Informe de Pruebas - API Clon de AirBnB

Hicimos pruebas a todos los endpoints generados hasta el momento, en caso normales y casos con data invalida.

Se testearon los siguientes endpoints:
- User:
    - User | POST | /api/v1/users/
    - User | GET | /api/v1/users/<id>
    - User | PUT | /api/v1/users/<id>	
- Place:
    - Place | POST | /api/v1/places/
    - Place | GET | /api/v1/places/<id>
    - Place | PUT | /api/v1/places/<id>
- Review
    - Review | POST | /api/v1/reviews/
    - Review | GET | /api/v1/reviews/<id>
    - Review | PUT | /api/v1/reviews/<id>
    - Review | DELETE | /api/v1/reviews/<id>
- Amenity
    - Amenity | POST | /api/v1/amenity/
    - Amenity | GET | /api/v1/amenity/<id>
    - Amenity | PUT | /api/v1/amenity/<id>

Las pruebas las fuimos haciendo a medida que ibamos implementando los endpoints y sus validaciones, 
posteriormente implementamos unittest para automatizar los tests. Adicionalmete para poder realizar las pruebas
tuvimos que implementar uuid para generar datos únicos (como emails) y evitar colisiones.

Resultados generales
Ejecutamos todos los tests automáticos y pasaron sin problemas. Además, confirmamos que los mensajes de error son claros y que la API se comporta correctamente tanto en casos buenos como en los de error.

Al ejecutar:
python3 -m unittest discover tests -v

Obtenemos la siguiente respuesta:
Ran 20 tests in 0.39s
OK
