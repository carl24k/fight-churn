# fight-churn

This is code for the (forthcoming) book "Fighting Churn With Data: The
Subscribed Institute Guide to Data Driven Customer Engagement".  See
http://www.fightchurnwithdata.com for more information.

## Getting Started



### Prerequisites

* Python 3 and the required packages (requirements.txt)
* Postgres
* Data to analyze (no publicy available data at this time)


### Installing

You will need to create a schema with the tables in the schema folder - you
can use any tool or method you prefer.  After that you need to load subscription
and event data into those tables.  For details on the subscription data see
the blog posts on http://www.fightchurnwithdata.com for more information:

* [Subscription Data (and Churn Calculation)](http://fightchurnwithdata.com/how-to-calculate-churn-with-sql/)
* [Event Data (and Metric Calculation)](http://fightchurnwithdata.com/user-metrics-101/)


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

First you need to configure some metrics specifically for your event data in a
configuration file for your schema.  See the examples
_metric-example/conf/x_metrics.json_ where the "x" is replaced with your
schema name.  Then running _metrics.py_ in the metric-framework folder will 1)
truncate the metrics in the metric table and 2) insert new metrics defined by
whatever is in  the file _metric-example/conf/yourschema_metrics.json_.  

Currently everything is hard coded, so you *must* set the postgres connection string, the 
schema, and date range in the file.  

```
python metrics.py
```

If you want to run just one metric you can uncomment the variable
*one_metric*.   Note that when running one metric currently you need to take
care of deleting values yourself (if you find yourself running the same metric
again after changes.)

Command line parameters coming soon...


### Evemt QA

Details coming soon...


```
python event_qa.py
```

### Metric QA

Details coming soon...


```
python metric_qa.py
```

## Authors

* **Carl Gold** [carl24k](https://github.com/carl24k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Coming soon
