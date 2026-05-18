import time, os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:secret123@localhost:5432/elearning")

# Wait for DB
for _ in range(20):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        break
    except:
        time.sleep(2)

from main import Base, Course, Lesson, Quiz, SessionLocal

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Only seed if empty
if db.query(Course).count() > 0:
    print("Already seeded, skipping.")
    db.close()
    exit()

print("Seeding database...")

courses_data = [
    {
        "title": "Docker & Docker Compose",
        "description": "Maîtrisez la conteneurisation avec Docker. Apprenez à créer des images, gérer des volumes, des réseaux et orchestrer des services avec Docker Compose.",
        "instructor": "Pr. Ahmed Khalil",
        "duration": "8h",
        "level": "Intermédiaire",
        "emoji": "🐳",
        "lessons": [
            ("Introduction à Docker", "Docker est une plateforme de conteneurisation qui permet d'emballer une application et toutes ses dépendances dans un conteneur isolé.\n\n**Pourquoi Docker ?**\n- Portabilité : fonctionne partout (dev, staging, prod)\n- Isolation : chaque app dans son propre environnement\n- Légèreté : les conteneurs partagent le kernel Linux\n\n**Commandes de base :**\n```\ndocker pull nginx          # télécharger une image\ndocker run -p 80:80 nginx  # lancer un conteneur\ndocker ps                  # voir les conteneurs actifs\ndocker stop <id>           # arrêter un conteneur\n```"),
            ("Images & Dockerfile", "Un Dockerfile est un fichier texte qui contient les instructions pour construire une image Docker.\n\n**Structure d'un Dockerfile :**\n```dockerfile\nFROM python:3.12-slim      # image de base\nWORKDIR /app               # dossier de travail\nCOPY requirements.txt .    # copier les fichiers\nRUN pip install -r requirements.txt  # exécuter une commande\nCOPY . .                   # copier le code\nEXPOSE 8000               # port exposé\nCMD [\"uvicorn\", \"main:app\"] # commande de démarrage\n```\n\n**Build & run :**\n```\ndocker build -t mon-app .  # construire l'image\ndocker run mon-app         # lancer\n```"),
            ("Volumes & Persistance", "Les volumes Docker permettent de persister les données au-delà du cycle de vie d'un conteneur.\n\n**Types de stockage :**\n- **Volumes nommés** : gérés par Docker, recommandés pour la prod\n- **Bind mounts** : lier un dossier de l'hôte au conteneur\n- **tmpfs** : stockage en mémoire uniquement\n\n**Exemples :**\n```\n# Volume nommé\ndocker run -v mon_volume:/data postgres\n\n# Bind mount\ndocker run -v $(pwd):/app mon-app\n```\n\nDans docker-compose.yml :\n```yaml\nvolumes:\n  - pg_data:/var/lib/postgresql/data\n```"),
            ("Docker Compose", "Docker Compose permet de définir et lancer des applications multi-conteneurs avec un seul fichier YAML.\n\n**docker-compose.yml minimal :**\n```yaml\nversion: '3.9'\nservices:\n  web:\n    build: .\n    ports:\n      - '3000:3000'\n  db:\n    image: postgres:16\n    environment:\n      POSTGRES_PASSWORD: secret\n    volumes:\n      - db_data:/var/lib/postgresql/data\nvolumes:\n  db_data:\n```\n\n**Commandes essentielles :**\n```\ndocker compose up -d     # lancer en arrière-plan\ndocker compose down      # arrêter\ndocker compose logs -f   # voir les logs\ndocker compose ps        # état des services\n```"),
        ],
        "quizzes": [
            ("Quel fichier définit comment construire une image Docker ?", "docker-compose.yml", "Dockerfile", ".env", "Makefile", "b"),
            ("Quelle commande lance tous les services définis dans docker-compose.yml ?", "docker run all", "docker start compose", "docker compose up", "docker build .", "c"),
            ("Quel type de stockage Docker recommande-t-on pour la production ?", "Bind mounts", "tmpfs", "Volumes nommés", "NFS direct", "c"),
        ]
    },
    {
        "title": "Python pour le Web",
        "description": "Construisez des APIs REST modernes avec FastAPI. Bases de Python, Pydantic, SQLAlchemy et déploiement avec Uvicorn.",
        "instructor": "Pr. Sara Bouali",
        "duration": "12h",
        "level": "Débutant",
        "emoji": "🐍",
        "lessons": [
            ("Bases de Python", "Python est un langage interprété, dynamiquement typé et très lisible.\n\n**Types de base :**\n```python\nnom = 'Amira'          # str\nage = 22               # int\nnote = 18.5            # float\nactif = True           # bool\ncours = ['Math', 'Info']  # list\ninfos = {'nom': 'Amira', 'age': 22}  # dict\n```\n\n**Contrôle de flux :**\n```python\nif age >= 18:\n    print('Majeur')\nelse:\n    print('Mineur')\n\nfor cours in liste:\n    print(cours)\n\n# Compréhension de liste\ncours_courts = [c for c in liste if len(c) < 10]\n```"),
            ("FastAPI — Créer une API", "FastAPI est le framework Python le plus rapide pour créer des APIs REST.\n\n**Installation :**\n```\npip install fastapi uvicorn\n```\n\n**API minimale :**\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef hello():\n    return {'message': 'Hello World'}\n\n@app.get('/users/{user_id}')\ndef get_user(user_id: int):\n    return {'id': user_id, 'nom': 'Amira'}\n\n@app.post('/users')\ndef create_user(data: dict):\n    return {'created': True, 'data': data}\n```\n\n**Lancer :**\n```\nuvicorn main:app --reload\n```\nDocumentation auto disponible sur http://localhost:8000/docs"),
            ("SQLAlchemy & Base de données", "SQLAlchemy est l'ORM (Object Relational Mapper) le plus utilisé en Python.\n\n**Définir un modèle :**\n```python\nfrom sqlalchemy.orm import declarative_base\nfrom sqlalchemy import Column, Integer, String\n\nBase = declarative_base()\n\nclass User(Base):\n    __tablename__ = 'users'\n    id    = Column(Integer, primary_key=True)\n    name  = Column(String(100))\n    email = Column(String(200), unique=True)\n```\n\n**Opérations CRUD :**\n```python\n# Créer\nuser = User(name='Amira', email='amira@example.com')\ndb.add(user)\ndb.commit()\n\n# Lire\nusers = db.query(User).all()\nuser = db.query(User).filter(User.id == 1).first()\n\n# Modifier\nuser.name = 'Sara'\ndb.commit()\n\n# Supprimer\ndb.delete(user)\ndb.commit()\n```"),
        ],
        "quizzes": [
            ("Quel décorateur FastAPI définit une route GET ?", "@app.route('/path')", "@app.get('/path')", "@get('/path')", "@route.get('/path')", "b"),
            ("Comment accéder à tous les enregistrements d'un modèle SQLAlchemy ?", "Model.find_all()", "db.query(Model).all()", "Model.select(*)", "db.get(Model)", "b"),
            ("Quel type Python représente un nombre à virgule flottante ?", "int", "str", "float", "decimal", "c"),
        ]
    },
    {
        "title": "React & Interfaces Modernes",
        "description": "Créez des interfaces utilisateur dynamiques avec React 18. Hooks, composants, state management et intégration d'APIs REST.",
        "instructor": "Pr. Lamine Trabelsi",
        "duration": "15h",
        "level": "Intermédiaire",
        "emoji": "⚛️",
        "lessons": [
            ("Composants & JSX", "React est une bibliothèque JavaScript pour construire des interfaces utilisateur à partir de composants.\n\n**Composant fonctionnel :**\n```jsx\nfunction Bonjour({ nom, age }) {\n  return (\n    <div>\n      <h1>Bonjour, {nom} !</h1>\n      <p>Vous avez {age} ans.</p>\n    </div>\n  )\n}\n\n// Utilisation\n<Bonjour nom=\"Amira\" age={22} />\n```\n\n**Règles JSX :**\n- Toujours fermer les balises : `<img />` pas `<img>`\n- Un seul élément racine par return\n- Les classes CSS s'écrivent `className` pas `class`\n- Les expressions JavaScript entre `{}`"),
            ("useState & useEffect", "Les hooks permettent d'ajouter de l'état et des effets secondaires dans les composants fonctionnels.\n\n**useState :**\n```jsx\nimport { useState } from 'react'\n\nfunction Compteur() {\n  const [count, setCount] = useState(0)\n\n  return (\n    <div>\n      <p>Compte : {count}</p>\n      <button onClick={() => setCount(count + 1)}>+1</button>\n      <button onClick={() => setCount(0)}>Reset</button>\n    </div>\n  )\n}\n```\n\n**useEffect :**\n```jsx\nimport { useState, useEffect } from 'react'\n\nfunction MesCours() {\n  const [cours, setCours] = useState([])\n\n  useEffect(() => {\n    fetch('/api/courses')\n      .then(r => r.json())\n      .then(data => setCours(data))\n  }, [])  // [] = exécuté une seule fois au montage\n\n  return <ul>{cours.map(c => <li key={c.id}>{c.title}</li>)}</ul>\n}\n```"),
            ("Fetch API & Intégration Backend", "Connecter React à une API REST avec fetch ou axios.\n\n**GET — Charger des données :**\n```jsx\nconst [data, setData] = useState(null)\nconst [loading, setLoading] = useState(true)\n\nuseEffect(() => {\n  fetch('http://localhost:8000/courses')\n    .then(res => res.json())\n    .then(data => {\n      setData(data)\n      setLoading(false)\n    })\n}, [])\n\nif (loading) return <p>Chargement...</p>\n```\n\n**POST — Envoyer des données :**\n```jsx\nasync function sauvegarder(progression) {\n  const res = await fetch('http://localhost:8000/progress', {\n    method: 'POST',\n    headers: { 'Content-Type': 'application/json' },\n    body: JSON.stringify(progression)\n  })\n  const result = await res.json()\n  console.log(result)\n}\n```"),
        ],
        "quizzes": [
            ("Quel hook React gère l'état local d'un composant ?", "useRef", "useContext", "useState", "useReducer", "c"),
            ("Dans JSX, comment écrit-on une classe CSS ?", "class='btn'", "className='btn'", "cssClass='btn'", "style='btn'", "b"),
            ("Quel tableau passé à useEffect déclenche l'effet une seule fois au montage ?", "[true]", "null", "undefined", "[]", "d"),
        ]
    },
]

for cd in courses_data:
    course = Course(
        title=cd["title"], description=cd["description"],
        instructor=cd["instructor"], duration=cd["duration"],
        level=cd["level"], emoji=cd["emoji"]
    )
    db.add(course)
    db.flush()

    for i, (title, content) in enumerate(cd["lessons"]):
        db.add(Lesson(course_id=course.id, title=title, content=content, order=i))

    for q, a, b, c, d, ans in cd["quizzes"]:
        db.add(Quiz(course_id=course.id, question=q,
                    option_a=a, option_b=b, option_c=c, option_d=d, answer=ans))

db.commit()
db.close()
print("Done! 3 courses, lessons and quizzes seeded.")