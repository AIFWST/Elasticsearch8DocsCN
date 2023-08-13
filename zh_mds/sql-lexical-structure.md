

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« SQL Language](sql-spec.md) [SQL Commands »](sql-commands.md)

## 词汇结构

本节涵盖了SQL的主要词汇结构，在大多数情况下，它将类似于ANSI SQL本身，因此没有深入讨论低级细节。

Elasticsearch SQL 目前一次只接受一个 _command_。命令是由输入流末尾终止的 _tokens_ 序列。

标记可以是_key word_、标识符(引用或未引用)、a_literal_(或常量)或特殊字符符号(通常是分隔符)。标记通常由空格(空格，制表符)分隔，但在某些情况下，如果没有歧义(通常是由于字符符号)，则不需要这样做 - 但是出于可读性目的，应避免这样做。

### 关键词

举个例子：

    
    
    SELECT * FROM table

此查询有四个标记："选择"、"*"、"发件人"和"表"。前三个，即"SELECT"，"*"和"FROM"_key words_意思是在SQL中具有固定含义的单词。令牌"表"是一个_标识符_，这意味着它标识(按名称)SQL中的实体，例如表(在本例中)，列等...

如您所见，关键字和标识符都具有_same_词法结构，因此如果不了解SQL语言，就无法知道令牌是一个还是另一个;关键词的完整列表见附录。请注意，关键字不区分大小写，这意味着前面的示例可以写为：

    
    
    select * fRoM table;

然而，标识符不是 - 因为Elasticsearch区分大小写，Elasticsearch SQL逐字使用接收到的值。

为了帮助区分这两者，在整个文档中，SQL关键字都是大写的，我们发现这种约定提高了可读性，因此推荐给其他人。

###Identifiers

标识符可以有两种类型：_quoted_ 和 _unquoted_：

    
    
    SELECT ip_address FROM "hosts-*"

此查询有两个标识符："ip_address"和"hosts-*"(索引模式)。由于"ip_address"不与任何关键字冲突，因此可以逐字使用，另一方面，"hosts-*"不能，因为它与"-"(减号操作)和"*"冲突，因此需要双引号。

再比如：

    
    
    SELECT "from" FROM "<logstash-{now/d}>"

来自的第一个标识符需要引用，否则它与"FROM"关键字冲突(不区分大小写，因此可以写为"from")，而第二个标识符在索引和索引别名中使用Elasticsearch Date数学支持会混淆解析器。

因此，为什么一般来说，**特别是**在处理用户输入时，**强烈建议使用引号作为标识符。它为您的查询增加了最小的增加，并反过来提供清晰度和消除歧义。

### 文字(常量)

Elasticsearch SQL支持两种_implicitly typed_文字：字符串和数字。

##### 字符串文字

字符串文本是由单引号""："巨型机器人"限定的任意数量的字符。要在字符串中包含单引号，请使用另一个单引号对其进行转义："EO 船长的航行"。

转义的单引号不是双引号 ('"')，而是单引号 _'

##### 数字文字

数字文字以十进制和科学记数法和科学记数法接受，带有指数标记("e"或"E")，以数字或小数点开头。

    
    
    1969    -- integer notation
    3.14    -- decimal notation
    .1234   -- decimal notation starting with decimal point
    4E5     -- scientific notation (with exponent marker)
    1.2e-3  -- scientific notation with decimal point

包含小数点的数字文本始终被解释为类型为"double"。如果没有的那些被认为是"整数"，如果它们适合否则它们的类型是"long"(或 ANSI SQL 类型中的"BIGINT")。

##### 泛型文字

在处理任意类型文本时，通常通过将字符串表示形式转换为所需类型来创建对象。这可以通过专门的铸造操作员和功能来实现：

    
    
    123::LONG                                   -- cast 123 to a LONG
    CAST('1969-05-13T12:34:56' AS TIMESTAMP)    -- cast the given string to datetime
    CONVERT('10.0.0.1', IP)                     -- cast '10.0.0.1' to an IP

请注意，Elasticsearch SQL提供的函数开箱即用地返回流行的文字(如'E()')或为某些字符串提供专用解析。

### 单引号与双引号

值得指出的是，在SQL中，单引号'''和双引号'具有不同的含义，**不能互换使用。单引号用于声明字符串文本，而标识符则用于声明双引号。

即：

    
    
    SELECT "first_name" __FROM "musicians" __WHERE "last_name" __= 'Carroll' __

__

|

用于列和表标识符的双引号 '"' ---|--- __

|

用于字符串文本的单引号 ''' 要转义单引号或双引号，需要再次使用该特定引号。例如，文字"John's"可以像"SELECT'John's' AS name"一样进行转义。双引号转义也是如此 - "SELECT 123 AS"test""number""将显示一个名为"test"number"的列。

### 特殊字符

一些非字母数字字符具有与运算符不同的专用含义。为完整起见，下面指定了这些内容：

**Char**

|

**描述** ---|--- '*'

|

星号(或通配符)在某些上下文中用于表示 atable 的所有字段。也可以用作某些聚合函数的参数。   `,`

|

逗号用于枚举列表的元素。   `.`

|

用于数字常量或分隔标识符限定符(目录、表、列名等)。   `()`

|

括号用于特定的 SQL 命令、函数声明或强制优先级。   ###Operatorsedit

Elasticsearch SQL中的大多数运算符都具有相同的优先级，并且是左关联运算符。由于这是在解析时完成的，因此需要使用括号来强制执行不同的优先级。

下表显示了支持的运算符及其优先级(从最高到最低);

**Operator/Element**

|

**Associativity**

|

**描述** ---|---|--- '."

|

left

|

限定符分隔符 '：：'

|

left

|

PostgreSQL 样式的类型转换 '+ -'

|

right

|

一元加减号(数字文字符号)'* / %'

|

left

|

乘法、除法、模 '+ -'

|

left

|

加法，减去"在喜欢之间"

|

|

范围包含，字符串匹配 '< > <= >= = <=> <> ！='

|

|

比较"不"

|

right

|

逻辑否定"和"

|

left

|

逻辑连词"或"

|

left

|

逻辑析取 ###Commentsedit

Elasticsearch SQL允许被解析器忽略的字符序列注释。

支持两种样式：

单行

     Comments start with a double dash `--` and continue until the end of the line. 
Multi line

     Comments that start with `/*` and end with `*/` (also known as C-style). 
    
    
    -- single line comment
    /* multi
       line
       comment
       that supports /* nested comments */
       */

[« SQL Language](sql-spec.md) [SQL Commands »](sql-commands.md)
