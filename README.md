# Jupyter Bitcoin and Ethereum + ERC20 demo.

## How run notebook

Setup `pipenv`:

```angular2html
pipenv install --skip-lock
```

`--skip-lock` - because of dependency issue between two1 and neocore.

Run Jupyter:

```angular2html
pipenv shell
python -m ipykernel install --user --name=my-virtualenv-name
jupyter notebook
```

Then click to `Kernel` -> `Change kernel` -> `my-virtualenv-name`
