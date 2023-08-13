

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Append processor](append-processor.md) [Bytes processor »](bytes-
processor.md)

## 附件处理器

附件处理器允许 Elasticsearch 使用 Apache 文本提取库 Tika 以常见格式(如 PPT、XLS 和 PDF)提取文件附件。

源字段必须是 base64 编码的二进制文件。如果不想产生在 base64 之间来回转换的开销，则可以使用 CBORformat 而不是 JSON，并将字段指定为字节数组而不是字符串表示形式。然后处理器将跳过 base64 解码。

### 在管道中使用附件处理器

**表 4.附件选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

从"target_field"获取 base64 编码字段的字段

|

no

|

attachment

|

将保存附件信息"indexed_chars"的字段

|

no

|

100000

|

用于提取以防止大字段的字符数。使用"-1"表示无限制。   "indexed_chars_field"

|

no

|

`null`

|

字段名称，您可以从中覆盖用于提取的字符数。参见"indexed_chars"。   "属性"

|

no

|

所有属性

|

要选择要存储的属性数组。可以是"内容"、"标题"、"姓名"、"作者"、"关键字"、"日期"、"content_type"、"content_length"、"语言"、"ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将悄悄退出，而不修改文档"remove_binary"

|

no

|

`false`

|

如果为"true"，则二进制"字段"将从文档"resource_name"中删除

|

no

|

|

包含要解码的资源的名称的字段。如果指定，处理器将此资源名称传递给底层 Tika 库以启用基于资源名称的检测。   ####Exampleedit

如果将文件附加到 JSON 文档，则必须首先将文件编码为 abase64 字符串。在类Unix系统上，您可以使用"base64"命令执行此操作：

    
    
    base64 -in myfile.rtf

该命令返回文件的 base64 编码字符串。以下base64字符串用于包含文本"Lorem ipsum dolor sitamet"的".rtf"文件：'e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0='。

使用附件处理器解码字符串并提取文件的属性：

    
    
    response = client.ingest.put_pipeline(
      id: 'attachment',
      body: {
        description: 'Extract attachment information',
        processors: [
          {
            attachment: {
              field: 'data',
              remove_binary: false
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id',
      pipeline: 'attachment',
      body: {
        data: 'e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0='
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    PUT _ingest/pipeline/attachment
    {
      "description" : "Extract attachment information",
      "processors" : [
        {
          "attachment" : {
            "field" : "data",
            "remove_binary": false
          }
        }
      ]
    }
    PUT my-index-000001/_doc/my_id?pipeline=attachment
    {
      "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0="
    }
    GET my-index-000001/_doc/my_id

文档的"附件"对象包含文件的提取属性：

    
    
    {
      "found": true,
      "_index": "my-index-000001",
      "_id": "my_id",
      "_version": 1,
      "_seq_no": 22,
      "_primary_term": 1,
      "_source": {
        "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=",
        "attachment": {
          "content_type": "application/rtf",
          "language": "ro",
          "content": "Lorem ipsum dolor sit amet",
          "content_length": 28
        }
      }
    }

将二进制文件保留为文档中的字段可能会消耗大量资源。强烈建议从文档中删除该字段。将"remove_binary"设置为"true"以自动删除该字段。

### 导出字段

可以从文档中提取的字段包括：

* "内容"， * "标题"， * "作者"， * "关键字"， * "日期"， * "content_type"， * "content_length"， * "语言"， * "修改"， * "格式"， * "标识符"， * "贡献者"， * "覆盖范围"， * "修饰符"， * "creator_tool"， * "出版商"， * "关系"， * "权利"， * "来源"， * "类型"， * "描述"， * "print_date"， * "metadata_date"， * "纬度"， * "经度"， * "海拔"， * "评级"， * "评论"

要仅提取某些"附件"字段，请指定"属性"数组：

    
    
    response = client.ingest.put_pipeline(
      id: 'attachment',
      body: {
        description: 'Extract attachment information',
        processors: [
          {
            attachment: {
              field: 'data',
              properties: [
                'content',
                'title'
              ],
              remove_binary: false
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/attachment
    {
      "description" : "Extract attachment information",
      "processors" : [
        {
          "attachment" : {
            "field" : "data",
            "properties": [ "content", "title" ],
            "remove_binary": false
          }
        }
      ]
    }

从二进制数据中提取内容是一项资源密集型操作，会消耗大量资源。强烈建议在专用采集节点中使用此处理器运行管道。

### 将附件处理器与 CBOR 一起使用

若要避免将 JSON 编码和解码为 base64，可以改为将 CBOR 数据传递到附件处理器。例如，以下请求创建使用附件处理器的"cbor-attachment"管道。

    
    
    response = client.ingest.put_pipeline(
      id: 'cbor-attachment',
      body: {
        description: 'Extract attachment information',
        processors: [
          {
            attachment: {
              field: 'data',
              remove_binary: false
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/cbor-attachment
    {
      "description" : "Extract attachment information",
      "processors" : [
        {
          "attachment" : {
            "field" : "data",
            "remove_binary": false
          }
        }
      ]
    }

以下 Python 脚本将 CBOR 数据传递给包含"cbor-attachment"管道的 HTTP 索引请求。HTTP 请求标头使用"application/cbor"的"内容类型"。

并非所有 Elasticsearch 客户端都支持自定义 HTTP 请求标头。

    
    
    import cbor2
    import requests
    
    file = 'my-file'
    headers = {'content-type': 'application/cbor'}
    
    with open(file, 'rb') as f:
      doc = {
        'data': f.read()
      }
      requests.put(
        'http://localhost:9200/my-index-000001/_doc/my_id?pipeline=cbor-attachment',
        data=cbor2.dumps(doc),
        headers=headers
      )

### 限制提取字符的数量

为了防止提取过多字符并使节点内存过载，默认情况下，用于提取的字符数限制为"100000"。您可以通过设置"indexed_chars"来更改此值。使用"-1"没有限制，但请确保在设置时，您的节点将有足够的堆来提取非常大的文档的内容。

您还可以通过从给定字段中提取要设置的限制来定义每个文档的此限制。如果文档具有该字段，它将覆盖"indexed_chars"设置。要设置此字段，请定义"indexed_chars_field"设置。

例如：

    
    
    response = client.ingest.put_pipeline(
      id: 'attachment',
      body: {
        description: 'Extract attachment information',
        processors: [
          {
            attachment: {
              field: 'data',
              indexed_chars: 11,
              indexed_chars_field: 'max_size',
              remove_binary: false
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id',
      pipeline: 'attachment',
      body: {
        data: 'e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0='
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    PUT _ingest/pipeline/attachment
    {
      "description" : "Extract attachment information",
      "processors" : [
        {
          "attachment" : {
            "field" : "data",
            "indexed_chars" : 11,
            "indexed_chars_field" : "max_size",
            "remove_binary": false
          }
        }
      ]
    }
    PUT my-index-000001/_doc/my_id?pipeline=attachment
    {
      "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0="
    }
    GET my-index-000001/_doc/my_id

返回以下内容：

    
    
    {
      "found": true,
      "_index": "my-index-000001",
      "_id": "my_id",
      "_version": 1,
      "_seq_no": 35,
      "_primary_term": 1,
      "_source": {
        "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=",
        "attachment": {
          "content_type": "application/rtf",
          "language": "is",
          "content": "Lorem ipsum",
          "content_length": 11
        }
      }
    }
    
    
    response = client.ingest.put_pipeline(
      id: 'attachment',
      body: {
        description: 'Extract attachment information',
        processors: [
          {
            attachment: {
              field: 'data',
              indexed_chars: 11,
              indexed_chars_field: 'max_size',
              remove_binary: false
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id_2',
      pipeline: 'attachment',
      body: {
        data: 'e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=',
        max_size: 5
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id_2'
    )
    puts response
    
    
    PUT _ingest/pipeline/attachment
    {
      "description" : "Extract attachment information",
      "processors" : [
        {
          "attachment" : {
            "field" : "data",
            "indexed_chars" : 11,
            "indexed_chars_field" : "max_size",
            "remove_binary": false
          }
        }
      ]
    }
    PUT my-index-000001/_doc/my_id_2?pipeline=attachment
    {
      "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=",
      "max_size": 5
    }
    GET my-index-000001/_doc/my_id_2

返回以下内容：

    
    
    {
      "found": true,
      "_index": "my-index-000001",
      "_id": "my_id_2",
      "_version": 1,
      "_seq_no": 40,
      "_primary_term": 1,
      "_source": {
        "data": "e1xydGYxXGFuc2kNCkxvcmVtIGlwc3VtIGRvbG9yIHNpdCBhbWV0DQpccGFyIH0=",
        "max_size": 5,
        "attachment": {
          "content_type": "application/rtf",
          "language": "sl",
          "content": "Lorem",
          "content_length": 5
        }
      }
    }

### 使用带有数组的附件处理器

要在附件数组中使用附件处理器，需要 foreach处理器。这使附件处理器能够在数组的各个元素上运行。

例如，给定以下源：

    
    
    {
      "attachments" : [
        {
          "filename" : "ipsum.txt",
          "data" : "dGhpcyBpcwpqdXN0IHNvbWUgdGV4dAo="
        },
        {
          "filename" : "test.txt",
          "data" : "VGhpcyBpcyBhIHRlc3QK"
        }
      ]
    }

在这种情况下，我们希望处理附件字段的每个元素中的数据字段，并将属性插入到文档中，以便使用以下"foreach"处理器：

    
    
    response = client.ingest.put_pipeline(
      id: 'attachment',
      body: {
        description: 'Extract attachment information from arrays',
        processors: [
          {
            foreach: {
              field: 'attachments',
              processor: {
                attachment: {
                  target_field: '_ingest._value.attachment',
                  field: '_ingest._value.data',
                  remove_binary: false
                }
              }
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id',
      pipeline: 'attachment',
      body: {
        attachments: [
          {
            filename: 'ipsum.txt',
            data: 'dGhpcyBpcwpqdXN0IHNvbWUgdGV4dAo='
          },
          {
            filename: 'test.txt',
            data: 'VGhpcyBpcyBhIHRlc3QK'
          }
        ]
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    PUT _ingest/pipeline/attachment
    {
      "description" : "Extract attachment information from arrays",
      "processors" : [
        {
          "foreach": {
            "field": "attachments",
            "processor": {
              "attachment": {
                "target_field": "_ingest._value.attachment",
                "field": "_ingest._value.data",
                "remove_binary": false
              }
            }
          }
        }
      ]
    }
    PUT my-index-000001/_doc/my_id?pipeline=attachment
    {
      "attachments" : [
        {
          "filename" : "ipsum.txt",
          "data" : "dGhpcyBpcwpqdXN0IHNvbWUgdGV4dAo="
        },
        {
          "filename" : "test.txt",
          "data" : "VGhpcyBpcyBhIHRlc3QK"
        }
      ]
    }
    GET my-index-000001/_doc/my_id

返回以下内容：

    
    
    {
      "_index" : "my-index-000001",
      "_id" : "my_id",
      "_version" : 1,
      "_seq_no" : 50,
      "_primary_term" : 1,
      "found" : true,
      "_source" : {
        "attachments" : [
          {
            "filename" : "ipsum.txt",
            "data" : "dGhpcyBpcwpqdXN0IHNvbWUgdGV4dAo=",
            "attachment" : {
              "content_type" : "text/plain; charset=ISO-8859-1",
              "language" : "en",
              "content" : "this is\njust some text",
              "content_length" : 24
            }
          },
          {
            "filename" : "test.txt",
            "data" : "VGhpcyBpcyBhIHRlc3QK",
            "attachment" : {
              "content_type" : "text/plain; charset=ISO-8859-1",
              "language" : "en",
              "content" : "This is a test",
              "content_length" : 16
            }
          }
        ]
      }
    }

请注意，需要设置"target_field"，否则使用默认值，即顶级字段"附件"。此顶级字段上的属性将仅包含第一个附件的值。但是，通过将"target_field"指定为"_ingest._value"上的值，它将正确地将属性与正确的附件相关联。

[« Append processor](append-processor.md) [Bytes processor »](bytes-
processor.md)
