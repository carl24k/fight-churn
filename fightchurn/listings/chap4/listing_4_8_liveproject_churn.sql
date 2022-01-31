select count(*) as num_customers,
sum(is_churn::int) as num_churn,
sum(is_churn::int)::float  / count(*)::float as pcnt_churn
from observation;
