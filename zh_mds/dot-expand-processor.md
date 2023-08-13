

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Dissect processor](dissect-processor.md) [Drop processor »](drop-
processor.md)

## 点扩展器处理器

将带点的字段展开为对象字段。此处理器允许管道中的其他处理器访问名称中带有点的字段。否则，任何处理器都无法访问这些字段。

**表 15.点展开选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要展开为对象字段的字段。如果设置为"*"，则将展开所有顶级字段。   "路径"

|

no

|

-

|

包含要展开的字段的字段。仅当要展开的字段是另一个对象字段的一部分时才需要，因为"字段"选项只能理解叶字段。   "覆盖"

|

no

|

false

|

控制已存在与展开字段冲突的现有嵌套对象时的行为。当"false"时，处理器将通过将旧值和新值组合到一个数组中来合并冲突。当"true"时，扩展字段中的值将覆盖现有值。   "说明"

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

处理器的标识符。对于调试和指标很有用。               { "dot_expander"： { "字段"： "foo.bar" } }

例如，点展开处理器将转动此文档：

    
    
    {
      "foo.bar" : "value"
    }

into:

    
    
    {
      "foo" : {
        "bar" : "value"
      }
    }

如果"foo"下已经嵌套了一个"bar"字段，则此处理器会将"foo.bar"字段合并到其中。如果字段是标量值，则它将将该字段转换为数组字段。

例如，以下文档：

    
    
    {
      "foo.bar" : "value2",
      "foo" : {
        "bar" : "value1"
      }
    }

由"dot_expander"处理器转换为：

    
    
    {
      "foo" : {
        "bar" : ["value1", "value2"]
      }
    }

与"覆盖"选项设置为"true"时形成对比。

    
    
    {
      "dot_expander": {
        "field": "foo.bar",
        "override": true
      }
    }

在这种情况下，展开字段的值将覆盖 thenested 对象的值。

    
    
    {
      "foo" : {
        "bar" : "value2"
      }
    }

* * *

"字段"的值也可以设置为"*"以展开所有顶级虚线字段名称：

    
    
    {
      "dot_expander": {
        "field": "*"
      }
    }

点展开处理器将转动此文档：

    
    
    {
      "foo.bar" : "value",
      "baz.qux" : "value"
    }

into:

    
    
    {
      "foo" : {
        "bar" : "value"
      },
      "baz" : {
        "qux" : "value"
      }
    }

* * *

如果虚线字段嵌套在非虚线结构中，则使用"path"选项导航非虚线结构：

    
    
    {
      "dot_expander": {
        "path": "foo"
        "field": "*"
      }
    }

点展开处理器将转动此文档：

    
    
    {
      "foo" : {
        "bar.one" : "value",
        "bar.two" : "value"
      }
    }

into:

    
    
    {
      "foo" : {
        "bar" : {
          "one" : "value",
          "two" : "value"
        }
      }
    }

* * *

如果叶字段之外的任何字段与同名的预先存在的字段冲突，则需要先重命名该字段。

请考虑以下文档：

    
    
    {
      "foo": "value1",
      "foo.bar": "value2"
    }

然后，在应用"dot_expander"处理器之前，需要先重命名"foo"。因此，为了使"foo.bar"字段正确扩展到"foo"字段下的"bar"字段，应使用以下管道：

    
    
    {
      "processors" : [
        {
          "rename" : {
            "field" : "foo",
            "target_field" : "foo.bar"
          }
        },
        {
          "dot_expander": {
            "field": "foo.bar"
          }
        }
      ]
    }

原因是 Ingest 不知道如何自动将标量字段转换为对象字段。

[« Dissect processor](dissect-processor.md) [Drop processor »](drop-
processor.md)
