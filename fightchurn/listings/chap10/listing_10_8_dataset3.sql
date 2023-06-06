with observation_params as
(
    select  interval '%metric_interval' as metric_period,
    '%from_yyyy-mm-dd'::timestamp as obs_start,
    '%to_yyyy-mm-dd'::timestamp as obs_end
)
select m.account_id, o.observation_date, is_churn,
a.channel,
a.country,
date_part('day',o.observation_date::timestamp - a.date_of_birth::timestamp)::float/365.0 as customer_age,
sum(case when metric_name_id=1 then metric_value else 0 end) as add_contact,
sum(case when metric_name_id=2 then metric_value else 0 end) as edit_contact,
sum(case when metric_name_id=3 then metric_value else 0 end) as add_lead,
sum(case when metric_name_id=4 then metric_value else 0 end) as edit_lead,
sum(case when metric_name_id=5 then metric_value else 0 end) as email_lead,
sum(case when metric_name_id=6 then metric_value else 0 end) as call_lead,
sum(case when metric_name_id=7 then metric_value else 0 end) as unsub_lead,
sum(case when metric_name_id=8 then metric_value else 0 end) as create_list,
sum(case when metric_name_id=9 then metric_value else 0 end) as delete_list,
sum(case when metric_name_id=10 then metric_value else 0 end) as email_list,
sum(case when metric_name_id=11 then metric_value else 0 end) as meetings,
sum(case when metric_name_id=12 then metric_value else 0 end) as schedule_meeting,
sum(case when metric_name_id=13 then metric_value else 0 end) as edit_meeting,
sum(case when metric_name_id=14 then metric_value else 0 end) as cancel_meeting,
sum(case when metric_name_id=15 then metric_value else 0 end) as quote,
sum(case when metric_name_id=16 then metric_value else 0 end) as create_opportunity,
sum(case when metric_name_id=17 then metric_value else 0 end) as advance_stage,
sum(case when metric_name_id=18 then metric_value else 0 end) as win_opportunity,
sum(case when metric_name_id=19 then metric_value else 0 end) as add_competitor,

sum(case when metric_name_id=21 then metric_value else 0 end) as lose_opportunity,

sum(case when metric_name_id=23 then metric_value else 0 end) as search,
sum(case when metric_name_id=44 then metric_value else 0 end) as search_actions,

sum(case when metric_name_id=27 then metric_value else 0 end) as discount,
sum(case when metric_name_id=29 then metric_value else 0 end) as bill_period_months,
sum(case when metric_name_id=30 then metric_value else 0 end) as mrr,
sum(case when metric_name_id=31 then metric_value else 0 end) as opp_value_per_month,
sum(case when metric_name_id=32 then metric_value else 0 end) as users_purchased,
sum(case when metric_name_id=33 then metric_value else 0 end) as opp_close_per_dollar,
sum(case when metric_name_id=34 then metric_value else 0 end) as active_users_per_month,
sum(case when metric_name_id=35 then metric_value else 0 end) as user_utilization,
sum(case when metric_name_id=36 then metric_value else 0 end) as search_action_per_search,

sum(case when metric_name_id=38 then metric_value else 0 end) as loss_rate,
sum(case when metric_name_id=39 then metric_value else 0 end) as cancel_meeting_rate,
sum(case when metric_name_id=40 then metric_value else 0 end) as deletes_per_email,
sum(case when metric_name_id=45 then metric_value else 0 end) as search_actions_per_dollar_closed,
sum(case when metric_name_id=46 then metric_value else 0 end) as mrr_per_lead_added,
sum(case when metric_name_id=47 then metric_value else 0 end) as mrr_per_dollar_opp_close,
sum(case when metric_name_id=48 then metric_value else 0 end) as mrr_per_active_user,
sum(case when metric_name_id=49 then metric_value else 0 end) as opp_value_lost_per_month,
sum(case when metric_name_id=50 then metric_value else 0 end) as total_opp_value_closed,
sum(case when metric_name_id=51 then metric_value else 0 end) as pcnt_opp_value_lost,
sum(case when metric_name_id=52 then metric_value else 0 end) as opp_value_closed_per_active_user

from metric m inner join observation_params
on metric_time between obs_start and obs_end
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp
    and m.metric_time <= o.observation_date::timestamp
inner join account a on m.account_id = a.id
group by m.account_id, metric_time, observation_date, is_churn, a.channel, date_of_birth, country
order by observation_date,m.account_id
