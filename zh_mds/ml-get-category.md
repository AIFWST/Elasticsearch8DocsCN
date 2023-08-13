

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get calendars API](ml-get-calendar.md) [Get datafeeds API »](ml-get-
datafeed.md)

## 获取类别API

检索一个或多个类别的异常情况检测作业结果。

###Request

"获取_ml/anomaly_detectors/<job_id>/结果/类别"

'获取_ml/anomaly_detectors/<job_id>/结果/类别/<category_id>"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

在作业配置中指定"categorization_field_name"时，可以查看结果类别的定义。类别定义描述匹配的常用术语，并包含匹配值的示例。

分类分析的异常结果可用作存储桶、影响因素和记录结果。例如，结果可能表明在 16：45 时，日志消息类别 11 的计数异常。然后，您可以检查该类别的说明和示例。更多信息，请参见日志消息分类。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 
`<category_id>`

     (Optional, long) Identifier for the category, which is unique in the job. If you specify neither the category ID nor the `partition_field_value`, the API returns information about all categories. If you specify only the `partition_field_value`, it returns information about all categories for the specified partition. 

### 查询参数

`from`

     (Optional, integer) Skips the specified number of categories. Defaults to `0`. 
`partition_field_value`

     (Optional, string) Only return categories for the specified partition. 
`size`

     (Optional, integer) Specifies the maximum number of categories to obtain. Defaults to `100`. 

### 请求正文

您还可以在请求正文中指定"partition_field_value"查询参数。

`page`

     Properties of `page`

`from`

     (Optional, integer) Skips the specified number of categories. Defaults to `0`. 
`size`

     (Optional, integer) Specifies the maximum number of categories to obtain. Defaults to `100`. 

### 响应正文

API 返回类别对象数组，这些对象具有以下属性：

`category_id`

     (unsigned integer) A unique identifier for the category. `category_id` is unique at the job level, even when per-partition categorization is enabled. 
`examples`

     (array) A list of examples of actual values that matched the category. 
`grok_pattern`

     [preview]  This functionality is in technical preview and may be changed or removed in a future release. Elastic will apply best effort to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.  (string) A Grok pattern that could be used in Logstash or an ingest pipeline to extract fields from messages that match the category. This field is experimental and may be changed or removed in a future release. The Grok patterns that are found are not optimal, but are often a good starting point for manual tweaking. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`max_matching_length`

     (unsigned integer) The maximum length of the fields that matched the category. The value is increased by 10% to enable matching for similar fields that have not been analyzed. 

`partition_field_name`

     (string) If per-partition categorization is enabled, this property identifies the field used to segment the categorization. It is not present when per-partition categorization is disabled. 
`partition_field_value`

     (string) If per-partition categorization is enabled, this property identifies the value of the `partition_field_name` for the category. It is not present when per-partition categorization is disabled. 
`regex`

     (string) A regular expression that is used to search for values that match the category. 
`terms`

     (string) A space separated list of the common tokens that are matched in values of the category. 
`num_matches`

     (long) The number of messages that have been matched by this category. This is only guaranteed to have the latest accurate count after a job `_flush` or `_close`
`preferred_to_categories`

     (list) A list of `category_id` entries that this current category encompasses. Any new message that is processed by the categorizer will match against this category and not any of the categories in this list. This is only guaranteed to have the latest accurate list of categories after a job `_flush` or `_close`

###Examples

    
    
    response = client.ml.get_categories(
      job_id: 'esxi_log',
      body: {
        page: {
          size: 1
        }
      }
    )
    puts response
    
    
    GET _ml/anomaly_detectors/esxi_log/results/categories
    {
      "page":{
        "size": 1
      }
    }
    
    
    {
      "count": 11,
      "categories": [
        {
          "job_id" : "esxi_log",
          "category_id" : 1,
          "terms" : "Vpxa verbose vpxavpxaInvtVm opID VpxaInvtVmChangeListener Guest DiskInfo Changed",
          "regex" : ".*?Vpxa.+?verbose.+?vpxavpxaInvtVm.+?opID.+?VpxaInvtVmChangeListener.+?Guest.+?DiskInfo.+?Changed.*",
          "max_matching_length": 154,
          "examples" : [
            "Oct 19 17:04:44 esxi1.acme.com Vpxa: [3CB3FB90 verbose 'vpxavpxaInvtVm' opID=WFU-33d82c31] [VpxaInvtVmChangeListener] Guest DiskInfo Changed",
            "Oct 19 17:04:45 esxi2.acme.com Vpxa: [3CA66B90 verbose 'vpxavpxaInvtVm' opID=WFU-33927856] [VpxaInvtVmChangeListener] Guest DiskInfo Changed",
            "Oct 19 17:04:51 esxi1.acme.com Vpxa: [FFDBAB90 verbose 'vpxavpxaInvtVm' opID=WFU-25e0d447] [VpxaInvtVmChangeListener] Guest DiskInfo Changed",
            "Oct 19 17:04:58 esxi2.acme.com Vpxa: [FFDDBB90 verbose 'vpxavpxaInvtVm' opID=WFU-bbff0134] [VpxaInvtVmChangeListener] Guest DiskInfo Changed"
          ],
          "grok_pattern" : ".*?%{SYSLOGTIMESTAMP:timestamp}.+?Vpxa.+?%{BASE16NUM:field}.+?verbose.+?vpxavpxaInvtVm.+?opID.+?VpxaInvtVmChangeListener.+?Guest.+?DiskInfo.+?Changed.*"
        }
      ]
    }

[« Get calendars API](ml-get-calendar.md) [Get datafeeds API »](ml-get-
datafeed.md)
