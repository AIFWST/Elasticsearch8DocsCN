

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Geo queries](geo-queries.md)

[« Geo-distance query](query-dsl-geo-distance-query.md) [Geo-polygon query
»](query-dsl-geo-polygon-query.md)

## 地理网格查询

匹配与 GeoGrid 聚合中的格网像元相交的"geo_point"和"geo_shape"值。

该查询旨在通过提供存储桶的键来匹配属于 ageogrid 聚合存储桶中的文档。对于地理哈希和地理切片格网，查询可用于geo_point和geo_shape字段。Forgeo_hex网格中，它只能用于geo_point字段。

####Example

假设以下文档已编制索引：

    
    
    response = client.indices.create(
      index: 'my_locations',
      body: {
        mappings: {
          properties: {
            location: {
              type: 'geo_point'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my_locations',
      id: 1,
      refresh: true,
      body: {
        location: 'POINT(4.912350 52.374081)',
        city: 'Amsterdam',
        name: 'NEMO Science Museum'
      }
    )
    puts response
    
    response = client.index(
      index: 'my_locations',
      id: 2,
      refresh: true,
      body: {
        location: 'POINT(4.405200 51.222900)',
        city: 'Antwerp',
        name: 'Letterenhuis'
      }
    )
    puts response
    
    response = client.index(
      index: 'my_locations',
      id: 3,
      refresh: true,
      body: {
        location: 'POINT(2.336389 48.861111)',
        city: 'Paris',
        name: 'Musée du Louvre'
      }
    )
    puts response
    
    
    PUT /my_locations
    {
      "mappings": {
        "properties": {
          "location": {
            "type": "geo_point"
          }
        }
      }
    }
    
    PUT /my_locations/_doc/1?refresh
    {
      "location" : "POINT(4.912350 52.374081)",
      "city": "Amsterdam",
      "name": "NEMO Science Museum"
    }
    
    PUT /my_locations/_doc/2?refresh
    {
      "location" : "POINT(4.405200 51.222900)",
      "city": "Antwerp",
      "name": "Letterenhuis"
    }
    
    PUT /my_locations/_doc/3?refresh
    {
      "location" : "POINT(2.336389 48.861111)",
      "city": "Paris",
      "name": "Musée du Louvre"
    }

### 地理哈希网格

使用geohash_grid聚合，可以根据文档的地理哈希值对文档进行分组：

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        size: 0,
        aggregations: {
          grouped: {
            geohash_grid: {
              field: 'location',
              precision: 2
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_locations/_search
    {
      "size" : 0,
      "aggs" : {
         "grouped" : {
            "geohash_grid" : {
               "field" : "location",
               "precision" : 2
            }
         }
      }
    }
    
    
    {
      "took" : 10,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 3,
          "relation" : "eq"
        },
        "max_score" : null,
        "hits" : [ ]
      },
      "aggregations" : {
        "grouped" : {
          "buckets" : [
            {
              "key" : "u1",
              "doc_count" : 2
            },
            {
              "key" : "u0",
              "doc_count" : 1
            }
          ]
        }
      }
    }

我们可以通过使用具有以下语法的存储桶键执行geo_gridquery来提取其中一个存储桶上的文档：

    
    
    GET /my_locations/_search
    {
      "query": {
        "geo_grid" :{
          "location" : {
            "geohash" : "u0"
          }
        }
      }
    }
    
    
    {
      "took" : 1,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my_locations",
            "_id" : "3",
            "_score" : 1.0,
            "_source" : {
              "location" : "POINT(2.336389 48.861111)",
              "city" : "Paris",
              "name" : "Musée du Louvre"
            }
          }
        ]
      }
    }

### 地理格网

使用geotile_grid聚合，可以根据文档的地理切片值对文档进行分组：

    
    
    response = client.search(
      index: 'my_locations',
      body: {
        size: 0,
        aggregations: {
          grouped: {
            geotile_grid: {
              field: 'location',
              precision: 6
            }
          }
        }
      }
    )
    puts response
    
    
    GET /my_locations/_search
    {
      "size" : 0,
      "aggs" : {
         "grouped" : {
            "geotile_grid" : {
               "field" : "location",
               "precision" : 6
            }
         }
      }
    }
    
    
    {
      "took" : 1,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 3,
          "relation" : "eq"
        },
        "max_score" : null,
        "hits" : [ ]
      },
      "aggregations" : {
        "grouped" : {
          "buckets" : [
            {
              "key" : "6/32/21",
              "doc_count" : 2
            },
            {
              "key" : "6/32/22",
              "doc_count" : 1
            }
          ]
        }
      }
    }

我们可以通过使用具有以下语法的存储桶键执行geo_gridquery来提取其中一个存储桶上的文档：

    
    
    GET /my_locations/_search
    {
      "query": {
        "geo_grid" :{
          "location" : {
            "geotile" : "6/32/22"
          }
        }
      }
    }
    
    
    {
      "took" : 1,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my_locations",
            "_id" : "3",
            "_score" : 1.0,
            "_source" : {
              "location" : "POINT(2.336389 48.861111)",
              "city" : "Paris",
              "name" : "Musée du Louvre"
            }
          }
        ]
      }
    }

### 地理六角网格

使用geohex_grid聚合，可以根据文档的地理十六进制值对文档进行分组：

    
    
    GET /my_locations/_search
    {
      "size" : 0,
      "aggs" : {
         "grouped" : {
            "geohex_grid" : {
               "field" : "location",
               "precision" : 1
            }
         }
      }
    }
    
    
    {
      "took" : 2,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 3,
          "relation" : "eq"
        },
        "max_score" : null,
        "hits" : [ ]
      },
      "aggregations" : {
        "grouped" : {
          "buckets" : [
            {
              "key" : "81197ffffffffff",
              "doc_count" : 2
            },
            {
              "key" : "811fbffffffffff",
              "doc_count" : 1
            }
          ]
        }
      }
    }

我们可以通过使用具有以下语法的存储桶键执行geo_gridquery来提取其中一个存储桶上的文档：

    
    
    GET /my_locations/_search
    {
      "query": {
        "geo_grid" :{
          "location" : {
            "geohex" : "811fbffffffffff"
          }
        }
      }
    }
    
    
    {
      "took" : 26,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 1.0,
        "hits" : [
          {
            "_index" : "my_locations",
            "_id" : "3",
            "_score" : 1.0,
            "_source" : {
              "location" : "POINT(2.336389 48.861111)",
              "city" : "Paris",
              "name" : "Musée du Louvre"
            }
          }
        ]
      }
    }

[« Geo-distance query](query-dsl-geo-distance-query.md) [Geo-polygon query
»](query-dsl-geo-polygon-query.md)
