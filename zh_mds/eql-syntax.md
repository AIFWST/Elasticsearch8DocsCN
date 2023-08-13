

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[EQL
search](eql.md)

[« EQL search](eql.md) [EQL function reference »](eql-function-ref.md)

## EQL 语法参考

### 基本语法

EQL 查询需要事件类别和匹配条件。"where"关键字将它们连接起来。

    
    
    event_category where condition

事件类别是事件类别字段的索引值。默认情况下，EQLsearch API 使用 Elastic Common Schema (ECS) 中的 'event.category' 字段。您可以使用 API 的"event_category_field"参数指定另一个事件类别字段。

例如，以下 EQL 查询匹配事件类别为"进程"和"process.name"为"svchost.exe"的事件：

    
    
    process where process.name == "svchost.exe"

#### 匹配任何事件类别

要匹配任何类别的事件，请使用"任意"关键字。您还可以使用"any"关键字搜索没有事件类别字段的文档。

例如，以下 EQL 查询匹配字段值为"http"的任何文档：

    
    
    any where network.protocol == "http"

#### 转义事件类别

使用括起来的双引号 ('"') 或三个括起来的双引号 ('"""'') 来转义以下事件类别：

* 包含特殊字符，如连字符 ('-') 或点 ('.') * 包含一个空格 * 以数字开头

    
    
    ".my.event.category"
    "my-event-category"
    "my event category"
    "6eventcategory"
    
    """.my.event.category"""
    """my-event-category"""
    """my event category"""
    """6eventcategory"""

#### 转义字段名称

使用括起来的反引号 (') 转义以下字段名称：

* 包含连字符 ('-') * 包含空格 * 以数字开头

    
    
    `my-field`
    `my field`
    `6myfield`

使用双反引号 ('') 转义字段名称中的任何反引号 (')。

    
    
    my`field -> `my``field`

###Conditions

条件由事件必须匹配的一个或多个条件组成。您可以使用以下运算符指定和组合这些条件。默认情况下，大多数 EQL 运算符都区分大小写。

#### 比较运算符

    
    
    <   <=   ==   :   !=   >=   >

"<"(小于)

     Returns `true` if the value to the left of the operator is less than the value to the right. Otherwise returns `false`. 
`<=` (less than or equal)

     Returns `true` if the value to the left of the operator is less than or equal to the value to the right. Otherwise returns `false`. 
`==` (equal, case-sensitive)

     Returns `true` if the values to the left and right of the operator are equal. Otherwise returns `false`. Wildcards are not supported. 
`:` (equal, case-insensitive)

     Returns `true` if strings to the left and right of the operator are equal. Otherwise returns `false`. Can only be used to compare strings. Supports [wildcards](eql-syntax.html#eql-syntax-wildcards "Wildcards") and [list lookups](eql-syntax.html#eql-syntax-lookup-operators "Lookup operators"). 
`!=` (not equal, case-sensitive)

     Returns `true` if the values to the left and right of the operator are not equal. Otherwise returns `false`. Wildcards are not supported. 
`>=` (greater than or equal)

     Returns `true` if the value to the left of the operator is greater than or equal to the value to the right. Otherwise returns `false`. When comparing strings, the operator uses a case-sensitive lexicographic order. 
`>` (greater than)

     Returns `true` if the value to the left of the operator is greater than the value to the right. Otherwise returns `false`. When comparing strings, the operator uses a case-sensitive lexicographic order. 

不支持将"="作为相等运算符。请改用"=="或"："。

#### 模式比较关键字

    
    
    my_field like  "VALUE*"         // case-sensitive wildcard matching
    my_field like~ "value*"         // case-insensitive wildcard matching
    
    my_field regex  "VALUE[^Z].?"   // case-sensitive regex matching
    my_field regex~ "value[^z].?"   // case-insensitive regex matching

"like"(区分大小写)

     Returns `true` if the string to the left of the keyword matches a [wildcard pattern](eql-syntax.html#eql-syntax-wildcards "Wildcards") to the right. Supports [list lookups](eql-syntax.html#eql-syntax-lookup-operators "Lookup operators"). Can only be used to compare strings. For case-insensitive matching, use `like~`. 
`regex` (case-sensitive)

     Returns `true` if the string to the left of the keyword matches a regular expression to the right. For supported regular expression syntax, see [_Regular expression syntax_](regexp-syntax.html "Regular expression syntax"). Supports [list lookups](eql-syntax.html#eql-syntax-lookup-operators "Lookup operators"). Can only be used to compare strings. For case-insensitive matching, use `regex~`. 

##### 比较的限制

您不能进行连锁比较。相反，请在比较之间使用逻辑运算符。例如，不支持"foo < bar <= baz"。但是，您可以将表达式重写为"foo < bar and bar <= baz"，这是受支持的。

您也无法将一个字段与另一个字段进行比较，即使使用函数更改了字段也是如此。

**示例** 以下 EQL 查询将"process.parent_name"字段值与非静态值"foo"进行比较。支持此比较。

但是，查询还会将"process.parent.name"字段值与"process.name"字段进行比较。不支持此比较，并且将返回整个查询的错误。

    
    
    process where process.parent.name == "foo" and process.parent.name == process.name

相反，您可以重写查询以将"process.parent.name"和"process.name"字段与静态值进行比较。

    
    
    process where process.parent.name == "foo" and process.name == "foo"

#### 逻辑运算符

    
    
    and  or  not

`and`

     Returns `true` only if the condition to the left and right _both_ return `true`. Otherwise returns `false`. 
`or`

     Returns `true` if one of the conditions to the left or right `true`. Otherwise returns `false`. 
`not`

     Returns `true` if the condition to the right is `false`. 

#### 查找运算符

    
    
    my_field in ("Value-1", "VALUE2", "VAL3")                 // case-sensitive
    my_field in~ ("value-1", "value2", "val3")                // case-insensitive
    
    my_field not in ("Value-1", "VALUE2", "VAL3")             // case-sensitive
    my_field not in~ ("value-1", "value2", "val3")            // case-insensitive
    
    my_field : ("value-1", "value2", "val3")                  // case-insensitive
    
    my_field like  ("Value-*", "VALUE2", "VAL?")              // case-sensitive
    my_field like~ ("value-*", "value2", "val?")              // case-insensitive
    
    my_field regex  ("[vV]alue-[0-9]", "VALUE[^2].?", "VAL3") // case-sensitive
    my_field regex~  ("value-[0-9]", "value[^2].?", "val3")   // case-sensitive

"in"(区分大小写)

     Returns `true` if the value is contained in the provided list. For case-insensitive matching, use `in~`. 
`not in` (case-sensitive)

     Returns `true` if the value is not contained in the provided list. For case-insensitive matching, use `not in~`. 
`:` (case-insensitive)

     Returns `true` if the string is contained in the provided list. Can only be used to compare strings. 
`like` (case-sensitive)

     Returns `true` if the string matches a [wildcard pattern](eql-syntax.html#eql-syntax-wildcards "Wildcards") in the provided list. Can only be used to compare strings. For case-insensitive matching, use `like~`. 
`regex` (case-sensitive)

     Returns `true` if the string matches a regular expression pattern in the provided list. For supported regular expression syntax, see [_Regular expression syntax_](regexp-syntax.html "Regular expression syntax"). Can only be used to compare strings. For case-insensitive matching, use `regex~`. 

#### 数学运算符

    
    
    +  -  *  /  %

"+"(添加)

     Adds the values to the left and right of the operator. 
`-` (subtract)

     Subtracts the value to the right of the operator from the value to the left. 
`*` (multiply)

     Multiplies the values to the left and right of the operator. 
`/` (divide)

    

将运算符左侧的值除以右侧的值。

如果除数和除数都是整数，则除法 ('\') 会将任何返回的浮点数operation_rounds down_为最接近的整数。为避免四舍五入，请将股息或除数转换为浮动。

**示例** "process.args_count"字段是包含进程参数计数的"长"整数字段。

用户可能希望以下 EQL 查询仅匹配值为"4"process.args_count"的事件。

    
    
    process where ( 4 / process.args_count ) == 1

但是，EQL 查询匹配"process.args_count"值为"3"或"4"的事件。

对于"process.args_count"值为"3"的事件，除法运算返回浮点数"1.333..."，该浮点数向下舍入为"1"。

要仅匹配"process.args_count"值为"4"的事件，请将除数或除数转换为浮动值。

以下 EQL 查询将整数"4"更改为等效的浮点数"4.0"。

    
    
    process where ( 4.0 / process.args_count ) == 1

"%"(模数)

     Divides the value to the left of the operator by the value to the right. Returns only the remainder. 

#### 匹配任何条件

要仅按事件类别匹配事件，请使用"如果为 true"条件。

例如，以下 EQL 查询匹配任何"文件"事件：

    
    
    file where true

要匹配任何事件，您可以将"any"关键字与"where true"条件结合使用：

    
    
    any where true

### 可选字段

默认情况下，EQL 查询只能包含您正在搜索的数据集中存在的字段。如果字段具有显式、动态或运行时映射，则数据集中存在该字段。如果 EQL 查询包含不存在的字段，则会返回错误。

如果不确定数据集中是否存在字段，请使用"？"运算符将该字段标记为可选。如果可选字段不存在，查询会将其替换为"null"，而不是返回错误。

**示例** 在以下查询中，"user.id"字段是可选的。

    
    
    network where ?user.id != null

如果要搜索的数据集中存在"user.id"字段，则查询将匹配包含"user.id"值的任何"网络"事件。如果数据集中不存在"user.id"字段，EQL 会将查询解释为：

    
    
    network where null != null

在这种情况下，查询与任何事件都不匹配。

#### 检查字段是否存在

要匹配包含字段任何值的事件，请使用"！="运算符将该字段与"null"进行比较：

    
    
    ?my_field != null

要匹配不包含字段值的事件，请使用"=="运算符将字段与"null"进行比较：

    
    
    ?my_field == null

###Strings

字符串括在双引号 ('"') 中。

    
    
    "hello world"

不支持用单引号 (''') 括起来的字符串。

#### 字符串中的转义字符

在字符串中使用特殊字符(如回车符或双引号 ('"'))必须使用前面的反斜杠 ('\') 进行转义。

    
    
    "example \r of \" escaped \n characters"

转义序列 |文字字符 ---|--- '\n'

|

换行符(换行)'\r'

|

回车符 '\t'

|

选项卡"\\"

|

反斜杠 ('\') '\''

|

双引号 ('"') 可以使用十六进制 '\u{XXXXXXXX}' 转义序列对 Unicode 字符进行转义。十六进制值可以是 2-8 个字符，并且不区分大小写。少于 8 个字符的值以零填充。您可以使用这些转义序列在转义序列中包含不可打印或从右到左 (RTL) 字符。例如，您可以将从右到左的标记 (RLM) 转义为"\u{200f}"、"\u{200F}"或"\u{0000200f}"。

单引号 (''') 字符保留供将来使用。不能对文本字符串使用转义单引号 ('\'')。请改用转义的双引号 ('\"')。

#### 原始字符串

原始字符串将特殊字符(如反斜杠 ('\'))视为文字字符。原始字符串括在三个双引号 ('"""') 中。

    
    
    """Raw string with a literal double quote " and blackslash \ included"""

原始字符串不能包含三个连续的双引号 ('""""')。请改用带有"\""转义序列的常规字符串。

    
    
    "String containing \"\"\" three double quotes"

####Wildcards

对于使用"："运算符或"like"关键字的字符串比较，可以使用"*"和"？"通配符来匹配特定模式。"*"通配符匹配零个或多个字符：

    
    
    my_field : "doc*"     // Matches "doc", "docs", or "document" but not "DOS"
    my_field : "*doc"     // Matches "adoc" or "asciidoc"
    my_field : "d*c"      // Matches "doc" or "disc"
    
    my_field like "DOC*"  // Matches "DOC", "DOCS", "DOCs", or "DOCUMENT" but not "DOS"
    my_field like "D*C"   // Matches "DOC", "DISC", or "DisC"

"？"通配符只匹配一个字符：

    
    
    my_field : "doc?"     // Matches "docs" but not "doc", "document", or "DOS"
    my_field : "?doc"     // Matches "adoc" but not "asciidoc"
    my_field : "d?c"      // Matches "doc" but not "disc"
    
    my_field like "DOC?"  // Matches "DOCS" or "DOCs" but not "DOC", "DOCUMENT", or "DOS"
    my_field like "D?c"   // Matches "DOC" but not "DISC"

"："运算符和"like"关键字也支持列表查找中的通配符：

    
    
    my_field : ("doc*", "f*o", "ba?", "qux")
    my_field like ("Doc*", "F*O", "BA?", "QUX")

###Sequences

您可以使用 EQL 序列来描述和匹配有序的一系列事件。序列中的每个项目都是一个事件类别和事件条件，用方括号 ('[ ]') 括起来。事件按时间升序列出，最近的事件列在最后。

    
    
    sequence
      [ event_category_1 where condition_1 ]
      [ event_category_2 where condition_2 ]
      ...

**示例** 以下 EQL 序列查询与这一系列有序事件匹配：

1. 从以下事件开始：

    * An event category of `file`
    * A `file.extension` of `exe`

2. 后跟事件类别为"流程"的事件

    
    
    sequence
      [ file where file.extension == "exe" ]
      [ process where true ]

#### 'with maxspan'语句

您可以使用"与最大跨度"将序列限制为指定的时间跨度。匹配序列中的所有事件都必须在此持续时间内发生，从第一个事件的时间戳开始。

'maxspan' 接受时间值参数。

    
    
    sequence with maxspan=30s
      [ event_category_1 where condition_1 ] by field_baz
      [ event_category_2 where condition_2 ] by field_bar
      ...

**示例** 以下序列查询使用"maxspan"值"15m"(15 分钟)。匹配序列中的事件必须在第一个事件的时间戳的 15 分钟内发生。

    
    
    sequence with maxspan=15m
      [ file where file.extension == "exe" ]
      [ process where true ]

#### 'by'关键字

在序列查询中使用"by"关键字仅匹配共享相同值的事件，即使这些值位于不同的字段中也是如此。这些共享值称为联接键。如果联接键在所有事件中应位于同一字段中，请使用"序列依据"。

    
    
    sequence by field_foo
      [ event_category_1 where condition_1 ] by field_baz
      [ event_category_2 where condition_2 ] by field_bar
      ...

**示例** 以下序列查询使用"by"关键字将匹配事件约束为：

* 具有相同"user.name"值的事件 * "file.path"值等于以下"进程"事件的"进程.可执行文件"值的"文件"事件。

    
    
    sequence
      [ file where file.extension == "exe" ] by user.name, file.path
      [ process where true ] by user.name, process.executable

由于"user.name"字段在序列中的所有事件之间共享，因此可以使用"序列依据"将其包含在内。以下序列等效于前一个序列。

    
    
    sequence by user.name
      [ file where file.extension == "exe" ] by file.path
      [ process where true ] by process.executable

您可以组合"序列依据"和"与最大跨度"，以按字段值和时间跨度约束序列。

    
    
    sequence by field_foo with maxspan=30s
      [ event_category_1 where condition_1 ]
      [ event_category_2 where condition_2 ]
      ...

**示例** 以下序列查询使用"sequence by"和"with maxspan"来仅匹配以下事件序列：

* 共享相同的"user.name"字段值 * 在第一个匹配事件的"15m"(15 分钟)内发生

    
    
    sequence by user.name with maxspan=15m
      [ file where file.extension == "exe" ]
      [ process where true ]

#### 可选的"by"字段

默认情况下，联接键必须是非"空"字段值。要允许"null"连接键，请使用"？"运算符将"by"字段标记为可选。如果您不确定要搜索的数据集是否包含"by"字段，这也很有用。

**示例** 以下序列查询使用"序列依据"将匹配事件约束为：

* 具有相同"process.pid"值的事件，不包括"空"值。如果正在搜索的数据集中不存在"process.pid"字段，则查询将返回错误。  * 具有相同"process.entity_id"值的事件，包括"空"值。如果事件不包含"process.entity_id"字段，则其"process.entity_id"值被视为"null"。即使您要搜索的数据集中不存在"process.pid"字段，这也适用。

    
    
    sequence by process.pid, ?process.entity_id
      [process where process.name == "regsvr32.exe"]
      [network where true]

#### 'until'关键字

您可以使用"until"关键字指定序列的过期事件。如果此过期事件发生在序列中的匹配事件之间，则该序列将过期，不被视为匹配。如果过期事件occurs_after_序列中的匹配事件，则该序列仍被视为匹配。过期事件不包括在结果中。

    
    
    sequence
      [ event_category_1 where condition_1 ]
      [ event_category_2 where condition_2 ]
      ...
    until [ event_category_3 where condition_3 ]

**示例** 数据集包含以下事件序列，按共享 ID 分组：

    
    
    A, B
    A, B, C
    A, C, B

以下 EQL 查询在数据集中搜索包含事件"A"后跟事件"B"的序列。事件"C"用作过期事件。

    
    
    sequence by ID
      A
      B
    until C

查询匹配序列"A，B"和"A，B，C"，但不匹配"A，C，B"。

在 Windows 事件日志中搜索进程序列时，"until"关键字非常有用。

在 Windows 中，进程 ID (PID) 仅在进程运行时是唯一的。进程终止后，可以重用其 PID。

您可以使用"by"和"sequence by"关键字搜索具有相同 PID 值的事件序列。

**示例** 以下 EQL 查询使用"sequence by"关键字来匹配共享相同"process.pid"值的事件序列。

    
    
    sequence by process.pid
      [ process where event.type == "start" and process.name == "cmd.exe" ]
      [ process where file.extension == "exe" ]

但是，由于 PID 重用，这可能会导致匹配序列包含跨不相关进程的事件。为了防止误报，可以使用"until"关键字在进程终止事件之前结束匹配序列。

以下 EQL 查询使用"until"关键字在"处理"事件之前结束序列，"event.type"为"stop"。这些事件表示进程已终止。

    
    
    sequence by process.pid
      [ process where event.type == "start" and process.name == "cmd.exe" ]
      [ process where file.extension == "exe" ]
    until [ process where event.type == "stop" ]

#### 'with runs'语句

使用"with runs"语句在序列查询中连续运行相同的事件条件。例如：

    
    
    sequence
      [ process where event.type == "creation" ]
      [ library where process.name == "regsvr32.exe" ] with runs=3
      [ registry where true ]

相当于：

    
    
    sequence
      [ process where event.type == "creation" ]
      [ library where process.name == "regsvr32.exe" ]
      [ library where process.name == "regsvr32.exe" ]
      [ library where process.name == "regsvr32.exe" ]
      [ registry where true ]

"runs"值必须介于"1"和"100"(含)之间。

您可以将"with runs"语句与"by"关键字一起使用。例如：

    
    
    sequence
      [ process where event.type == "creation" ] by process.executable
      [ library where process.name == "regsvr32.exe" ] by dll.path with runs=3

###Samples

您可以使用 EQL 示例来描述和匹配按时间顺序排列的一系列无序事件。对于使用"by"关键字(联接键)指定的一个或多个字段，示例中的所有事件共享相同的值。样本中的每个项目都是一个事件类别和事件条件，用方括号 ('[ ]') 括起来。事件按其匹配的筛选器顺序列出。

    
    
    sample by join_key
      [ event_category_1 where condition_1 ]
      [ event_category_2 where condition_2 ]
      ...

**示例** 以下 EQL 示例查询最多返回 10 个具有"host"唯一值的示例。每个示例包含两个事件：

1. 从以下事件开始：

    * An event category of `file`
    * A `file.extension` of `exe`

2. 后跟事件类别为"流程"的事件

    
    
    sample by host
      [ file where file.extension == "exe" ]
      [ process where true ]

示例查询不考虑事件的时间顺序。不支持"with maxspan"和"with runs"语句以及"until"关键字。

###Functions

您可以使用 EQL 函数转换数据类型、执行数学运算、操作字符串等。有关支持的函数的列表，请参阅 _函数引用_。

#### 不区分大小写的函数

默认情况下，大多数 EQL 函数都区分大小写。要使函数不区分大小写，请在函数名称后使用"~"运算符：

    
    
    stringContains(process.name,".exe")  // Matches ".exe" but not ".EXE" or ".Exe"
    stringContains~(process.name,".exe") // Matches ".exe", ".EXE", or ".Exe"

#### 函数如何影响搜索性能

在 EQL 查询中使用函数可能会导致搜索速度变慢。如果您经常使用函数来转换索引数据，则可以通过在索引期间进行这些更改来加快搜索速度。但是，这通常意味着较慢的索引速度。

**示例** 索引包含"file.path"字段。"file.path"包含文件的完整路径，包括文件扩展名。

运行 EQL 搜索时，用户经常使用带有"file.path"字段的"endsWith"函数来匹配文件扩展名：

    
    
    file where endsWith(file.path,".exe") or endsWith(file.path,".dll")

虽然这有效，但编写起来可能会重复，并且会降低搜索速度。为了加快搜索速度，您可以改为执行以下操作：

1. 在索引中添加一个新字段"file.extension"。"file.extension"字段将仅包含"file.path"字段中的文件扩展名。  2. 在编制索引之前，使用包含"grok"处理器或其他预处理器工具的摄取管道从"file.path"字段中提取文件扩展名。  3. 将提取的文件扩展名索引到"file.extension"字段。

这些更改可能会减慢索引编制速度，但可以加快搜索速度。用户可以使用"file.extension"字段而不是多个"endsWith"函数调用：

    
    
    file where file.extension in ("exe", "dll")

我们建议在将任何索引更改部署到生产环境之前对其进行测试和基准测试。有关索引speed_，请参阅_Tune，有关搜索speed_，请参阅_Tune。

###Pipes

EQL 管道过滤、聚合和后处理 EQL 查询返回的事件。您可以使用管道来缩小 EQL 查询结果的范围或使其更具体。

管道使用竖线 ('|') 字符分隔。

    
    
    event_category where condition | pipe

**示例** 以下 EQL 查询使用"尾"管道仅返回与查询匹配的 10 个最新事件。

    
    
    authentication where agent.id == 4624
    | tail 10

可以将一个管道的输出传递到另一个管道。这允许您将多个管道与单个查询一起使用。

有关支持的管道的列表，请参阅 _Pipe reference_。

###Limitations

EQL 具有以下限制。

#### EQL 使用"字段"参数

EQL 使用搜索 API 的"字段"参数检索字段值。对"字段"参数的任何限制也适用于 EQL 查询。例如，如果对任何返回的字段或在索引级别禁用了"_source"，则无法检索值。

#### 比较字段

不能使用 EQL 比较运算符将一个字段与另一个字段进行比较。即使使用函数更改字段，这也适用。

不支持 #### 文本字段

EQL 搜索不支持"文本"字段。Toa搜索"文本"字段，使用EQL搜索API的查询DSL'filter'参数。

#### 嵌套字段上的 EQL 搜索

不能使用 EQL 搜索"嵌套"字段的值或"嵌套"字段的子字段。但是，支持包含"嵌套"字段映射的数据流和索引。

#### 与残局均衡器语法的区别

Elasticsearch EQL 与 Elastic Endgame EQL语法的不同之处如下：

* 在 Elasticsearch EQL 中，大多数运算符都区分大小写。例如，'process_name == "cmd.exe"不等同于'process_name == "Cmd.exe"'。  * 在 Elasticsearch EQL 中，函数区分大小写。要使函数不区分大小写，请使用"~"，例如"endsWith~(process_name，".exe")"。  * 对于不区分大小写的相等比较，请使用"："运算符。"*"和"？"都是可识别的通配符。  * "=="和"！="运算符不扩展通配符。例如，'process_name == "cmd*.exe"' 将"*"解释为文字星号，而不是通配符。  * 对于通配符匹配，区分大小写时使用"like"关键字，不区分大小写时使用"like~"。"："运算符等效于"like~"。  * 对于正则表达式匹配，请使用"正则表达式"或"正则表达式~"。  * "="不能代替"=="运算符。  * 不支持用单引号 (''') 括起来的字符串。改为将字符串括在双引号 ('"') 中。  * `?"'和'？' 不指示原始字符串。改为将原始字符串括在三个双引号 ('"""') 中。  * Elasticsearch EQL 不支持：

    * Array functions:

      * [`arrayContains`](https://eql.readthedocs.io/en/latest/query-guide/functions.html#arrayContains)
      * [`arrayCount`](https://eql.readthedocs.io/en/latest/query-guide/functions.html#arrayCount)
      * [`arraySearch`](https://eql.readthedocs.io/en/latest/query-guide/functions.html#arraySearch)

    * The [`match`](https://eql.readthedocs.io/en/latest/query-guide//functions.html#match) function 
    * [Joins](https://eql.readthedocs.io/en/latest/query-guide/joins.html)
    * [Lineage-related keywords](https://eql.readthedocs.io/en/latest/query-guide/basic-syntax.html#event-relationships):

      * `child of`
      * `descendant of`
      * `event of`

    * The following [pipes](https://eql.readthedocs.io/en/latest/query-guide/pipes.html):

      * [`count`](https://eql.readthedocs.io/en/latest/query-guide/pipes.html#count)
      * [`filter`](https://eql.readthedocs.io/en/latest/query-guide/pipes.html#filter)
      * [`sort`](https://eql.readthedocs.io/en/latest/query-guide/pipes.html#sort)
      * [`unique`](https://eql.readthedocs.io/en/latest/query-guide/pipes.html#unique)
      * [`unique_count`](https://eql.readthedocs.io/en/latest/query-guide/pipes.html#unique-count)

#### 序列查询如何处理匹配项

序列查询找不到序列的所有潜在匹配项。对于大型事件数据集，此方法太慢且成本太高。相反，序列查询将挂起的序列匹配作为状态机处理：

* 序列查询中的每个事件项都是计算机中的一个状态。  * 每种状态一次只能有一个挂起序列。  * 如果两个挂起序列同时处于相同状态，则最新的序列将覆盖较旧的序列。  * 如果查询包含"by"字段，则查询对每个唯一的"by"字段值使用单独的状态机。

**Example**

数据集包含以下按时间升序排列的"过程"事件：

    
    
    { "index" : { "_id": "1" } }
    { "user": { "name": "root" }, "process": { "name": "attrib" }, ...}
    { "index" : { "_id": "2" } }
    { "user": { "name": "root" }, "process": { "name": "attrib" }, ...}
    { "index" : { "_id": "3" } }
    { "user": { "name": "elkbee" }, "process": { "name": "bash" }, ...}
    { "index" : { "_id": "4" } }
    { "user": { "name": "root" }, "process": { "name": "bash" }, ...}
    { "index" : { "_id": "5" } }
    { "user": { "name": "root" }, "process": { "name": "bash" }, ...}
    { "index" : { "_id": "6" } }
    { "user": { "name": "elkbee" }, "process": { "name": "attrib" }, ...}
    { "index" : { "_id": "7" } }
    { "user": { "name": "root" }, "process": { "name": "attrib" }, ...}
    { "index" : { "_id": "8" } }
    { "user": { "name": "elkbee" }, "process": { "name": "bash" }, ...}
    { "index" : { "_id": "9" } }
    { "user": { "name": "root" }, "process": { "name": "cat" }, ...}
    { "index" : { "_id": "10" } }
    { "user": { "name": "elkbee" }, "process": { "name": "cat" }, ...}
    { "index" : { "_id": "11" } }
    { "user": { "name": "root" }, "process": { "name": "cat" }, ...}

EQL 序列查询搜索数据集：

    
    
    sequence by user.name
      [process where process.name == "attrib"]
      [process where process.name == "bash"]
      [process where process.name == "cat"]

查询的事件项对应于以下状态：

* 状态 A："[process.name == "属性"]的进程]" * 状态 B："[process.name == "bash"]] * 完成："[process.name == "cat"]]

！序列状态机

为了查找匹配的序列，查询对每个唯一的"user.name"值使用单独的状态机。根据数据集，您可以期待两个状态机：一个用于"root"用户，一个用于"elkbee"。

！独立的状态机

挂起的序列匹配在每台计算机的状态中移动，如下所示：

    
    
    { "index" : { "_id": "1" } }
    { "user": { "name": "root" }, "process": { "name": "attrib" }, ...}
    // Creates sequence [1] in state A for the "root" user.
    //
    // +------------------------"root"------------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |    [1]    |     |           |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "2" } }
    { "user": { "name": "root" }, "process": { "name": "attrib" }, ...}
    // Creates sequence [2] in state A for "root", overwriting sequence [1].
    //
    // +------------------------"root"------------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |    [2]    |     |           |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "3" } }
    { "user": { "name": "elkbee" }, "process": { "name": "bash" }, ...}
    // Nothing happens. The "elkbee" user has no pending sequence to move
    // from state A to state B.
    //
    // +-----------------------"elkbee"-----------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |           |     |           |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "4" } }
    { "user": { "name": "root" }, "process": { "name": "bash" }, ...}
    // Sequence [2] moves out of state A for "root".
    // State B for "root" now contains [2, 4].
    // State A for "root" is empty.
    //
    // +------------------------"root"------------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+ --> +-----------+     +------------+  |
    // |  |           |     |   [2, 4]  |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "5" } }
    { "user": { "name": "root" }, "process": { "name": "bash" }, ...}
    // Nothing happens. State A is empty for "root".
    //
    // +------------------------"root"------------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |           |     |   [2, 4]  |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "6" } }
    { "user": { "name": "elkbee" }, "process": { "name": "attrib" }, ...}
    // Creates sequence [6] in state A for "elkbee".
    //
    // +-----------------------"elkbee"-----------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |    [6]    |     |           |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "7" } }
    { "user": { "name": "root" }, "process": { "name": "attrib" }, ...}
    // Creates sequence [7] in state A for "root".
    // Sequence [2, 4] remains in state B for "root".
    //
    // +------------------------"root"------------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |    [7]    |     |   [2, 4]  |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "8" } }
    { "user": { "name": "elkbee" }, "process": { "name": "bash" }, ...}
    // Sequence [6, 8] moves to state B for "elkbee".
    // State A for "elkbee" is now empty.
    //
    // +-----------------------"elkbee"-----------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+ --> +-----------+     +------------+  |
    // |  |           |     |   [6, 8]  |     |            |  |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "9" } }
    { "user": { "name": "root" }, "process": { "name": "cat" }, ...}
    // Sequence [2, 4, 9] is complete for "root".
    // State B for "root" is now empty.
    // Sequence [7] remains in state A.
    //
    // +------------------------"root"------------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+ --> +------------+  |
    // |  |    [7]    |     |           |     |  [2, 4, 9] |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "10" } }
    { "user": { "name": "elkbee" }, "process": { "name": "cat" }, ...}
    // Sequence [6, 8, 10] is complete for "elkbee".
    // State A and B for "elkbee" are now empty.
    //
    // +-----------------------"elkbee"-----------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+ --> +------------+  |
    // |  |           |     |           |     | [6, 8, 10] |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    
    { "index" : { "_id": "11" } }
    { "user": { "name": "root" }, "process": { "name": "cat" }, ...}
    // Nothing happens.
    // The machines for "root" and "elkbee" remain the same.
    //
    // +------------------------"root"------------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |    [7]    |     |           |     |  [2, 4, 9] |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+
    //
    // +-----------------------"elkbee"-----------------------+
    // |  +-----------+     +-----------+     +------------+  |
    // |  |  State A  |     |  State B  |     |  Complete  |  |
    // |  +-----------+     +-----------+     +------------+  |
    // |  |           |     |           |     | [6, 8, 10] |
    // |  +-----------+     +-----------+     +------------+  |
    // +------------------------------------------------------+

[« EQL search](eql.md) [EQL function reference »](eql-function-ref.md)
