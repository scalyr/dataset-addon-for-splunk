#  DataSet Add-on for Splunk
The DataSet Add-on for Splunk provides integration with [DataSet](https://www.dataset.com) and [XDR](https://www.sentinelone.com/platform/xdr-ingestion) by [SentinelOne](https://sentinelone.com). The key functions allow two-way integration:
- SPL custom command to query directly from the Splunk UI.
- Inputs to index alerts as CIM-compliant, or any user-defined query results.
- Alert action to send events from Splunk.

## Installation
The add-on can be installed from [Splunkbase](https://splunkbase.splunk.com/app/6575) or manually via the .tgz file. For those looking to customize, the package subdirectory contains all artifacts. To compile, reference Splunk's [UCC Framework instructions](https://splunk.github.io/addonfactory-ucc-generator/how_to_use/) to use `ucc-gen` and `slim package`.

Reference Splunk documentation for [installing add-ons](https://docs.splunk.com/Documentation/AddOns/released/Overview/Installingadd-ons). 

## Permissions
The add-on uses Splunk encrypted secrets storage, so admins require `admin_all_objects` to create secret storage objects and users require `list_storage_passwords` capability to retrieve secrets.

### Splunk Enterprise
| Splunk component | Required | Comments |
| ------ | ------ | ------ |
| Search heads | Yes | Required to use the custom search command. |
| Indexers | No | Parsing is performed during data collection. | 
| Forwarders | Optional | For distributed deployments, if the modular inputs are used, this add-on is installed on heavy forwarders. |

### Splunk Cloud
| Splunk component | Required | Comments |
| ------ | ------ | ------ |
| Search heads | Yes | Required to use the custom search command. Splunk Cloud Victoria Experience also handles modular inputs on the search heads. |
| Indexers | No | Parsing is performed during data collection. | 
| Inputs Data Manager | Optional | For Splunk Cloud Classic Experience, if the modular inputs are used, this add-on is installed on an IDM. |

## Configuration
### XDR
1. From the SentinelOne console, ensure Enhanced Deep Visibility is enabled by clicking your name > My User > Change Deep Visibility Mode > Enhanced.

![Setting Enhanced Deep Visibility](README_images/setup_enhanced_dv.png)

2. Open Enhanced Deep Visibility.
3. Continue following the DataSet instructions below.

### Dataset (or XDR continued)
1. Make note of the URL (e.g. `https://app.scalyr.com` or `https://xdr.us1.sentinelone.net`). For XDR users, note this differs from the core SentinelOne console URL.
2. Navigate to API Keys.

![Creating DataSet API keys](README_images/dataset_key.png)

3. Click Add Key > Add Read Key (required for search command and inputs).
4. Click Add Key > Add Write Key (required for alert action).
5. Optionally, click the pencil icon to rename the keys.

### Splunk
1. In Splunk, open the Add-on

![Configuring DataSet Account](README_images/setup_account.png)

2. On the configuration > account tab:
- Click Add
- Enter a user-friendly account name. For multiple accounts, the account name can be used in queries (more details below).
- Enter the full URL noted above (e.g.: `https://app.scalyr.com` or `https://xdr.us1.sentinelone.net`).
- Enter the DataSet read key from above (required for searching)
- Enter the DataSet write key from above (only required for alert actions).
- Click Save

3. Optionally, configure logging level and proxy information on the associated tabs.
4. Click Save.
5. The included DataSet by Example dashboard can be used to confirm connectivity and also shows example searches to get started.

## SPL Command
The `| dataset` command allows queries against the [DataSet APIs](https://app.scalyr.com/help/api) directly from Splunk's search bar. 

Optional parameters are supported:

- **account** - If multiple accounts are used, the account name as configured in setup can be specified (`emea` in the screenshot above). If multiple accounts are configured but not specified in search, the first result (by alphanumeric name) is used. To search across all accounts, `account=*` can be used. 
- **method** - Define `query`, `powerquery`, `facet` or `timeseries` to call the appropriate REST endpoint. Default is query.
- **query** - The DataSet [query](https://app.scalyr.com/help/query-language) filter used to select events. Default is no filter (return all events limited by time and maxCount).
- **starttime** - The Splunk time picker can be used (not "All Time"), but if starttime is defined it will take precedence to define the [start time](https://app.scalyr.com/help/time-reference) for DataSet events to return. Use epoch time or relative shorthand in the form of a number followed by d, h, m or s (for days, hours, minutes or seconds), e.g.: `24h`. Default is 24h.
- **endtime** - The Splunk time picker can be used (not "All Time"), but if endtime is defined it will take precedence to define the [end time](https://app.scalyr.com/help/time-reference) for DataSet events to return. Use epoch time or relative shorthand in the form of a number followed by d, h, m or s (for days, hours, minutes or seconds), e.g.: `5m`. Default is current time at search.

For query and powerquery:
- **maxcount** - Number of events to return.
- **columns** - Specified fields to return from DataSet query (or powerquery, analogous to using `| columns` in a powerquery). Yields performance gains for high volume queries instead of returning and merging all fields.

For facet:
- **field** - Define field to get most frequent values of. Default is logfile.

For timeseries:
- **function** - Define value to compute from matching events. Default is rate.
- **buckets** - The number of numeric values to return by dividing time range into equal slices. Default is 1.
- **createsummaries** - Specify whether to create summaries to automatically update on ingestion pipeline. Default is true; recommend setting to false for one-off or while testing new queries.
- **useonlysummaries** - Specify whether to only use preexisting timeseries for fastest speed.

For all queries, be sure to `"`wrap the entire query in double quotes, and use `'`single quotes`'` inside`"` or double quotes `\"`escaped with a backslash`\"`, as shown in the following examples.

Query Example:
`| dataset method=query search="serverHost = * AND Action = 'allow'" maxcount=50 starttime=10m endtime=1m`

Power Query Example 1: `| dataset method=powerquery search="dataset = \"accesslog\"
| group requests = count(), errors = count(status == 404) by uriPath
| let rate = errors / requests
| filter rate > 0.01
| sort -rate"`

![SPL Power Query example](README_images/spl_powerquery.png)

Power Query Example 2: `| dataset account=emea method=powerQuery search="$serverHost == 'cloudWatchLogs' 
| parse 'RequestId: $RID$ Duration: $DUR$ ms Billed Duration: $BDUR$ ms Memory Size: $MEM$ MB Max Memory Used: $UMEM$ MB' 
| let deltaDUR= BDUR - DUR, deltaMEM = MEM - UMEM 
| sort -DUR 
| columns 'Request ID' = RID, 'Duration(ms)' = DUR, 'Charged delta (ms)' = deltaDUR, 'Used Memory (MB)' = UMEM, 'Charged delta Memory (MB)' = deltaMEM" starttime=5m`

Facet Query Example:
`
| dataset account=* method=facet search="serverHost = *" field=serverHost maxcount=25
| spath
| table value, count
`

Timeseries Query Example:
`
| dataset method=timeseries search="serverHost='scalyr-metalog'" function="p90(delayMedian)" starttime="24h" buckets=24 createsummaries=false onlyusesummaries=false
`

Since events are returned in JSON format, the Splunk [spath command](https://docs.splunk.com/Documentation/SplunkCloud/latest/SearchReference/Spath) is useful. Additionally, the Splunk [collect command](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/collect) can be used to add the events to a summary index:

`
| dataset query="serverHost = * AND Action = 'allow'" maxcount=50 starttime=10m endtime=1m
| spath
| collect index=dataset
`

## Inputs
For use cases requiring data indexed in Splunk, optional inputs are provided utilizing time-based checkpointing to prevent reindexing the same data:

| Source Type | Description | CIM Data Model |
| ------ | ------ | ------ |
| dataset:alerts | Predefined Power Query API call to index [alert state change records](https://app.scalyr.com/help/alerts#logging)  | [Alerts](https://docs.splunk.com/Documentation/CIM/latest/User/Alerts) |
| dataset:query | User-defined standard [query](https://app.scalyr.com/help/api#query) API call to index events | - |
| dataset:powerquery | User-defined [PowerQuery](https://app.scalyr.com/help/api#powerquery) API call to index events | - |

1. On the inputs page, click Create New Input and select the desired input

2. For DataSet alerts, enter:

![Setup alerts indexing](README_images/setup_alerts.png)
- A name for the input.
- Interval, in seconds. A good starting point is `300` seconds to collect every five mintues.
- Splunk index name
- Start time, in relative shorthand form, e.g.: `24h` for 24 hours before input execution time.

3. For DataSet queries, enter:

![Setup query indexing](README_images/setup_query.png)
- A name for the input.
- Interval, in seconds. A good starting point is `300` seconds to collect every five mintues.
- Splunk index name
- Start time, in relative shorthand form, e.g.: `24h` for 24 hours before input execution time.
- *(optional)* End time, in relative shorthand form, e.g.: `5m` for 5 minutes before input execution time.
- *(optional)* Query string used to return matching events.
- *(optional)* Maximum number of events to return.

4. For DataSet Power Queries, enter:
- A name for the input.
- Interval, in seconds. A good starting point is `300` seconds to collect every five mintues.
- Splunk index name
- Start time, in relative shorthand form, e.g.: `24h` for 24 hours before input execution time.
- *(optional)* End time, in relative shorthand form, e.g.: `5m` for 5 minutes before input execution time.
- Query string used to return matching events, including commands such as `| columns`, `| limit`, etc.

## Alert Action
An alert action allows sending an event to the DataSet [addEvents API](https://app.scalyr.com/help/api#addEvents). 

## Support and troubleshooting
Error saving configuration "CSRF validation failed" - This is a Splunk browser issue; try reloading the page, using a private window or clearing cache and cookies then retrying.

Search errors `Account token error, review search log for details` or `Splunk configuration error, see search log for details.` - API token was unable to be retrieved. Common issues include user role missing list_storage_passwords permission, API token not set or incorrect account name given that has not been configured. Review job inspector search log for errors returned by Splunk. `Error retrieving account settings, error = UrlEncoded('broken')` indicates a likely misconfigured or incorrect account name; `splunklib.binding.HTTPError: HTTP 403 Forbidden -- You (user=username) do not have permission to perform this operation (requires capability: list_storage_passwords OR admin_all_objects)` indicates missing Splunk user permissions (list_storage_passwords).

To troubleshoot the custom command, check the Job Inspector search log, also available in the internal index: `index=_internal app="TA-dataset" sourcetype=splunk_search_messages`.

For support, open a ticket with DataSet (or SentinelOne for XDR) support including any logged errors, or open a GitHub issue.

##### Note
This add-on was built with the [Splunk Add-on UCC framework](https://splunk.github.io/addonfactory-ucc-generator/) and uses the [Splunk Enterprise Python SDK](https://github.com/splunk/splunk-sdk-python).
Splunk is a trademark or registered trademark of Splunk Inc. in the United States and other countries.
