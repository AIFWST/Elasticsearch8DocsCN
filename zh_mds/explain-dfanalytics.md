

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning data frame analytics APIs](ml-df-
analytics-apis.md)

[« Evaluate data frame analytics API](evaluate-dfanalytics.md) [Get data
frame analytics jobs API »](get-dfanalytics.md)

## 解释数据帧分析API

解释数据帧分析配置。

###Request

"获取_ml/data_frame/分析/_explain"

"发布_ml/data_frame/分析/_explain"

"获取_ml/data_frame/分析/<data_frame_analytics_id>/_explain"

"发布_ml/data_frame/分析/<data_frame_analytics_id>/_explain"

###Prerequisites

需要以下权限：

* 集群："monitor_ml"("machine_learning_user"内置角色授予此权限) * 源索引："读取"、"view_index_metadata"

###Description

此 API 为已存在或尚未创建的数据框分析配置提供说明。提供了以下说明：

* 分析中包含或不包含哪些字段以及原因， * 估计需要多少内存。在以后决定"model_memory_limit"设置的适当值时，可以使用估计值。

如果您有对象字段或通过源过滤排除的字段，则它们不包括在说明中。

### 路径参数

`<data_frame_analytics_id>`

     (Optional, string) Identifier for the data frame analytics job. 

### 请求正文

数据框分析配置，如创建数据框分析作业中所述。请注意，不需要在此 API 的上下文中提供"id"和"dest"。

### 响应正文

API 返回包含以下内容的响应：

`field_selection`

    

(阵列)解释每个字段的选择的对象数组，按字段名称排序。

"field_selection"对象的属性

`is_included`

     (Boolean) Whether the field is selected to be included in the analysis. 
`is_required`

     (Boolean) Whether the field is required. 
`feature_type`

     (string) The feature type of this field for the analysis. May be `categorical` or `numerical`. 
`mapping_types`

     (string) The mapping types of the field. 
`name`

     (string) The field name. 
`reason`

     (string) The reason a field is not selected to be included in the analysis. 

`memory_estimation`

    

(对象)包含内存估计值的对象。

"memory_estimation"的属性

`expected_memory_with_disk`

     (string) Estimated memory usage under the assumption that overflowing to disk is allowed during data frame analytics. `expected_memory_with_disk` is usually smaller than `expected_memory_without_disk` as using disk allows to limit the main memory needed to perform data frame analytics. 
`expected_memory_without_disk`

     (string) Estimated memory usage under the assumption that the whole data frame analytics should happen in memory (i.e. without overflowing to disk). 

###Examples

    
    
    POST _ml/data_frame/analytics/_explain
    {
      "source": {
        "index": "houses_sold_last_10_yrs"
      },
      "analysis": {
        "regression": {
          "dependent_variable": "price"
        }
      }
    }

API 返回以下结果：

    
    
    {
      "field_selection": [
        {
          "field": "number_of_bedrooms",
          "mappings_types": ["integer"],
          "is_included": true,
          "is_required": false,
          "feature_type": "numerical"
        },
        {
          "field": "postcode",
          "mappings_types": ["text"],
          "is_included": false,
          "is_required": false,
          "reason": "[postcode.keyword] is preferred because it is aggregatable"
        },
        {
          "field": "postcode.keyword",
          "mappings_types": ["keyword"],
          "is_included": true,
          "is_required": false,
          "feature_type": "categorical"
        },
        {
          "field": "price",
          "mappings_types": ["float"],
          "is_included": true,
          "is_required": true,
          "feature_type": "numerical"
        }
      ],
      "memory_estimation": {
        "expected_memory_without_disk": "128MB",
        "expected_memory_with_disk": "32MB"
      }
    }

[« Evaluate data frame analytics API](evaluate-dfanalytics.md) [Get data
frame analytics jobs API »](get-dfanalytics.md)
