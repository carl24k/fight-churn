

# fight-churn

<a name="top"/>

This is code for the book "***Fighting Churn With Data: Science and strategy for keeping your customers***"; the book serves as a detailed guide to the code.  You can get more information at:

- https://www.manning.com/books/fighting-churn-with-data, the publisher (Manning Publications)'s page for the book
- http://www.fightchurnwithdata.com, the author's blog site
- https://www.twitch.tv/carl24k_datascience, the author's live stream
- [The author's You Tube Channel, Fighting Churn With Data Science](https://www.youtube.com/channel/UCGVh5vcL4AAxErNdqJrr_Sw/featured)

This page contains the most up to date setup instructions.

## Note from the Author

Before you can load data or run the code you have to do some setup on your system. If you never have done this before it may seem like a lot of work, and it kind of is, but this amount of setup is routine when you begin to work with a new technology. These  setup instructions should work for most people using either shell Python, Jupyter Notebook, or an IDE, on either Mac or Windows.  That said, I must apologize because I am neither an expert in PostgreSQL nor an expert in Python, but I am about to give a lot of advice on how to setup and use these technologies - if you find I am not doing things the best way, or just not how you would have done it, please be patient.   If you want to make things better please help help out! :)

## **Setup Instructions**  

*WARNING TO PYPI USERS: None of the internal links in this document work on the pypi.org website! [To use the internal links in this README view it on github](https://github.com/carl24k/fight-churn).*

### Pre-Requisite Setup

Python and PostgreSQL are required.

- [**Pre-Requisites - Start Here!**](./readme_files/prereq.md)

### Code Setup

After the pre-requesisites, you have a choice on how to run the Fighting Churn With Data Code:

- [Command Line Setup](./readme_files/cmdline.md) : The fastest and easiest way to get started, using a `pip` Python package installation. This is great if you want to run the code and see the output, but you do not want to change the code or run it line by line.
- [Jupyter Notebook Setup](readme_files/notebook.md) : This is another way to get started quickly, if you already have Jupyter Notebooks installed.
- [Developers IDE Setup](readme_files/ide.md) : This method takes more time, but allows you to run 
  the code line by line in a debugger, or change it. (If you are a professional developer 
  planning to really use the code for your company, this is for you.)

## Errata for the 1st Printing

This version of the README if for the the code released with the fightchurn pip package in September 2021. In this version there have been some modifications to the paths described in the first printing of *Fighting Churn With Data* to enable packaging the Python code. The following two differences summarize the changes: 

- To run the code listings, the first printing of the book refers  to the script `fight-churn/listings/py/run_churn_list.py` : the path in the *current* code is `fight-churn/fightchurn/run_churn_listing.py`
- To generate the data, the first printing of the book refers to scripts under `fight-churn/data-generation/` : the path in the current code is `fight-churn/fightchurn/datagen`

[Complete details of the errata are described here](readme_files/errata.md).

## Extras

There is also some extra code from the development phase of the book, which are partially documented on [this page.](readme_files/extras.md)

## Authors

* **Carl Gold** [carl24k](https://github.com/carl24k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
