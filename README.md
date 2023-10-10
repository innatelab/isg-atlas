# The ISG screen analysis
---------
## How to run the jupyter notebook:
   
1. [Install python](https://www.python.org/downloads/) depending on your operating system. (Alternatively you could also [install conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation))
2. Clone or Download this repositery.
3. Open terminal (or command prompt for windows) and navigate to the project's folder.
4. Create a python's virtual environment named `isg_screen` using the command:

```python -m venv isg_screen```
   
6. Activate the environment using:
   1. Unix: `source ./isg_screen/bin/activate `
   2. Windows: `.\isg_screen\Scripts\Activate`
7. Install the required packages using:

   ```pip install -r requirements.txt```
   
8. Start jupyter notebook ```jupyter notebook main_analysis.ipynb```

More info about creating a virtual environment and installing packages can be found [here](https://docs.python.org/3/library/venv.html).
