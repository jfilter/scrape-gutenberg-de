# Scrape Gutenberg DE

Scrape all Books from [Projekt Gutenberg-DE](http://gutenberg.spiegel.de/). Usefull, i.e., if you need a large corpus of German text to do some serious language modeling.

## Usage

```bash
git clone https://github.com/jfilter/scrape-gutenberg-de --depth 1
pipenv install
pipenv run scrapy runspider scrape.py -o data.json
```

## License

MIT.
