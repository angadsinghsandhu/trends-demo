# Trends Demonstration

## DIRECTORY STRUCTURE

```md
.
├── .vscode/
├── home/
│   ├── helper/
│   │   ├── trends/
│   │   │   ├── healthcare/
│   │   │   │   ├── data/
│   │   │   │   └── models/
│   │   │   ├── nursing/
│   │   │   │   ├── data/
│   │   │   │   └── models/
│   │   │   ├── nyt/
│   │   │   │   ├── data/
│   │   │   │   └── models/
├── migrations/
├── static/
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   ├── sass/
│   │   │   ├── base/
│   │   │   ├── components/
│   │   │   ├── layout/
│   │   │   └── libs/
│   │   ├── webfonts/
│   ├── csv/
│   ├── images/
├── templates/
├── tests/
│   ├── helper/
│   │   ├── trends/
│   │   │   ├── healthcare/
│   │   │   └── nyt/
└── trends/
```

## DESCRIPTION

This project is a demonstration of creating semantic trends embeddings from Word2Vec models. The project is divided into two main sections: healthcare and New York Times (NYT) articles. The healthcare section is further divided into two subsections: nursing and healthcare. The project is structured in a way that the user can easily add new sections and subsections. The project is designed to be scalable and flexible. The project is built using Python, Flask, and SQLite.

## INSTALLATION

1. Clone the repository
2. Create a virtual environment
3. Install the requirements
4. Run the application
5. Access the application on the browser

## USAGE

## DJANGO

Run the django application using the following command:

```bash
python manage.py runserver
```

Access the application on the browser using the following URL:

```bash
http://127.0.0.1:8000/
```

update the application by making migrations using the following command:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Important Links
