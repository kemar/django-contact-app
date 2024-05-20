# Django Contact.app

A Django implementation of the [Contact.app](https://github.com/bigskysoftware/contact-app) used in the Chapter 3 of the book [*Hypermedia Systems*](https://hypermedia.systems/a-web-1-0-application/).

This is for people familiar with Django wishing to continue the reading in familiar territory.

The game is to use a hypermedia-oriented library to improve this "web 1.0 application" while retaining the hypermedia-based approach.

## Switch between tags

    $ git switch -d web-1-app
    $ git switch -d chapter-5
    $ git switch -d chapter-6
    $ git switch -d chapter-7
    $ git switch -d chapter-9
    $ git switch -d chapter-12

## Usage with Docker

To run the Django dev server:

    $ docker-compose up

To load the initial data, open a new terminal window:

    $ make django_admin COMMAND="loaddata fixtures/contact.json"

## Pull requests

- [Chapter 5 "Htmx Patterns"](https://github.com/kemar/django-contact-app/pull/1)
- [Chapter 6 "More Htmx Patterns"](https://github.com/kemar/django-contact-app/pull/2)
- [Chapter 7 "A Dynamic Archive UI"](https://github.com/kemar/django-contact-app/pull/3)
- [Chapter 9 "Client Side Scripting"](https://github.com/kemar/django-contact-app/pull/4)
- [Chapter 12 "Building a Contacts App With Hyperview"](https://github.com/kemar/django-contact-app/pull/6)

## Data source

Initial data from [generatedata](https://github.com/benkeen/generatedata).
