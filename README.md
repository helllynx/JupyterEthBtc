# Jupyter Bitcoin and Ethereum + ERC20 demo.

## How run notebook

Setup `pipenv`:
```angular2html
pipenv install
```

if you have some issues wih dependences, use:

```angular2html
pipenv install --skip-lock
```

Run Jupyter:

```angular2html
pipenv shell
python -m ipykernel install --user --name=my-virtualenv-name
jupyter notebook
```

Then click to `Kernel` -> `Change kernel` -> `my-virtualenv-name`
