

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« Overview](sql-rest-overview.md) [Paginating through a large response
»](sql-pagination.md)

## 响应数据格式

虽然文本格式对人类来说很好，但计算机更喜欢结构化的东西。

Elasticsearch SQL可以返回以下格式的数据，可以通过URL中的"format"属性或设置"Accept"HTTP标头进行设置：

URL 参数优先于"接受"HTTP 标头。如果两者都未指定，则以与请求相同的格式返回响应。

**format**

|

**"接受"HTTP 标头**

|

**描述** ---|---|--- **人类可读** 'csv'

|

`text/csv`

|

逗号分隔值"json"

|

`application/json`

|

JSON(JavaScript Object Notation)人类可读格式'tsv'

|

`text/tab-separated-values`

|

制表符分隔值"txt"

|

`text/plain`

|

类似 CLI 的表示"yaml"

|

`application/yaml`

|

YAML (YAML Ain't Markup Language) 人类可读格式 **二进制格式** 'cbor'

|

`application/cbor`

|

简洁的二进制对象表示"微笑"

|

`application/smile`

|

微笑)类似于 CBOR 的二进制数据格式 "CSV"格式接受格式 URL 查询属性"分隔符"，该属性指示应使用哪个字符来分隔 CSV 值。它默认为逗号 ('，')，并且不能采用以下任何值：双引号 ('"')、回车符 ('\r') 和换行符 ('\n')。选项卡('\t')也不能使用，需要使用'tsv'格式。

以下是人类可读格式的一些示例：

###CSV

    
    
    response = client.sql.query(
      format: 'csv',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST /_sql?format=csv
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

返回：

    
    
    author,name,page_count,release_date
    Peter F. Hamilton,Pandora's Star,768,2004-03-02T00:00:00.000Z
    Vernor Vinge,A Fire Upon the Deep,613,1992-06-01T00:00:00.000Z
    Frank Herbert,Dune,604,1965-06-01T00:00:00.000Z
    Alastair Reynolds,Revelation Space,585,2000-03-15T00:00:00.000Z
    James S.A. Corey,Leviathan Wakes,561,2011-06-02T00:00:00.000Z

or:

    
    
    response = client.sql.query(
      format: 'csv',
      delimiter: ';',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST /_sql?format=csv&delimiter=%3b
    {
        "query": "SELECT * FROM library ORDER BY page_count DESC",
        "fetch_size": 5
    }

返回：

    
    
    author;name;page_count;release_date
    Peter F. Hamilton;Pandora's Star;768;2004-03-02T00:00:00.000Z
    Vernor Vinge;A Fire Upon the Deep;613;1992-06-01T00:00:00.000Z
    Frank Herbert;Dune;604;1965-06-01T00:00:00.000Z
    Alastair Reynolds;Revelation Space;585;2000-03-15T00:00:00.000Z
    James S.A. Corey;Leviathan Wakes;561;2011-06-02T00:00:00.000Z

###JSON

    
    
    response = client.sql.query(
      format: 'json',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST /_sql?format=json
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

其中返回：

    
    
    {
      "columns": [
        {"name": "author",       "type": "text"},
        {"name": "name",         "type": "text"},
        {"name": "page_count",   "type": "short"},
        {"name": "release_date", "type": "datetime"}
      ],
      "rows": [
        ["Peter F. Hamilton",  "Pandora's Star",       768, "2004-03-02T00:00:00.000Z"],
        ["Vernor Vinge",       "A Fire Upon the Deep", 613, "1992-06-01T00:00:00.000Z"],
        ["Frank Herbert",      "Dune",                 604, "1965-06-01T00:00:00.000Z"],
        ["Alastair Reynolds",  "Revelation Space",     585, "2000-03-15T00:00:00.000Z"],
        ["James S.A. Corey",   "Leviathan Wakes",      561, "2011-06-02T00:00:00.000Z"]
      ],
      "cursor": "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWWWdrRlVfSS1TbDYtcW9lc1FJNmlYdw==:BAFmBmF1dGhvcgFmBG5hbWUBZgpwYWdlX2NvdW50AWYMcmVsZWFzZV9kYXRl+v///w8="
    }

###TSV

    
    
    response = client.sql.query(
      format: 'tsv',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST /_sql?format=tsv
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

其中返回：

    
    
    author	name	page_count	release_date
    Peter F. Hamilton	Pandora's Star	768	2004-03-02T00:00:00.000Z
    Vernor Vinge	A Fire Upon the Deep	613	1992-06-01T00:00:00.000Z
    Frank Herbert	Dune	604	1965-06-01T00:00:00.000Z
    Alastair Reynolds	Revelation Space	585	2000-03-15T00:00:00.000Z
    James S.A. Corey	Leviathan Wakes	561	2011-06-02T00:00:00.000Z

###TXT

    
    
    response = client.sql.query(
      format: 'txt',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST /_sql?format=txt
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

其中返回：

    
    
         author      |        name        |  page_count   |      release_date
    -----------------+--------------------+---------------+------------------------
    Peter F. Hamilton|Pandora's Star      |768            |2004-03-02T00:00:00.000Z
    Vernor Vinge     |A Fire Upon the Deep|613            |1992-06-01T00:00:00.000Z
    Frank Herbert    |Dune                |604            |1965-06-01T00:00:00.000Z
    Alastair Reynolds|Revelation Space    |585            |2000-03-15T00:00:00.000Z
    James S.A. Corey |Leviathan Wakes     |561            |2011-06-02T00:00:00.000Z

###YAML

    
    
    response = client.sql.query(
      format: 'yaml',
      body: {
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST /_sql?format=yaml
    {
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

其中返回：

    
    
    columns:
    - name: "author"
      type: "text"
    - name: "name"
      type: "text"
    - name: "page_count"
      type: "short"
    - name: "release_date"
      type: "datetime"
    rows:
    - - "Peter F. Hamilton"
      - "Pandora's Star"
      - 768
      - "2004-03-02T00:00:00.000Z"
    - - "Vernor Vinge"
      - "A Fire Upon the Deep"
      - 613
      - "1992-06-01T00:00:00.000Z"
    - - "Frank Herbert"
      - "Dune"
      - 604
      - "1965-06-01T00:00:00.000Z"
    - - "Alastair Reynolds"
      - "Revelation Space"
      - 585
      - "2000-03-15T00:00:00.000Z"
    - - "James S.A. Corey"
      - "Leviathan Wakes"
      - 561
      - "2011-06-02T00:00:00.000Z"
    cursor: "sDXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAAEWWWdrRlVfSS1TbDYtcW9lc1FJNmlYdw==:BAFmBmF1dGhvcgFmBG5hbWUBZgpwYWdlX2NvdW50AWYMcmVsZWFzZV9kYXRl+v///w8="

[« Overview](sql-rest-overview.md) [Paginating through a large response
»](sql-pagination.md)
