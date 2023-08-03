[dataset_query://<name>]
account = DataSet account.
interval = Collection interval in seconds.
start_time = Start time for the DataSet query to use. Use shortform (e.g.: 1m, 24h, 3d).
end_time = If left blank, present time at query execution is used.
dataset_query_string = If left blank, all records (limited by max count) are retrieved.
dataset_query_columns = If left blank, all columns are retrieved.
max_count = Specifies the maximum number of records to return, from 1 to 5000. If left blank, the default is 100.
python.version = {default|python|python2|python3}
start_by_shell = {true|false}

[dataset_powerquery://<name>]
account = DataSet account.
interval = Collection interval in seconds.
start_time = Start time for the DataSet query to use. Use shortform (e.g.: 1m, 24h, 3d).
end_time = If left blank, timestamp and message from all records (limited by max count) are retrieved.
dataset_query_string = If left blank, all records (limited by max count) are retrieved.
python.version = {default|python|python2|python3}
start_by_shell = {true|false}

[dataset_alerts://<name>]
account = DataSet account.
interval = Collection interval in seconds.
start_time = Relative time to query back. Use short form relative time, e.g.: 24h or 30d. Reference https://app.scalyr.com/help/time-reference
python.version = {default|python|python2|python3}
start_by_shell = {true|false}
