

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Get data frame analytics jobs statistics API](get-dfanalytics-stats.md)
[Start data frame analytics jobs API »](start-dfanalytics.md)

## 预览数据帧分析API

预览数据框分析配置使用的功能。

###Request

"获取_ml/data_frame/分析/_preview"

"发布_ml/data_frame/分析/_preview"

"获取_ml/data_frame/分析/<data_frame_analytics_id>/_preview"

"发布_ml/data_frame/分析/<data_frame_analytics_id>/_preview"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

此 API 为已存在或尚未创建的数据框分析配置提供提取要素的预览。

### 路径参数

`<data_frame_analytics_id>`

     (Optional, string) Identifier for the data frame analytics job. 

### 请求正文

`config`

     (Optional, object) A data frame analytics config as described in [Create data frame analytics jobs](put-dfanalytics.html "Create data frame analytics jobs API"). Note that `id` and `dest` don't need to be provided in the context of this API. 

### 响应正文

API 返回包含以下内容的响应：

`feature_values`

     (array) An array of objects that contain feature name and value pairs. The features have been processed and indicate what will be sent to the model for training. 

###Examples

    
    
    POST _ml/data_frame/analytics/_preview
    {
      "config": {
        "source": {
          "index": "houses_sold_last_10_yrs"
        },
        "analysis": {
          "regression": {
            "dependent_variable": "price"
          }
        }
      }
    }

API 返回以下结果：

    
    
    {
      "feature_values": [
        {
          "number_of_bedrooms": "1",
          "postcode": "29655",
          "price": "140.4"
        },
        ...
      ]
    }

[« Get data frame analytics jobs statistics API](get-dfanalytics-stats.md)
[Start data frame analytics jobs API »](start-dfanalytics.md)
