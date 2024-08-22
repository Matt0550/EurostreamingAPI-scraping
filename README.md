[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Discord][discord-shield]][discord-url]
[![Docker Pulls][docker-shield]][docker-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Matt0550/EurostreamingAPI-scraping">
    <img src="logo.png" alt="Logo" height="40" style="filter: invert(1);">
  </a>

  <h3 align="center">Eurostreaming Unofficial REST API & WebApp</h3>

  <p align="center">
    An unofficial REST API for Eurostreaming website, with a WebApp to search for movies and series. Using FastAPI and BeautifulSoup.
    <br />
    <br />
    <a href="https://github.com/Matt0550/EurostreamingAPI-scraping/issues">Report Bug</a>
    ·
    <a href="https://github.com/Matt0550/EurostreamingAPI-scraping/issues">Request Feature</a>
  </p>
</div>

All the data is scraped from the Eurostreaming website. This project is for educational purposes only. I do not condone piracy in any way. Please use this project responsibly. 

Copyright and all rights belong to the respective owners.


# EurostreamingAPI-scraping

An unofficial REST API for Eurostreaming website, with a WebApp to search for movies and series. Using FastAPI and BeautifulSoup.

## Features

- Get all series per page
- Search for series
- Get the list of seasons and episodes of a series and related links to watch them

## API Endpoints

- `/shows/{page}`: Get all series per page. Page is an integer and is required.
- `/search?q={query}&page={page}`: Search for series. Query is a string and is required. Page is an integer and is optional.
- `/show?path={show_path}&alsoEpisodes={alsoEpisodes}`: Get the list of seasons and episodes of a series and related links to watch them. Show_path is a string and is required. AlsoEpisodes is a boolean and is optional, default is true.

> [!TIP]
> The API is self-documented. You can access the Swagger UI at `/docs` and the ReDoc UI at `/redoc`.

## WebApp
> [!WARNING]
> SOON

## TO-DO
- [ ] Add Dockerfile
- [ ] Add Docker Compose
- [ ] Add WebApp
- [ ] Add show categories


## Public instance of the API
Unfortunately, I can't provide a public instance of the API because scraping is not a good practice and it's illegal in some cases. You can host your own instance of the API using the instructions below.

## Environment Variables
> [!WARNING]
> SOON

## Installation - Using Docker Compose (recommended)
> [!WARNING]
> SOON

Run the container with `docker-compose up -d`

## Installation - Using Docker Run
> [!WARNING]
> SOON


## Installation - Self-Host or docker build

Clone the project

```bash
  git clone https://github.com/Matt0550/EurostreamingAPI-scraping
```

Go to the project directory

```bash
  cd EurostreamingAPI-scraping-master
```

OPTIONAL: use docker to build the image

```bash
  docker build -t eurostreamingAPI-scraping .
```
If you don't want to use docker, skip this step.
Else, change the `image` in `docker-compose.yml` with the image name you used.
Run the container with `docker-compose up -d`

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the REST API (after setting the environment variables)

```bash
  cd api
  fastapi run api.py
```

## Help - feedback
You can contact me on:

Discord: https://discord.gg/5WrVyQKWAr

Telegram: https://t.me/Non_Sono_matteo

Mail: <a href="mailto:mail@matteosillitti.it">me@matteosillitti.it</a>

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Support me

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/matt05)

[![buy-me-a-coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Matt0550)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/sillittimatteo)

[contributors-shield]: https://img.shields.io/github/contributors/Matt0550/EurostreamingAPI-scraping.svg?style=for-the-badge
[contributors-url]: https://github.com/Matt0550/EurostreamingAPI-scraping/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Matt0550/EurostreamingAPI-scraping.svg?style=for-the-badge
[forks-url]: https://github.com/Matt0550/EurostreamingAPI-scraping/network/members
[stars-shield]: https://img.shields.io/github/stars/Matt0550/EurostreamingAPI-scraping.svg?style=for-the-badge
[stars-url]: https://github.com/Matt0550/EurostreamingAPI-scraping/stargazers
[issues-shield]: https://img.shields.io/github/issues/Matt0550/EurostreamingAPI-scraping.svg?style=for-the-badge
[issues-url]: https://github.com/Matt0550/EurostreamingAPI-scraping/issues
[license-shield]: https://img.shields.io/github/license/Matt0550/EurostreamingAPI-scraping.svg?style=for-the-badge
[license-url]: https://github.com/Matt0550/EurostreamingAPI-scraping/blob/master/LICENSE
[discord-shield]: https://img.shields.io/discord/828990499507404820?style=for-the-badge
[discord-url]: https://discord.gg/5WrVyQKWAr
[docker-shield]: https://img.shields.io/docker/pulls/matt0550/panini-progno?style=for-the-badge
[docker-url]: https://hub.docker.com/r/matt0550/panini-progno
