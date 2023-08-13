

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md) ›[Migrating to 8.0](migrating-8.0.md)

[« Migrating to 8.0](migrating-8.0.md) [Transient settings migration guide
»](transient-settings-migration-guide.md)

## Java 时间迁移指南

在 7.0 中，Elasticsearch 从 joda 时间切换到 java 时间，以进行与日期相关的解析、格式化和计算。本指南旨在帮助您确定集群是否受到影响，如果是，请准备升级。

#### 转换日期格式

要升级到 Elasticsearch 8，您需要将任何 joda-time 日期格式转换为它们的 java-time 等效格式。

### 受影响的功能

切换到 java 时间只会影响自定义的"日期"和"date_nanos"格式。

这些格式通常用于：

* 索引映射 * 索引模板 * 引入管道

如果您不使用自定义日期格式，则可以跳过本指南的其余部分。大多数自定义日期格式都是兼容的。但是，有几个需要更新。

要查看您的日期格式是否受到影响，请使用弃用 infoAPI 或 KibanaUpgrade 助手。

### 不兼容的日期格式

应迁移包含以下 joda 时间文本的自定义日期格式。

"Y"(时代年份)

    

替换为"y"。

**示例：** "YYYY-MM-dd" 应变为 "yyyy-MM-dd"。

在java时间中，"Y"用于基于周的年份。使用"Y"代替"y"可能会导致年份计算中出现偏差错误。

对于模式"YYYY-ww"和日期"2019-01-01T00：00：00.000Z"将给出"2019-01"对于模式"YYYY-ww"，日期"2018-12-31T00：00：00.000Z"将给出"2019-01"(违反直觉)，因为 2019 年该周有 >4 天

"y"(年)

    

替换为"u"。

**示例：** 'yyyy-MM-dd' 应变为 'uuuu-MM-dd'。

在java时间中，"y"用于纪元年份。"u"可以包含非正值，而"y"不能。"y"也可以与纪元字段相关联。

"C"(世纪时代)

    

Java时代不支持百年时代。没有替代品。相反，我们建议您预处理输入。

"x"(周年)

    

替换为"Y"。

在 java 时间中，"x"表示区域偏移量。

未能正确将"x"(周年)转换为"Y"可能会导致数据丢失。

"Z"(区域偏移量/ID)

    

替换为多个"X"。

"Z"在java时代也有类似的含义。但是，Java 时间需要不同数量的文字来解析不同的形式。

考虑迁移到"X"，这样您就可以更好地控制时间的解析方式。例如，joda-time 格式 'YYYY-MM-dd'T'hh：mm：ssZZ' 接受以下日期：

    
    
    2010-01-01T01:02:03Z
    2010-01-01T01:02:03+01
    2010-01-01T01:02:03+01:02
    2010-01-01T01:02:03+01:02:03

在 java 时间中，您不能使用单一格式解析所有这些日期，而是必须指定 3 种单独的格式：

    
    
    2010-01-01T01:02:03Z
    2010-01-01T01:02:03+01
    both parsed with yyyy-MM-dd'T'hh:mm:ssX
    
    2010-01-01T01:02:03+01:02
    yyyy-MM-dd'T'hh:mm:ssXXX
    
    2010-01-01T01:02:03+01:02:03
    yyyy-MM-dd'T'hh:mm:ssXXXXX

然后必须使用"||`:

    
    
    yyyy-MM-dd'T'hh:mm:ssX||yyyy-MM-dd'T'hh:mm:ssXXX||yyyy-MM-dd'T'hh:mm:ssXXXXX

如果您希望模式在没有冒号 ('：') 的情况下出现，则同样适用：例如，'YYYY-MM-dd'T'hh：mm：ssZ' 格式接受以下日期格式：

    
    
    2010-01-01T01:02:03Z
    2010-01-01T01:02:03+01
    2010-01-01T01:02:03+0102
    2010-01-01T01:02:03+010203

要在 java 时间内接受所有这些形式，您必须使用 '||' 分隔符：

    
    
    yyyy-MM-dd'T'hh:mm:ssX||yyyy-MM-dd'T'hh:mm:ssXX||yyyy-MM-dd'T'hh:mm:ssXXXX

"d"(日)

    

在java时代，"d"仍然被解释为"day"，但不太灵活。

例如，joda 时间日期格式"YYYY-MM-dd"接受"2010-01-01"或"2010-01-1"。

在 java 时间，您必须使用 '||' 分隔符以提供指定每种格式：

    
    
    yyyy-MM-dd||yyyy-MM-d

在java时代，"d"也不接受超过2位数字。要接受超过两位数的日期，必须在 java 时间日期格式中包含文本文字。例如，要解析 '2010-01-00001'，必须使用以下 java 时间日期格式：

    
    
    yyyy-MM-'000'dd

"e"(日期名称)

    

在java时代，"e"仍然被解释为"日期名称"，但不解析短文本或全文形式。

例如，joda 时间日期格式"EEE YYYY-MM"同时接受"星期三2020-01"和"星期三 2020-01"。

要在 java 时间中接受这两个日期，必须使用"||' 分隔符：

    
    
    cccc yyyy-MM||ccc yyyy-MM

joda-time 字面"E"被解释为"星期几"。java-time文字"c"被解释为"本地化的星期几"。 "E"不接受全文日期格式，例如"星期三"。

"EEEE"和类似的文本表单

    

对全文表单的支持取决于随 Java 开发工具包 (JDK) 提供的区域设置数据和其他实现详细信息。我们建议您在升级之前仔细测试包含这些模式的格式。

"z"(时区文本)

    

在爪哇时间中，当给定 UTC 时区时，"z"输出祖鲁语的 _Z_。

### 使用您的数据进行测试

强烈建议您在生产中部署之前使用实际数据测试任何日期格式更改。

### 更新索引映射

若要更新索引映射中的 joda-time 日期格式，必须使用更新的映射创建一个新索引，并将数据重新索引到该索引。

以下"my-index-000001"索引包含"datetime"字段的映射，该字段是具有自定义 joda-time 日期格式的"date"字段。

    
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET my-index-000001/_mapping
    
    
    {
      "my-index-000001" : {
        "mappings" : {
          "properties" : {
             "datetime": {
               "type": "date",
               "format": "yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||epoch_millis"
             }
          }
        }
      }
    }

要更改"日期时间"字段的日期格式，请创建一个包含更新的映射和日期格式的单独索引。

例如，以下"my-index-000002"索引将"datetime"字段的日期格式更改为"uuuu/MM/dd HH：mm：ss||呜/呜�epoch_millis'。

    
    
    response = client.indices.create(
      index: 'my-index-000002',
      body: {
        mappings: {
          properties: {
            datetime: {
              type: 'date',
              format: 'uuuu/MM/dd HH:mm:ss||uuuu/MM/dd||epoch_millis'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000002
    {
      "mappings": {
        "properties": {
          "datetime": {
            "type": "date",
            "format": "uuuu/MM/dd HH:mm:ss||uuuu/MM/dd||epoch_millis"
          }
        }
      }
    }

接下来，将数据从旧索引重新索引到新索引。

以下重新索引 API 请求将数据从"my-index-000001"重新索引到"my-index-000002"。

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my-index-000001'
        },
        dest: {
          index: 'my-index-000002'
        }
      }
    )
    puts response
    
    
    POST _reindex
    {
      "source": {
        "index": "my-index-000001"
      },
      "dest": {
        "index": "my-index-000002"
      }
    }

如果使用索引别名，请更新它们以指向新索引。

    
    
    POST /_aliases
    {
      "actions" : [
        { "remove" : { "index" : "my-index-000001", "alias" : "my-index" } },
        { "add" : { "index" : "my-index-000002", "alias" : "my-index" } }
      ]
    }

[« Migrating to 8.0](migrating-8.0.md) [Transient settings migration guide
»](transient-settings-migration-guide.md)
