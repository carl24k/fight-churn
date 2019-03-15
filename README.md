# fight-churn

This is code for the (forthcoming) book "Fighting Churn With Data: The
Subscribed Institute Guide to Data Driven Customer Engagement".  See
http://www.fightchurnwithdata.com for more information.

## Getting Started



### Prerequisites

* Python 3
* Postgres
* Data to analyze (no publicy available data at this time)


### Installing

You will need to create a schema with the tables in the schema folder - you
can use any tool or method you prefer.  After that you need to load subscription
and event data into those tables.  For details on the subscription data see
the blog posts on http://www.fightchurnwithdata.com for more information:

* [Subscription Data (and Churn Calculation)](http://fightchurnwithdata.com/how-to-calculate-churn-with-sql/)
* [Event Data (and Metricn Calculation)] (http://fightchurnwithdata.com/user-metrics-101/)


## Running the Code

### Book Examples

You can run the book examples with the project under _examples_.  

```
python churn_example.py
```

Currently everything is hard coded.  If you want to run just one example or
chapter you can uncomment the variables *one_chapter* and/or *one_example*.
Command line parameters coming soon...


### Metric Calculation

First you need to configure some metrics specifically for your event data in the file...

```
Give an example
```

## Authors

* **Carl Gold**[carl24k](https://github.com/carl24k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Coming soon
