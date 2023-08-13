

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Filters aggregation](search-aggregations-bucket-filters-aggregation.md)
[Geo-distance aggregation »](search-aggregations-bucket-geodistance-
aggregation.md)

## 常用项集聚合

查找频繁项目集的存储桶聚合。它是一种关联规则挖掘形式，用于标识经常一起发生的项目。经常一起购买的项目或倾向于同时发生的日志事件是频繁项目集的示例。查找常用项集有助于发现不同数据点(项)之间的关系。

聚合报告已关闭的项集。如果不存在具有相同文档比率(也称为其支持值)的超集，则频繁项目集称为 closed。例如，对于一个常用项目集，我们有以下两个候选项，它们具有相同的支持值：1\。"苹果、橙子、香蕉" 2\."苹果，橙子，香蕉，番茄"。仅返回第二项集("苹果、橙子、香蕉、番茄")和第一个集(是第二组的子集)。如果两个项目集的支持值不同，则可能会返回这两个项目集。

聚合的运行时间取决于数据和提供的参数。聚合可能需要很长时间才能完成。因此，建议使用异步搜索异步运行请求。

###Syntax

"frequent_item_sets"聚合单独如下所示：

    
    
    "frequent_item_sets": {
      "minimum_set_size": 3,
      "fields": [
        {"field": "my_field_1"},
        {"field": "my_field_2"}
      ]
    }

**表 49.'frequent_item_sets' 参数**

参数名称

|

Description

|

Required

|

默认值 ---|---|---|--- '字段'

|

(阵列)要分析的字段。

|

Required

|   "minimum_set_size"

|

(整数)一个项目集的最小大小。

|

Optional

|

"1" "minimum_support"

|

(整数)单项集的最低支持。

|

Optional

|

"0.1""大小"

|

(整数)要返回的顶级项集数。

|

Optional

|

"10""过滤器"

|

(对象)从分析中筛选文档的查询

|

Optional

|

'match_all' ####Fieldsedit

分析字段支持的字段类型包括这些类型的关键字、数字、ip、日期和数组。您还可以将运行时字段添加到分析字段。

如果分析字段的组合基数较高，则聚合可能需要大量系统资源。

您可以使用"包含"和"排除"参数筛选每个字段的值。参数可以是正则表达式字符串或精确术语的字符串数组。过滤后的值将从分析中删除，从而减少运行时间。如果同时定义了"包括"和"排除"，则以"排除"为准;这意味着首先评估"包含"，然后评估"排除"。

#### 最小设置大小

最小集大小是集需要包含的最小项数。值 1 返回单个项目的频率。仅返回至少包含"minimum_set_size"项数的项集。例如，仅当最小集大小为 3 或更小时，才会返回项目集"橙色、香蕉、苹果"。

#### 最低支持

最小支持值是项目集必须存在于其中才能被视为"频繁"的文档的比率。特别是，它是介于 0 和 1 之间的规范化值。它的计算方法是将包含设置的项目的文档数除以文档总数。

例如，如果给定项目集包含五个文档，并且文档总数为 20，则项目集的支持为 5/20 = 0.25。因此，仅当最小支持为 0.25 或更低时，才会返回此集。由于较高的最小支持会修剪更多的项目，因此计算的资源密集度较低。"minimum_support"参数会影响所需的内存和聚合的运行时。

####Size

此参数定义要返回的最大项集数。结果包含前 k 个项目集;具有最高支撑值的项目集。此参数对所需的内存和聚合的运行时有显著影响。

####Filter

用于筛选要用作分析一部分的文档的查询。生成项目集时，将忽略与筛选器不匹配的文档，但在计算项目集的支持时仍会计数。

如果要将项目集分析范围缩小到感兴趣的字段，请使用过滤器。使用顶级查询筛选数据集。

####Examples

在以下示例中，我们使用电子商务 Kibana 示例数据集。

#### 具有两个分析字段和一个"排除"参数的聚合

在第一个示例中，目标是根据交易数据 (1) 进行查找。客户经常从哪些产品类别一起购买产品，以及 (2.) 他们从哪些城市购买这些产品。我们希望排除位置信息不可用的结果(城市名称为"其他")。最后，我们对包含三个或更多项目的集合感兴趣，并希望看到支持率最高的前三个常用项目集合。

请注意，我们在第一个示例中使用异步搜索终结点。

    
    
    POST /kibana_sample_data_ecommerce/_async_search
    {
       "size":0,
       "aggs":{
          "my_agg":{
             "frequent_item_sets":{
                "minimum_set_size":3,
                "fields":[
                   {
                      "field":"category.keyword"
                   },
                   {
                      "field":"geoip.city_name",
                      "exclude":"other"
                   }
                ],
                "size":3
             }
          }
       }
    }

上述 API 调用的响应包含异步搜索请求的标识符 ('id')。您可以使用标识符检索搜索结果：

    
    
    GET /_async_search/<id>

API 返回类似于以下内容的响应：

    
    
    (...)
    "aggregations" : {
        "my_agg" : {
          "buckets" : [ __{
              "key" : { __"category.keyword" : [
                  "Women's Clothing",
                  "Women's Shoes"
                ],
                "geoip.city_name" : [
                  "New York"
                ]
              },
              "doc_count" : 217, __"support" : 0.04641711229946524 __},
            {
              "key" : {
                "category.keyword" : [
                  "Women's Clothing",
                  "Women's Accessories"
                ],
                "geoip.city_name" : [
                  "New York"
                ]
              },
              "doc_count" : 135,
              "support" : 0.028877005347593583
            },
            {
              "key" : {
                "category.keyword" : [
                  "Men's Clothing",
                  "Men's Shoes"
                ],
                "geoip.city_name" : [
                  "Cairo"
                ]
              },
              "doc_count" : 123,
              "support" : 0.026310160427807486
            }
          ],
        (...)
      }
    }

__

|

返回的项集的数组。   ---|---    __

|

"键"对象包含一个项目集。在这种情况下，它由"category.keyword"字段的两个值和一个"geoip.city_name"的值组成。   __

|

包含项目集的文档数。   __

|

项集的支持值。它的计算方法是将包含所设置项目的文档数除以文档总数。   回复显示，客户最常一起购买的类别是"女装"和"女鞋"，来自纽约的顾客倾向于经常一起购买这些类别的商品。换句话说，购买标有"女装"的产品的顾客更有可能购买"女鞋"类别的产品，而来自纽约的客户最有可能一起购买这些类别的产品。获得第二高支持率的商品是"女装"和"女装配饰"，顾客大多来自纽约。最后，支持率排名第三的商品是"男装"和"男鞋"，顾客大多来自开罗。

#### 具有两个分析字段和筛选器的聚合

我们以第一个例子为例，但希望将项目集缩小到欧洲的地方。为此，我们添加一个过滤器，这一次，我们不使用 'exclude' 参数：

    
    
    POST /kibana_sample_data_ecommerce/_async_search
    {
      "size": 0,
      "aggs": {
        "my_agg": {
          "frequent_item_sets": {
            "minimum_set_size": 3,
            "fields": [
              { "field": "category.keyword" },
              { "field": "geoip.city_name" }
            ],
            "size": 3,
            "filter": {
              "term": {
                "geoip.continent_name": "Europe"
              }
            }
          }
        }
      }
    }

结果将仅显示从与筛选器匹配的文档创建的物料集，即在欧洲的购买。使用"过滤器"，计算出的"支持"仍然将所有购买计入计数。这与在顶层指定 aquery 不同，在这种情况下，"支持"仅从欧洲的购买中计算。

#### 使用运行时字段分析数值

频繁项目聚合使您能够使用运行时字段对数值进行存储桶。下一个示例演示如何使用脚本向文档添加名为"price_range"的运行时字段，该字段是根据各个交易的纳税总价计算得出的。然后，可以在频繁项聚合中将运行时字段用作要分析的字段。

    
    
    GET kibana_sample_data_ecommerce/_search
    {
      "runtime_mappings": {
        "price_range": {
          "type": "keyword",
          "script": {
            "source": """
               def bucket_start = (long) Math.floor(doc['taxful_total_price'].value / 50) * 50;
               def bucket_end = bucket_start + 50;
               emit(bucket_start.toString() + "-" + bucket_end.toString());
            """
          }
        }
      },
      "size": 0,
      "aggs": {
        "my_agg": {
          "frequent_item_sets": {
            "minimum_set_size": 4,
            "fields": [
              {
                "field": "category.keyword"
              },
              {
                "field": "price_range"
              },
              {
                "field": "geoip.city_name"
              }
            ],
            "size": 3
          }
        }
      }
    }

API 返回类似于以下内容的响应：

    
    
    (...)
    "aggregations" : {
        "my_agg" : {
          "buckets" : [
            {
              "key" : {
                "category.keyword" : [
                  "Women's Clothing",
                  "Women's Shoes"
                ],
                "price_range" : [
                  "50-100"
                ],
                "geoip.city_name" : [
                  "New York"
                ]
              },
              "doc_count" : 100,
              "support" : 0.0213903743315508
            },
            {
              "key" : {
                "category.keyword" : [
                  "Women's Clothing",
                  "Women's Shoes"
                ],
                "price_range" : [
                  "50-100"
                ],
                "geoip.city_name" : [
                  "Dubai"
                ]
              },
              "doc_count" : 59,
              "support" : 0.012620320855614974
            },
            {
              "key" : {
                "category.keyword" : [
                  "Men's Clothing",
                  "Men's Shoes"
                ],
                "price_range" : [
                  "50-100"
                ],
                "geoip.city_name" : [
                  "Marrakesh"
                ]
              },
              "doc_count" : 53,
              "support" : 0.011336898395721925
            }
          ],
        (...)
        }
      }

响应显示客户最常一起购买的类别、倾向于从这些类别购买商品的客户的位置以及这些购买的最频繁价格范围。

[« Filters aggregation](search-aggregations-bucket-filters-aggregation.md)
[Geo-distance aggregation »](search-aggregations-bucket-geodistance-
aggregation.md)
