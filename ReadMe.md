# Topic Modeling Trends Demonstration

## DESCRIPTION

This project is a demonstration of creating semantic trends embeddings from Word2Vec models. The project is divided into two main sections: healthcare and New York Times (NYT) articles. The healthcare section is further divided into two subsections: nursing and healthcare. The project is structured in a way that the user can easily add new sections and subsections. The project is designed to be scalable and flexible.

## QuckStart

1. Clone the repository

   ```bash
   git clone https://github.com/angadsinghsandhu/trends-demo.git
   ```

2. Create a virtual environment

   ```bash
   pip install uv
   uv venv
   ```

3. Install the requirements

   ```bash
   uv sync
   ```

4. Run the application

   ```bash
   uv run python manage.py runserver
   ```

5. Access the application locally on your the browser

   ```link
   http://127.0.0.1:8000/
   or
   http://0.0.0.0:8000/
   ```

## INFO

[TODO]

## DJANGO

update the application by making migrations using the following command:

```bash
python manage.py makemigrations
python manage.py migrate
```

## DOCKER commands

Rebuild Docker image using the updated Dockerfile and run the container using the following commands:

```bash
docker build --no-cache -t trends-demo .
# docker-compose up --build
docker run -p 8000:8000 trends-demo
```

run docker shell

```bash
docker exec -it <container_id> /bin/bash
```

## Important Links

- Paper Pre-Print: [ArXiv Link](http://dx.doi.org/10.48550/arXiv.2209.11717)
- MIND Lab Website: [CLICK HERE](https://mindlab.cs.umd.edu/)
- Our LinkedIn Profiles:
  - [LinkedIn: Angad](https://www.linkedin.com/in/angad-sandhu/)
  - [LinkedIn: Vishesh](https://www.linkedin.com/in/vishesh-gupta-975550206/)
  - [LinkedIn: Faizan](https://www.linkedin.com/in/fwajid/)
- Our GitHub Links:
  - [GitHub: Angad](https://github.com/angadsinghsandhu)
  - [GitHub: Vishesh](https://github.com/visheshnarayan)
- My Medium Blogs: [Medium: Angad](https://angadsandhu.medium.com/)
- My Twitter Profiles: [Twitter: Angad](https://x.com/angadsandhuwork)
- Professor Agrawala's Website: [LINK](https://www.cs.umd.edu/people/agrawala)

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