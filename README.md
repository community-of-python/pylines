# PYthon guideLines

<img src="./logo.svg?v2" width="250" />

These are comprehensive guidelines for Python backend/full-stack development, consisting of the following:

1. [Code style](./code-style.md)
1. [Architecture guide](https://habr.com/ru/companies/raiffeisenbank/articles/885792/)
1. [SOLID guide (work in progress)](./solid.md)
1. [REST guide](./rest.md)
1. [Tests guide](./tests.md)
1. [Our libraries, frameworks, etc](./our-stack.md)
1. [Frontend guide](./frontend.md)
1. [Frontend generation guide](./frontend-generation.md)
1. Local development guide
1. [CI/CD pipeline](https://github.com/insani7y/moscow-python-conf-2024)

## Agent skill

To install the `pylines` skill, based on this repo, just run:

```
npx skills add https://github.com/community-of-python/pylines -g
```

`-g` installs globally; drop it to install into the current project. The guides themselves are not
bundled — the skill fetches them from this repo and caches them locally, so it stays current.

## Why this project?

Because there are a lot of guidelines, but not a single one of them is comprehensive enough for most of the use-cases in modern backend development. Here we collect best of our guides to help maintain big codebases in good shape. Without hard and tricky words and rules.
