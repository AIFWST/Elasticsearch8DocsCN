

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md)

[« Grokking grok](grok.md) [Common scripting use cases »](common-script-
uses.md)

## 使用"字段"API 访问文档中的字段

"字段"API 仍在开发中，应被视为测试版功能。API 可能会发生变化，此迭代可能不是最终状态。有关功能状态，请参阅#78920。

使用"字段"API 访问文档字段：

    
    
    field('my_field').get(<default_value>)

此 API 从根本上改变了您在 Painless 中访问文档的方式。以前，您必须使用要访问的字段名称访问"doc"映射：

    
    
    doc['my_field'].value

以这种方式访问文档字段不会处理缺失值或缺失映射，这意味着要编写健壮的 Painless 脚本，您需要包含逻辑来检查字段和值是否存在。

相反，请使用"字段"API，这是在Painless中访问文档的首选方法。"字段"API 处理缺失值，并将演变为对"_source"和"doc_values"的抽象访问。

某些字段尚不与"字段"API 兼容，例如"文本"或"地理"字段。继续使用"doc"访问"字段"API 不支持的字段类型。

"field"API 返回一个"Field"对象，该对象循环访问具有多个值的字段，通过"get(<default_value>)"方法以及类型转换和帮助程序方法提供对基础值的访问。

"字段"API 返回您指定的默认值，无论该字段是否存在或是否具有当前文档的任何值。这意味着"字段"API 可以处理缺失值，而无需额外的逻辑。对于引用类型(如"关键字")，默认值可以是"null"。对于基元类型(如"布尔值"或"长整型")，默认值必须是匹配的基元类型，如"false"或"1"。

### 方便，更简单

您可以包含"$"快捷方式，而不是使用 'get()' 方法显式调用 'field' API。只需包含"$"符号、字段名称和默认值，以防字段没有值：

    
    
    $(‘field’, <default_value>)

借助这些增强的功能和简化的语法，您可以编写更短、更简单且更易于阅读的脚本。例如，以下脚本使用过时的语法来确定索引文档中两个复杂的"datetime"值之间的差异(以毫秒为单位)：

    
    
    if (doc.containsKey('start') && doc.containsKey('end')) {
       if (doc['start'].size() > 0 && doc['end'].size() > 0) {
           ZonedDateTime start = doc['start'].value;
           ZonedDateTime end = doc['end'].value;
           return ChronoUnit.MILLIS.between(start, end);
       } else {
           return -1;
       }
    } else {
       return -1;
    }

使用 'field' API，您可以更简洁地编写相同的脚本，而无需在对字段进行操作之前需要额外的逻辑来确定字段是否存在：

    
    
    ZonedDateTime start = field('start').get(null);
    ZonedDateTime end = field('end').get(null);
    return start == null || end == null ? -1 : ChronoUnit.MILLIS.between(start, end)

### 支持的映射字段类型

下表指示了"字段"API 支持的映射字段类型。对于每种受支持的类型，都会列出由"字段"API(来自"get"和"as"<Type>方法)和"doc"映射(来自"getValue"和"get"方法)返回的值。

"字段"API 目前不支持某些字段，但您仍可以通过"doc"映射访问这些字段。有关支持字段的最新列表，请参阅#79105。

映射字段类型 |从"字段"返回的类型 |从"doc"返回的类型 ---|---|--- |

**`get`**

|

**`as<Type>`**

|

**`getValue`**

|

**'获取'**'二进制'

|

`ByteBuffer`

|

-

|

`BytesRef`

|

'BytesRef' 'boolean'

|

`boolean`

|

-

|

`boolean`

|

"布尔""关键字"

|

`String`

|

-

|

`String`

|

"字符串""长"

|

`long`

|

-

|

`long`

|

"长""整数"

|

`int`

|

-

|

`long`

|

"长""短"

|

`short`

|

-

|

`long`

|

"长""字节"

|

`byte`

|

-

|

`long`

|

"长""双"

|

`double`

|

-

|

`double`

|

"双" "scaled_float"

|

`double`

|

-

|

`double`

|

"双" "half_float"

|

`float`

|

-

|

`double`

|

"双" "unsigned_long"

|

`long`

|

`BigInteger`

|

`long`

|

"长""日期"

|

`ZonedDateTime`

|

-

|

`ZonedDateTime`

|

"分区日期时间" "date_nanos"

|

`ZonedDateTime`

|

-

|

`ZonedDateTime`

|

"分区日期时间" "ip"

|

`IpAddress`

|

`String`

|

`String`

|

"字符串" "_version"

|

`long`

|

-

|

`long`

|

"长""_seq_no"

|

`long`

|

-

|

`long`

|

"长""版本"

|

`Version`

|

`String`

|

`String`

|

"弦""杂音3"

|

`long`

|

-

|

`long`

|

"长""constant_keyword"

|

`String`

|

-

|

`String`

|

"字符串""通配符"

|

`String`

|

-

|

`String`

|

"字符串""扁平"

|

`String`

|

-

|

`String`

|

'字符串' « Grokking grok 常见脚本用例 »