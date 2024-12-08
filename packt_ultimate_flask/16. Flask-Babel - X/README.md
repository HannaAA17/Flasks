# Flask-Babel

## Create template for translations
```bash
pybabel extract -F babel.cfg -o messages.pot
```

## Generate a translation for a language
```bash
pybabel init -i messages.pot -d translations -l es
```
* <-i> for template
* <-d> for directory
* <-l> for language

## Compiling
```bash
pybabel compile -d translations

```


## Application for translating the .pot files
**Poedit**