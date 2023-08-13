

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md) ›[Time series data stream (TSDS)](tsds.md)

[« Set up a time series data stream (TSDS)](set-up-tsds.md) [Downsampling a
time series data stream »](downsampling.md)

## 时序索引设置

时序数据流 (TSDS) 中的后备索引)支持以下索引设置。

`index.mode`

     ([Static](index-modules.html#_static_index_settings "Static index settings"), string) Mode for the index. Valid values are [`time_series`](tsds.html#time-series-mode "Time series mode") and `null` (no mode). Defaults to `null`. 

`index.time_series.start_time`

     ([Static](index-modules.html#_static_index_settings "Static index settings"), string) Earliest `@timestamp` value (inclusive) accepted by the index. Only indices with an `index.mode` of [`time_series`](tsds.html#time-series-mode "Time series mode") support this setting. For more information, refer to [Time-bound indices](tsds.html#time-bound-indices "Time-bound indices"). 

`index.time_series.end_time`

     ([Dynamic](index-modules.html#dynamic-index-settings "Dynamic index settings"), string) Latest `@timestamp` value (exclusive) accepted by the index. Only indices with an `index.mode` of `time_series` support this setting. For more information, refer to [Time-bound indices](tsds.html#time-bound-indices "Time-bound indices"). 

`index.look_ahead_time`

     ([Static](index-modules.html#_static_index_settings "Static index settings"), [time units](api-conventions.html#time-units "Time units")) Interval used to calculate the `index.time_series.end_time` for a TSDS's write index. Defaults to `2h` (2 hours). Accepts `1m` (one minute) to `7d` (seven days). Only indices with an `index.mode` of `time_series` support this setting. For more information, refer to [Look-ahead time](tsds.html#tsds-look-ahead-time "Look-ahead time"). Additionally this setting can not be less than `time_series.poll_interval` cluster setting. 
`index.routing_path`

     ([Static](index-modules.html#_static_index_settings "Static index settings"), string or array of strings) Plain `keyword` fields used to route documents in a TSDS to index shards. Supports wildcards (`*`). Only indices with an `index.mode` of `time_series` support this setting. Defaults to an empty list, except for data streams then defaults to the list of [dimension fields](tsds.html#time-series-dimension "Dimensions") with a `time_series_dimension` value of `true` defined in your component and index templates. For more information, refer to [Dimension-based routing](tsds.html#dimension-based-routing "Dimension-based routing"). 

`index.mapping.dimension_fields.limit`

     ([Dynamic](index-modules.html#dynamic-index-settings "Dynamic index settings"), integer) Maximum number of [time series dimensions](tsds.html#time-series-dimension "Dimensions") for the index. Defaults to `21`. 

[« Set up a time series data stream (TSDS)](set-up-tsds.md) [Downsampling a
time series data stream »](downsampling.md)
