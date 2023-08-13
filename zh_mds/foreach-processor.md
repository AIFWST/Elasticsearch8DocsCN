

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Fingerprint processor](fingerprint-processor.md) [Geo-grid processor
»](ingest-geo-grid-processor.md)

## Foreach处理器

对数组或对象的每个元素运行摄取处理器。

所有收录处理器都可以在数组或对象元素上运行。但是，如果元素的数量未知，则以相同的方式处理每个元素可能会很麻烦。

"foreach"处理器允许您指定一个包含数组或对象值的"字段"和一个要在字段中的每个元素上运行的"处理器"。

**表 20.福尔奇选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

包含数组或对象值的字段。   "处理器"

|

yes

|

-

|

摄取处理器以在每个元素上运行。   "ignore_missing"

|

no

|

false

|

如果为"true"，则在"字段"为"null"或缺失时，处理器将静默退出而不更改文档。   "说明"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。   #### 访问键和值编辑

当循环访问数组或对象时，"foreach"处理器将当前元素的值存储在"_ingest._value"摄取元数据字段中。"_ingest._value"包含整个元素值，包括任何子字段。您可以使用"_ingest._value"字段上的点表示法访问子字段值。

当迭代对象时，"foreach"处理器还将当前元素的键作为字符串存储在"_ingest._key"中。

您可以在"处理器"中访问和更改"_ingest._key"和"_ingest._value"。有关示例，请参阅对象示例。

#### 故障处理

如果"foreach"处理器无法处理元素，并且未指定"on_failure"处理器，则"foreach"处理器将以静默方式退出。这将使整个数组或对象值保持不变。

####Examples

以下示例显示了如何将"foreach"处理器与不同的数据类型和选项一起使用：

* 数组 * 对象数组 * 对象 * 故障处理

#####Array

假设以下文档：

    
    
    {
      "values" : ["foo", "bar", "baz"]
    }

当此"foreach"处理器对此示例文档进行操作时：

    
    
    {
      "foreach" : {
        "field" : "values",
        "processor" : {
          "uppercase" : {
            "field" : "_ingest._value"
          }
        }
      }
    }

然后文档在处理后将如下所示：

    
    
    {
      "values" : ["FOO", "BAR", "BAZ"]
    }

##### 对象数组

假设以下文档：

    
    
    {
      "persons" : [
        {
          "id" : "1",
          "name" : "John Doe"
        },
        {
          "id" : "2",
          "name" : "Jane Doe"
        }
      ]
    }

在这种情况下，需要删除"id"字段，因此使用以下"foreach"处理器：

    
    
    {
      "foreach" : {
        "field" : "persons",
        "processor" : {
          "remove" : {
            "field" : "_ingest._value.id"
          }
        }
      }
    }

处理后的结果是：

    
    
    {
      "persons" : [
        {
          "name" : "John Doe"
        },
        {
          "name" : "Jane Doe"
        }
      ]
    }

有关另一个对象数组示例，请参阅附件处理器文档。

#####Object

您还可以在对象字段上使用"foreach"处理器。例如，以下文档包含带有对象值的"产品"字段。

    
    
    {
      "products" : {
        "widgets" : {
          "total_sales" : 50,
          "unit_price": 1.99,
          "display_name": ""
        },
        "sprockets" : {
          "total_sales" : 100,
          "unit_price": 9.99,
          "display_name": "Super Sprockets"
        },
        "whizbangs" : {
          "total_sales" : 200,
          "unit_price": 19.99,
          "display_name": "Wonderful Whizbangs"
        }
      }
    }

以下"foreach"处理器将"products.display_name"的值更改为大写。

    
    
    {
      "foreach": {
        "field": "products",
        "processor": {
          "uppercase": {
            "field": "_ingest._value.display_name"
          }
        }
      }
    }

在文档上运行时，"foreach"处理器返回：

    
    
    {
      "products" : {
        "widgets" : {
          "total_sales" : 50,
          "unit_price" : 1.99,
          "display_name" : ""
        },
        "sprockets" : {
          "total_sales" : 100,
          "unit_price" : 9.99,
          "display_name" : "SUPER SPROCKETS"
        },
        "whizbangs" : {
          "total_sales" : 200,
          "unit_price" : 19.99,
          "display_name" : "WONDERFUL WHIZBANGS"
        }
      }
    }

以下"foreach"处理器将每个元素的键设置为"products.display_name"的值。如果"products.display_name"包含空字符串，处理器将删除该元素。

    
    
    {
      "foreach": {
        "field": "products",
        "processor": {
          "set": {
            "field": "_ingest._key",
            "value": "{{_ingest._value.display_name}}"
          }
        }
      }
    }

在上一个文档上运行时，"foreach"处理器返回：

    
    
    {
      "products" : {
        "Wonderful Whizbangs" : {
          "total_sales" : 200,
          "unit_price" : 19.99,
          "display_name" : "Wonderful Whizbangs"
        },
        "Super Sprockets" : {
          "total_sales" : 100,
          "unit_price" : 9.99,
          "display_name" : "Super Sprockets"
        }
      }
    }

##### 故障处理

包装的处理器可以有一个"on_failure"定义。例如，"id"字段可能不存在于所有人员对象上。您可以使用"on_failure"块将文档发送到索引以供以后检查，而不是使索引请求失败the_failure_index_：

    
    
    {
      "foreach" : {
        "field" : "persons",
        "processor" : {
          "remove" : {
            "field" : "_value.id",
            "on_failure" : [
              {
                "set" : {
                  "field": "_index",
                  "value": "failure_index"
                }
              }
            ]
          }
        }
      }
    }

在此示例中，如果"remove"处理器确实失败，则将更新到目前为止已处理的数组元素。

[« Fingerprint processor](fingerprint-processor.md) [Geo-grid processor
»](ingest-geo-grid-processor.md)
