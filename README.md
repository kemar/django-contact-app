# Django Contact.app

A Django implementation of the [Contact.app](https://github.com/bigskysoftware/contact-app) used in the Chapter 3 of the book [*Hypermedia Systems*](https://hypermedia.systems/a-web-1-0-application/).

This is for people familiar with Django wishing to continue the reading in familiar territory.

The game is to use a hypermedia-oriented library to improve this "web 1.0 application" while retaining the hypermedia-based approach.

## Switch between tags

Go to the "web 1.0 application" state:

    $ git switch -d web-1-app

Go to the "Chapter 5" state:

    $ git switch -d chapter-5

## Usage with Docker

To run the Django dev server:

    $ docker-compose up

To load the initial data, open a new terminal window:

    $ make django_admin COMMAND="loaddata fixtures/contact.json"

## Data source

Initial data from [generatedata](https://github.com/benkeen/generatedata).
