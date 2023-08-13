

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« Post Event to an Analytics Collection](post-analytics-collection-
event.md) [cat aliases API »](cat-alias.md)

## 压缩和对齐文本 (CAT)API

###Introduction

JSON很棒...对于计算机。即使打印得很漂亮，尝试在数据中查找关系也很乏味。人的眼睛，尤其是在看终端时，需要紧凑和对齐的文本。紧凑和对齐文本 (CAT)API 旨在满足这一需求。

cat API 仅供人类使用 Kibanaconsole 或命令行使用。它们are_not_供应用程序使用。对于应用程序使用，我们建议使用相应的 JSON API。

所有 cat 命令都接受查询字符串参数 'help' 以查看它们提供的所有标头和信息，并且 '/_cat' 命令单独列出所有可用命令。

### 常用参数

####Verbose

每个命令都接受查询字符串参数"v"以打开详细输出。例如：

    
    
    response = client.cat.master(
      v: true
    )
    puts response
    
    
    GET _cat/master?v=true

可能会回复：

    
    
    id                     host      ip        node
    u_n93zwxThWHi1PDBJAGAg 127.0.0.1 127.0.0.1 u_n93zw

####Help

每个命令都接受一个查询字符串参数"help"，该参数将输出其可用列。例如：

    
    
    response = client.cat.master(
      help: true
    )
    puts response
    
    
    GET _cat/master?help

可能会回复：

    
    
    id   |   | node id
    host | h | host name
    ip   |   | ip address
    node | n | node name

如果使用任何可选的 URL 参数，则不支持"帮助"。例如，'GET _cat/shards/my-index-000001？help' 或 'GET _cat/indices/my-index-*？help'会导致错误。改用"GET _cat/shards？help"或"GET _cat/indexs？help"。

####Headers

每个命令都接受一个查询字符串参数"h"，该参数仅强制显示这些列。例如：

    
    
    response = client.cat.nodes(
      h: 'ip,port,heapPercent,name'
    )
    puts response
    
    
    GET _cat/nodes?h=ip,port,heapPercent,name

响应：

    
    
    127.0.0.1 9300 27 sLBaIGK

您还可以使用简单的通配符(如'/_cat/thread_pool？h=ip，queue*')请求多个列，以获取以"queue"开头的所有标头(或别名)。

#### 数字格式

许多命令提供几种类型的数字输出，可以是字节、大小或时间值。默认情况下，这些类型是人工格式化的，例如，"3.5mb"而不是"3763212"。人类值无法按数字排序，因此为了在顺序很重要的情况下对这些值进行操作，您可以更改它。

假设您要查找集群中最大的索引(所有分片使用的存储，而不是文档数)。"/_cat/索引"API 是理想的。您只需要在 API 请求中添加三件事：

1. 值为"b"的"bytes"查询字符串参数，用于获取字节级分辨率。  2. 值为"store.size：desc"的"s"(排序)参数和带有"index：asc"的逗号，用于按分片存储降序对输出进行排序，然后按升序对索引名称进行排序。  3. "v"(详细)参数，用于在响应中包含列标题。

    
    
    response = client.cat.indices(
      bytes: 'b',
      s: 'store.size:desc,index:asc',
      v: true
    )
    puts response
    
    
    GET _cat/indices?bytes=b&s=store.size:desc,index:asc&v=true

API 返回以下响应：

    
    
    health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   my-index-000001  u8FNjxh8Rfy_awN11oDKYQ   1   1       1200            0      72171         72171
    green  open   my-index-000002  nYFWZEO7TUiOjLQXBaYJpA   1   0          0            0        230          230

如果要更改时间单位，请使用"time"参数。

如果要更改大小单位，请使用"size"参数。

如果要更改字节单位，请使用"bytes"参数。

#### 响应为文本、json、微笑、yaml orcbor

    
    
    % curl 'localhost:9200/_cat/indices?format=json&pretty'
    [
      {
        "pri.store.size": "650b",
        "health": "yellow",
        "status": "open",
        "index": "my-index-000001",
        "pri": "5",
        "rep": "1",
        "docs.count": "0",
        "docs.deleted": "0",
        "store.size": "650b"
      }
    ]

当前支持的格式(对于"？format="参数)：\- 文本(默认)\- json \- 微笑 \- yaml \- cbor

或者，您可以将"接受"HTTP 标头设置为适当的媒体格式。支持上述所有格式，GET 参数优先于标头。例如：

    
    
    % curl '192.168.56.10:9200/_cat/indices?pretty' -H "Accept: application/json"
    [
      {
        "pri.store.size": "650b",
        "health": "yellow",
        "status": "open",
        "index": "my-index-000001",
        "pri": "5",
        "rep": "1",
        "docs.count": "0",
        "docs.deleted": "0",
        "store.size": "650b"
      }
    ]

####Sort

每个命令都接受一个查询字符串参数"s"，该参数按指定为参数值的列对表进行排序。列按名称或别名指定，并以逗号分隔的字符串形式提供。默认情况下，排序按升序完成。将":d esc"追加到列将反转该列的顺序。"：ASC"也被接受，但表现出与默认排序顺序相同的行为。

例如，对于排序字符串 's=column1，column2：desc，column3'，表将按列 1 升序排序，按列 2 降序排序，按升序按列 3 排序。

    
    
    response = client.cat.templates(
      v: true,
      s: 'order:desc,index_patterns'
    )
    puts response
    
    
    GET _cat/templates?v=true&s=order:desc,index_patterns

returns:

    
    
    name                  index_patterns order version
    pizza_pepperoni       [*pepperoni*]  2
    sushi_california_roll [*avocado*]    1     1
    pizza_hawaiian        [*pineapples*] 1

[« Post Event to an Analytics Collection](post-analytics-collection-
event.md) [cat aliases API »](cat-alias.md)
