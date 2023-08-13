

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `position_increment_gap`](position-increment-gap.md) [`search_analyzer`
»](search-analyzer.md)

##'属性'

类型映射、"对象"字段和"嵌套"字段包含称为"属性"的子字段。这些属性可以是任何数据类型，包括"对象"和"嵌套"。可以添加属性：

* 通过在创建索引时显式定义它们。  * 通过使用更新映射 API 添加或更新映射类型时显式定义它们。  * 仅通过索引包含新字段的文档来动态。

下面是向映射类型、"对象"字段和"嵌套"字段添加"属性"的示例：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            manager: {
              properties: {
                age: {
                  type: 'integer'
                },
                name: {
                  type: 'text'
                }
              }
            },
            employees: {
              type: 'nested',
              properties: {
                age: {
                  type: 'integer'
                },
                name: {
                  type: 'text'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        region: 'US',
        manager: {
          name: 'Alice White',
          age: 30
        },
        employees: [
          {
            name: 'John Smith',
            age: 34
          },
          {
            name: 'Peter Brown',
            age: 26
          }
        ]
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": { __"manager": {
            "properties": { __"age":  { "type": "integer" },
              "name": { "type": "text"  }
            }
          },
          "employees": {
            "type": "nested",
            "properties": { __"age":  { "type": "integer" },
              "name": { "type": "text"  }
            }
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/1 __{
      "region": "US",
      "manager": {
        "name": "Alice White",
        "age": 30
      },
      "employees": [
        {
          "name": "John Smith",
          "age": 34
        },
        {
          "name": "Peter Brown",
          "age": 26
        }
      ]
    }

__

|

顶级映射定义中的属性。   ---|---    __

|

"管理器"对象字段下的属性。   __

|

"员工"嵌套字段下的属性。   __

|

对应于上述映射的示例文档。   允许"属性"设置对同一索引中同名的字段进行不同的设置。可以使用更新映射 API 将新属性添加到现有字段。

### 点表示法

内部字段可以在查询、聚合等中使用 _dotnotation_ 引用：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match: {
            "manager.name": 'Alice White'
          }
        },
        aggregations: {
          "Employees": {
            nested: {
              path: 'employees'
            },
            aggregations: {
              "Employee Ages": {
                histogram: {
                  field: 'employees.age',
                  interval: 5
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match": {
          "manager.name": "Alice White"
        }
      },
      "aggs": {
        "Employees": {
          "nested": {
            "path": "employees"
          },
          "aggs": {
            "Employee Ages": {
              "histogram": {
                "field": "employees.age",
                "interval": 5
              }
            }
          }
        }
      }
    }

必须指定内部字段的完整路径。

[« `position_increment_gap`](position-increment-gap.md) [`search_analyzer`
»](search-analyzer.md)
