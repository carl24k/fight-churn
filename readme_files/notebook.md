<a name="notebook"/>

# Jupyter Notebook Setup

These instructions assume you already have Jupyter Notebooks installed. If you don't then you can consider the resources at https://jupyter.org/install. 

## 1. Installing Packages Under Jupyter


To install the required packages, run the following:

```python
import sys
!{sys.executable} -m pip install fightchurn
```


## 2 Import the run_churn_listing_module

```python
from fightchurn import run_churn_listing
from fightchurn.run_churn_listing import run_listing
```

## 2  Set the churn environment variables


```python
run_churn_listing.set_churn_environment('churn','user','password','/path/to/my_churn_output_folder')
```



---

<a name="simulate"/>

## 3 Run the data simulation


```python
run_churn_listing.run_standard_simulation(init_customers=10000)
```


---

<a name="run"/>

## 4 Run code listings


```python
run_listing(2,1)
```

------

------

