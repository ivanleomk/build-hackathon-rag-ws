#  Introduction

This is a repo containing the code used for the workshop "Scaling beyond Vibe Checks" for the Build Together AI hackathon in Singapore.




## Installation

1. Install the required dependencies in the `requirements.txt` file in a virtual environment. I recommend using `uv` by astral to install and configure these dependencies

```bash
uv venv venv
uv pip install -r requirements.txt
```

2. Add the virtual environment to the IPython kernel so we can use it in jupyter notebok

```
python -m ipykernel install --user --name=vibecheck
```

3. Start the Jupyter Notebook. Make sure to select the new `vibecheck` kernel when running the notebooks so your installed packages are loaded in

```
jupyter notebook
```
