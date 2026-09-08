from app.core.database import get_database


def seed_data():
    db = get_database()

    if db.authors.count_documents({}) > 0:
        print("Datos ya existentes — seed omitido")
        return

    authors = [
        {
            "name": "Miguel de Cervantes",
            "country": "España",
            "birth_year": 1547,
            "death_year": 1616,
            "biography": "Novelista, poeta y dramaturgo español. Considerado una de las figuras más destacadas de la literatura española.",
            "image_url": "/authors/cervantes.webp",
        },
        {
            "name": "William Shakespeare",
            "country": "Inglaterra",
            "birth_year": 1564,
            "death_year": 1616,
            "biography": "Dramaturgo y poeta inglés. Autor de Hamlet, Romeo y Julieta, y muchas otras obras fundamentales de la literatura.",
            "image_url": "/authors/shakespeare.webp",
        },
        {
            "name": "Gabriel García Márquez",
            "country": "Colombia",
            "birth_year": 1927,
            "death_year": 2014,
            "biography": "Escritor y periodista colombiano. Premio Nobel de Literatura 1982. Padre del realismo mágico.",
            "image_url": "/authors/garcia-marquez.webp",
        },
        {
            "name": "Jorge Luis Borges",
            "country": "Argentina",
            "birth_year": 1899,
            "death_year": 1986,
            "biography": "Escritor y ensayista argentino. Conocido por sus cuentos fantásticos y filosóficos.",
            "image_url": "/authors/borges.webp",
        },
        {
            "name": "Jane Austen",
            "country": "Inglaterra",
            "birth_year": 1775,
            "death_year": 1817,
            "biography": "Novelista inglesa conocida por su crítica social y su ironía. Autora de Orgullo y Prejuicio.",
            "image_url": "/authors/austen.webp",
        },
    ]

    result = db.authors.insert_many(authors)
    author_ids = {a["name"]: str(_id) for a, _id in zip(authors, result.inserted_ids, strict=True)}

    books = [
        {
            "title": "Don Quijote de la Mancha",
            "author_id": author_ids["Miguel de Cervantes"],
            "country": "España",
            "publication_year": 1605,
            "genre": "Novela",
            "description": "Obra cumbre de la literatura española que narra las aventuras de un hidalgo que enloquece leyendo libros de caballerías.",
            "cover_url": "/covers/don-quijote.webp",
        },
        {
            "title": "La Celestina",
            "author_id": author_ids["Miguel de Cervantes"],
            "country": "España",
            "publication_year": 1499,
            "genre": "Tragicomedia",
            "description": "Obra de Fernando de Rojas que mezcla elementos medievales y renacentistas.",
            "cover_url": "/covers/celestina.webp",
        },
        {
            "title": "Hamlet",
            "author_id": author_ids["William Shakespeare"],
            "country": "Inglaterra",
            "publication_year": 1603,
            "genre": "Tragedia",
            "description": "La obra más famosa de Shakespeare, que narra la historia del príncipe de Dinamarca.",
            "cover_url": "/covers/hamlet.webp",
        },
        {
            "title": "Romeo y Julieta",
            "author_id": author_ids["William Shakespeare"],
            "country": "Inglaterra",
            "publication_year": 1597,
            "genre": "Tragedia",
            "description": "La historia de dos jóvenes amantes cuyas familias están enfrentadas.",
            "cover_url": "/covers/romeo-julieta.webp",
        },
        {
            "title": "El amor en los tiempos del cólera",
            "author_id": author_ids["Gabriel García Márquez"],
            "country": "Colombia",
            "publication_year": 1985,
            "genre": "Novela",
            "description": "Una historia de amor que abarca más de cincuenta años en el Caribe colombiano.",
            "cover_url": "/covers/amor-colera.webp",
        },
        {
            "title": "Cien años de soledad",
            "author_id": author_ids["Gabriel García Márquez"],
            "country": "Colombia",
            "publication_year": 1967,
            "genre": "Realismo mágico",
            "description": "La historia de la familia Buendía a lo largo de siete generaciones en Macondo.",
            "cover_url": "/covers/cien-anos.webp",
        },
        {
            "title": "Ficciones",
            "author_id": author_ids["Jorge Luis Borges"],
            "country": "Argentina",
            "publication_year": 1944,
            "genre": "Cuento",
            "description": "Colección de cuentos que exploran laberintos, espejos y bibliotecas infinitas.",
            "cover_url": "/covers/ficciones.webp",
        },
        {
            "title": "El Aleph",
            "author_id": author_ids["Jorge Luis Borges"],
            "country": "Argentina",
            "publication_year": 1949,
            "genre": "Cuento",
            "description": "Colección de cuentos que incluye el famoso relato del punto que contiene el universo.",
            "cover_url": "/covers/aleph.webp",
        },
        {
            "title": "Orgullo y Prejuicio",
            "author_id": author_ids["Jane Austen"],
            "country": "Inglaterra",
            "publication_year": 1813,
            "genre": "Novela",
            "description": "La historia de Elizabeth Bennet y el señor Darcy en la Inglaterra del siglo XIX.",
            "cover_url": "/covers/orgullo-prejuicio.webp",
        },
    ]

    db.books.insert_many(books)
    print(f"✓  Seed completado: {len(authors)} autores, {len(books)} libros")
