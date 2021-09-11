## Errata for the first printing

### **In Chapter 2, pages 42-43, sidebar Code for fighting churn with data:**

*If you are using the code from github after September 2021, or the fightchurn pip package, the paths have changed from those described in the first printing.* 

In the first numbered list in the sidebar it should now read:

	2. Create a database schema with `fightchurn/datagen/churndb.py`.
 	3. Generate simulation data and save it into the Postgres schema with `fightchurn/datagen/churnsim.py`.

In the command line example after the third paragraph it should now read:

​	`fightchurn/run_churn_listing.py --chapter 2 --listing 1`

In the second numbered listed in the sidebar it should now read:

	1. Create a schema with `fightchurn/datagen/churndb.py`
 	2. ...
 	3. The listing wrapper program works from parameters stored in a JSON file, `fightchurn/listings/conf/churnsim_listings.json`.

### **In command line examples throughout the book:**

*If you are using the code from github after September 2021, or the fightchurn pip package, the paths have changed from those described in the first printing.* 

In the command line program examples it should read:

​	`fightchurn/run_churn_listing.py`

The correction above applies in the following places:

| Chapter | Section | Page |
| ------- | ------- | ---- |
| 2       | 2.3.2   | 52   |
| 2       | 2.4.3   | 60   |
| 2       | 2.5.2   | 60   |
| 2       | 2.6.2   | 68   |
| 2       | 2.7.3   | 75   |
| 3       | 3.3     | 88   |
| 3       | 3.5.1   | 94   |
| 3       | 3.5.3   | 97   |
| 3       | 3.5.4   | 98   |
| 3       | 3.7.1   | 103  |
| 3       | 3.8.1   | 110  |
| 3       | 3.10.3  | 123  |
| 4       | 4.3.3   | 145  |
| 5       | 5.1.2   | 182  |
| 5       | 5.2.2   | 198  |
| 6       | 6.1.2   | 223  |
| 7       | 7.1.1   | 264  |
| 7       | 7.1.2   | 266  |
| 7       | 7.1.2   | 267  |
| 7       | 7.2.1   | 276  |
| 7       | 7.3.1   | 285  |
| 7       | 7.3.2   | 292  |
| 7       | 7.4.1   | 297  |
| 8       | 8.2     | 326  |
| 8       | 8.2     | 328  |
| 8       | 8.3.2   | 333  |
| 9       | 9.1.2   | 373  |
| 9       | 9.1.3   | 378  |
| 9       | 9.2.2   | 384  |
| 9       | 9.3.2   | 387  |
| 9       | 9.4.2   | 391  |
| 9       | 9.5.2   | 399  |
| 9       | 9.5.4   | 402  |
| 10      | 10.1.3  | 413  |
| 10      | 10.2.3  | 420  |
| 10      | 10.3.2  | 428  |
| 10      | 10.5.1  | 435  |
| 10      | 10.5.2  | 436  |
| 10      | 10.5.3  | 440  |
| 10      | 10.5.3  | 441  |
| 10      | 10.5.4  | 442  |
| 10      | 10.5.4  | 444  |
| 10      | 10.6    | 447  |
| 10      | 10.6    | 450  |