

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Geo-centroid aggregation](search-aggregations-metrics-geocentroid-
aggregation.md) [Cartesian-bounds aggregation »](search-aggregations-
metrics-cartesian-bounds-aggregation.md)

## 地理线聚合

"geo_line"聚合将存储桶中的所有"geo_point"值聚合到按所选"排序"字段排序的"LineString"中。例如，此"排序"可以是日期字段。返回的存储桶是表示线几何的有效 GeoJSONFeature。

    
    
    PUT test
    {
        "mappings": {
            "properties": {
                "my_location": { "type": "geo_point" },
                "group":       { "type": "keyword" },
                "@timestamp":  { "type": "date" }
            }
        }
    }
    
    POST /test/_bulk?refresh
    {"index":{}}
    {"my_location": {"lat":52.373184, "lon":4.889187}, "@timestamp": "2023-01-02T09:00:00Z"}
    {"index":{}}
    {"my_location": {"lat":52.370159, "lon":4.885057}, "@timestamp": "2023-01-02T10:00:00Z"}
    {"index":{}}
    {"my_location": {"lat":52.369219, "lon":4.901618}, "@timestamp": "2023-01-02T13:00:00Z"}
    {"index":{}}
    {"my_location": {"lat":52.374081, "lon":4.912350}, "@timestamp": "2023-01-02T16:00:00Z"}
    {"index":{}}
    {"my_location": {"lat":52.371667, "lon":4.914722}, "@timestamp": "2023-01-03T12:00:00Z"}
    
    POST /test/_search?filter_path=aggregations
    {
      "aggs": {
        "line": {
          "geo_line": {
            "point": {"field": "my_location"},
            "sort":  {"field": "@timestamp"}
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "line": {
          "type": "Feature",
          "geometry": {
            "type": "LineString",
            "coordinates": [
                [ 4.889187, 52.373184 ],
                [ 4.885057, 52.370159 ],
                [ 4.901618, 52.369219 ],
                [ 4.912350, 52.374081 ],
                [ 4.914722, 52.371667 ]
            ]
          },
          "properties": {
            "complete": true
          }
        }
      }
    }

生成的GeoJSONFeature既包含聚合生成的路径的"LineString"几何图形，也包含"属性"的映射。属性"complete"通知是否所有匹配的文档都用于生成几何图形。"size"选项可用于限制聚合中包含的文档数量，从而导致结果为"complete： false"。从结果中删除的确切文档取决于聚合是否基于"time_series"。

此结果可以显示在地图用户界面中：

!Kibana 地图与阿姆斯特丹博物馆之旅

###Options

`point`

     (Required) 

此选项指定"geo_point"字段的名称

将"my_location"配置为点字段的示例用法：

    
    
    "point": {
      "field": "my_location"
    }

`sort`

     (Required outside [`time_series`](search-aggregations-metrics-geo-line.html#search-aggregations-metrics-geo-line-grouping-time-series "Grouping with time-series") aggregations) 

此选项指定要用作对点进行排序的排序键的数值字段的名称。当"geo_line"聚合嵌套在"time_series"聚合中时，此字段默认为"@timestamp"，任何其他值都会导致错误。

将"@timestamp"配置为排序键的示例用法：

    
    
    "sort": {
      "field": "@timestamp"
    }

`include_sort`

     (Optional, boolean, default: `false`) This option includes, when true, an additional array of the sort values in the feature properties. 
`sort_order`

     (Optional, string, default: `"ASC"`) This option accepts one of two values: "ASC", "DESC". The line is sorted in ascending order by the sort key when set to "ASC", and in descending with "DESC". 

`size`

     (Optional, integer, default: `10000`) The maximum length of the line represented in the aggregation. Valid sizes are between one and 10000. Within [`time_series`](search-aggregations-metrics-geo-line.html#search-aggregations-metrics-geo-line-grouping-time-series "Grouping with time-series") the aggregation uses line simplification to constrain the size, otherwise it uses truncation. Refer to [Why group with time-series?](search-aggregations-metrics-geo-line.html#search-aggregations-metrics-geo-line-grouping-time-series-advantages "Why group with time-series?") for a discussion on the subtleties involved. 

###Grouping

这个简单的示例为查询选择的所有数据生成单个轨道。但是，需要将数据分组到多个轨道中更为常见。例如，按航班呼号对飞行应答器测量值进行分组，然后按时间戳对每个航班进行排序，并为每个航班生成单独的轨迹。

在以下示例中，我们将对阿姆斯特丹、安特卫普和巴黎等城市的兴趣点位置进行分组。这些轨道将按计划的参观顺序排序，以便步行游览博物馆和其他景点。

为了演示时间序列分组和匿名时间序列分组之间的区别，我们将首先创建一个启用时间序列的索引，然后给出不使用时间序列和时间序列对相同数据进行分组的示例。

    
    
    PUT tour
    {
        "mappings": {
            "properties": {
                "city": {
                    "type": "keyword",
                    "time_series_dimension": true
                },
                "category":   { "type": "keyword" },
                "route":      { "type": "long" },
                "name":       { "type": "keyword" },
                "location":   { "type": "geo_point" },
                "@timestamp": { "type": "date" }
            }
        },
        "settings": {
            "index": {
                "mode": "time_series",
                "routing_path": [ "city" ],
                "time_series": {
                    "start_time": "2023-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:00Z"
                }
            }
        }
    }
    
    POST /tour/_bulk?refresh
    {"index":{}}
    {"@timestamp": "2023-01-02T09:00:00Z", "route": 0, "location": "POINT(4.889187 52.373184)", "city": "Amsterdam", "category": "Attraction", "name": "Royal Palace Amsterdam"}
    {"index":{}}
    {"@timestamp": "2023-01-02T10:00:00Z", "route": 1, "location": "POINT(4.885057 52.370159)", "city": "Amsterdam", "category": "Attraction", "name": "The Amsterdam Dungeon"}
    {"index":{}}
    {"@timestamp": "2023-01-02T13:00:00Z", "route": 2, "location": "POINT(4.901618 52.369219)", "city": "Amsterdam", "category": "Museum", "name": "Museum Het Rembrandthuis"}
    {"index":{}}
    {"@timestamp": "2023-01-02T16:00:00Z", "route": 3, "location": "POINT(4.912350 52.374081)", "city": "Amsterdam", "category": "Museum", "name": "NEMO Science Museum"}
    {"index":{}}
    {"@timestamp": "2023-01-03T12:00:00Z", "route": 4, "location": "POINT(4.914722 52.371667)", "city": "Amsterdam", "category": "Museum", "name": "Nederlands Scheepvaartmuseum"}
    {"index":{}}
    {"@timestamp": "2023-01-04T09:00:00Z", "route": 5, "location": "POINT(4.401384 51.220292)", "city": "Antwerp", "category": "Attraction", "name": "Cathedral of Our Lady"}
    {"index":{}}
    {"@timestamp": "2023-01-04T12:00:00Z", "route": 6, "location": "POINT(4.405819 51.221758)", "city": "Antwerp", "category": "Museum", "name": "Snijders&Rockoxhuis"}
    {"index":{}}
    {"@timestamp": "2023-01-04T15:00:00Z", "route": 7, "location": "POINT(4.405200 51.222900)", "city": "Antwerp", "category": "Museum", "name": "Letterenhuis"}
    {"index":{}}
    {"@timestamp": "2023-01-05T10:00:00Z", "route": 8, "location": "POINT(2.336389 48.861111)", "city": "Paris", "category": "Museum", "name": "Musée du Louvre"}
    {"index":{}}
    {"@timestamp": "2023-01-05T14:00:00Z", "route": 9, "location": "POINT(2.327000 48.860000)", "city": "Paris", "category": "Museum", "name": "Musée dOrsay"}

### 使用术语分组

使用此数据，对于非时间序列用例，可以使用基于城市名称的术语聚合来完成分组。无论我们是否将"巡回赛"索引定义为时间序列索引，这都将起作用。

    
    
    POST /tour/_search?filter_path=aggregations
    {
      "aggregations": {
        "path": {
          "terms": {"field": "city"},
          "aggregations": {
            "museum_tour": {
              "geo_line": {
                "point": {"field": "location"},
                "sort": {"field": "@timestamp"}
              }
            }
          }
        }
      }
    }

其中返回：

    
    
    {
      "aggregations": {
        "path": {
          "doc_count_error_upper_bound": 0,
          "sum_other_doc_count": 0,
          "buckets": [
            {
              "key": "Amsterdam",
              "doc_count": 5,
              "museum_tour": {
                "type": "Feature",
                "geometry": {
                  "coordinates": [ [ 4.889187, 52.373184 ], [ 4.885057, 52.370159 ], [ 4.901618, 52.369219 ], [ 4.91235, 52.374081 ], [ 4.914722, 52.371667 ] ],
                  "type": "LineString"
                },
                "properties": {
                  "complete": true
                }
              }
            },
            {
              "key": "Antwerp",
              "doc_count": 3,
              "museum_tour": {
                "type": "Feature",
                "geometry": {
                  "coordinates": [ [ 4.401384, 51.220292 ], [ 4.405819, 51.221758 ], [ 4.4052, 51.2229 ] ],
                  "type": "LineString"
                },
                "properties": {
                  "complete": true
                }
              }
            },
            {
              "key": "Paris",
              "doc_count": 2,
              "museum_tour": {
                "type": "Feature",
                "geometry": {
                  "coordinates": [ [ 2.336389, 48.861111 ], [ 2.327, 48.86 ] ],
                  "type": "LineString"
                },
                "properties": {
                  "complete": true
                }
              }
            }
          ]
        }
      }
    }

这些结果包含一个存储桶数组，其中每个存储桶都是一个 JSON 对象，其中"键"显示"城市"字段的名称，以及一个名为"museum_tour"的内部聚合结果，其中包含描述该城市各个景点之间实际路线的 GeoJSONFeature。每个结果还包括一个具有"完整"值的"属性"对象，如果几何图形被截断到"size"参数中指定的限制，则该值将为"false"。请注意，当我们在下一个示例中使用"time_series"时，我们将得到结构略有不同的相同结果。

### 使用时间序列分组

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

使用与以前相同的数据，我们还可以使用"time_series"聚合执行分组。这将按 TSID 分组，TSID 定义为所有字段与"time_series_dimension：true"的组合，在本例中为前面术语聚合中使用的相同"城市"字段。仅当我们使用 'index.mode="time_series"' 将 'tour' 索引定义为时间序列索引时，此示例才有效。

    
    
    POST /tour/_search?filter_path=aggregations
    {
      "aggregations": {
        "path": {
          "time_series": {},
          "aggregations": {
            "museum_tour": {
              "geo_line": {
                "point": {"field": "location"}
              }
            }
          }
        }
      }
    }

嵌套在"time_series"聚合中时，"geo_line"聚合不再需要"sort"字段。这是因为排序字段设置为"@timestamp"，所有时间序列索引都按该字段进行预排序。如果您确实设置了此参数，并将其设置为"@timestamp"以外的其他内容，则会出现错误。

此查询将导致：

    
    
    {
      "aggregations": {
        "path": {
          "buckets": {
            "{city=Paris}": {
              "key": {
                "city": "Paris"
              },
              "doc_count": 2,
              "museum_tour": {
                "type": "Feature",
                "geometry": {
                  "coordinates": [ [ 2.336389, 48.861111 ], [ 2.327, 48.86 ] ],
                  "type": "LineString"
                },
                "properties": {
                  "complete": true
                }
              }
            },
            "{city=Antwerp}": {
              "key": {
                "city": "Antwerp"
              },
              "doc_count": 3,
              "museum_tour": {
                "type": "Feature",
                "geometry": {
                  "coordinates": [ [ 4.401384, 51.220292 ], [ 4.405819, 51.221758 ], [ 4.4052, 51.2229 ] ],
                  "type": "LineString"
                },
                "properties": {
                  "complete": true
                }
              }
            },
            "{city=Amsterdam}": {
              "key": {
                "city": "Amsterdam"
              },
              "doc_count": 5,
              "museum_tour": {
                "type": "Feature",
                "geometry": {
                  "coordinates": [ [ 4.889187, 52.373184 ], [ 4.885057, 52.370159 ], [ 4.901618, 52.369219 ], [ 4.91235, 52.374081 ], [ 4.914722, 52.371667 ] ],
                  "type": "LineString"
                },
                "properties": {
                  "complete": true
                }
              }
            }
          }
        }
      }
    }

这些结果与前面的"术语"聚合示例基本相同，但结构不同。在这里，我们看到存储桶以映射形式返回，其中键是 TSID 的内部描述。对于每个具有"time_series_dimension：true"的字段的唯一组合，此TSID都是唯一的。每个存储桶都包含一个"键"字段，该字段也是 TSID 的所有维度值的映射，在这种情况下，仅使用城市名称进行分组。此外，还有一个称为"museum_tour"的内部聚合结果，其中包含一个 GeoJSONFeature，用于描述该城市各个景点之间的实际路线。每个结果还包括一个具有"完整"值的"属性"对象，如果几何图形简化为"size"参数中指定的限制，则该值将为 false。

### 为什么要使用时间序列分组？

在查看这些示例时，您可能会认为使用"术语"或"time_series"对地理线进行分组之间几乎没有区别。但是，这两种情况在行为上存在一些重要差异。时序索引按非常特定的顺序存储在磁盘上。它们按时序维度字段预先分组，并按"@timestamp"字段预排序。这允许"geo_line"聚合得到显著优化：

* 为第一个存储桶分配的相同内存可以反复用于所有后续存储桶。这比同时收集所有存储桶的非时间序列情况所需的内存要少得多。  * 无需排序，因为数据是按"@timestamp"预先排序的。时间序列数据自然会以"DESC"顺序到达聚合收集器。这意味着如果我们指定"sort_order：ASC"(默认值)，我们仍然以"DESC"顺序收集，但在生成最终的"LineString"几何体之前执行有效的内存中反向顺序。  * "size"参数可用于流线简化算法。如果没有时间序列，我们被迫截断数据，默认情况下每个存储桶 10000 个文档后，以防止内存使用不受限制。这可能导致地理线被截断，从而丢失重要数据。通过时间序列，我们可以运行流线简化算法，保留对内存使用情况的控制，同时保持整体几何形状。事实上，对于大多数用例，将此"size"参数设置为更低的界限并节省更多内存是可行的。例如，如果要在具有特定分辨率的显示地图上绘制"geo_line"，则简化为少至 100 或 200 个点可能看起来同样好。这将节省服务器、网络和客户端上的内存。

注意：使用时间序列数据和使用"time_series"索引模式还有其他显著优势。这些在关于时间序列数据流的文档中进行了讨论")。

### 流线化

行简化是减小最终结果大小的好方法，最终结果发送到客户端，并显示在地图用户界面中。但是，通常这些算法使用大量内存来执行简化，需要将整个几何图形与支持数据一起保存在内存中以进行简化本身。流线简化算法的使用通过将内存限制在为简化几何定义的边界，允许在简化过程中将内存使用量降至最低。这只有在不需要排序的情况下才有可能，当分组由"time_series"聚合完成时，就是这种情况，在具有"time_series"索引模式的索引上运行。

在这些情况下，"geo_line"聚合将内存分配给指定的"大小"，然后用传入的文档填充该内存。一旦内存完全填满，行内的文档就会随着新文档的添加而被删除。选择要删除的文档是为了最大程度地减少对几何图形的视觉影响。这个过程利用了Visvalingam-Whyattalgorithm.从本质上讲，这意味着如果点具有最小的三角形面积，则删除点，三角形由所考虑的点定义，并且直线中前后的两个点定义。此外，我们使用球面坐标计算面积，以便平面变形不会影响选择。

为了证明线简化比线截断有多好，请考虑科迪亚克岛北岸的这个示例。这方面的数据只有 209 点，但如果我们想将"大小"设置为"100"，我们会得到戏剧性的截断。

!科迪亚克岛北部被截断为100点

灰线是 209 个点的整个几何形状，而蓝线是前 100 个点，与原始几何形状大不相同。

现在考虑将相同的几何图形简化为 100 个点。

!科迪亚克岛北部缩短为100点

为了进行比较，我们以灰色显示原始几何图形，以蓝色显示截断的几何图形，并以洋红色显示新的简化几何图形。可以看到新简化线与原始线的偏差，但整体几何形状看起来几乎相同，并且仍然可以清楚地识别为科迪亚克岛的北岸。

[« Geo-centroid aggregation](search-aggregations-metrics-geocentroid-
aggregation.md) [Cartesian-bounds aggregation »](search-aggregations-
metrics-cartesian-bounds-aggregation.md)
