# dea

An attempt at archiving Japanese doujin-related event info. Current main focus is for any event where music was sold at.

## Repository structure

This repository was made with a Vue.js as its core. It contains two main components:

- The [databases_management](./databases_management/) folder contains the "raw" databases and useful related utilites
- The rest makes the website, hosted at [kahpage.github.io/dea/](https://kahpage.github.io/dea/).

## Contribute

Help of any kind would be greatly appreciated, be it on interface (I am a bad web dev) or on archived content. Please refer to the [website](https://kahpage.github.io/dea/) for additionnal information.

## Updating the database

Please refer to [databases_management/README.md](./databases_management/README.md) for more details.

## Build and deploy website

The website requires vue.js v3.5.13 or higher, but no exotic packages otherwise.

To build it, simply use `pnpm run build` (if using pnpm for example).

To deploy the website locally, use `pnpm run preview`.

To deploy the website on GitHub pages, use `pnpm run deploy`. Be sure to have a working ssh setup to connect to GitHub, and enabled `gh-pages` as branch to use for GitHub pages. 