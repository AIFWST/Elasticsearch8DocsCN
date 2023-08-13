

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Mathematical Functions](sql-functions-math.md) [Type Conversion Functions
»](sql-functions-type-conversion.md)

## 字符串函数

用于执行字符串操作的函数。

###'ASCII'

**Synopsis:**

    
    
    ASCII(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**说明**：以整数形式返回最左侧字符"string_exp"的 ASCII 代码值。

    
    
    SELECT ASCII('Elastic');
    
    ASCII('Elastic')
    ----------------
    69

###'BIT_LENGTH'

**Synopsis:**

    
    
    BIT_LENGTH(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**说明**：返回"string_exp"输入表达式的长度(以位为单位)。

    
    
    SELECT BIT_LENGTH('Elastic');
    
    BIT_LENGTH('Elastic')
    ---------------------
    56

###'字符'

**Synopsis:**

    
    
    CHAR(code) __

**输入**：

__

|

介于"0"和"255"之间的整数表达式。如果为"null"、负数或大于"255"，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回具有由数字输入指定的 ASCII 代码值的字符。

    
    
    SELECT CHAR(69);
    
       CHAR(69)
    ---------------
    E

###'CHAR_LENGTH'

**Synopsis:**

    
    
    CHAR_LENGTH(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**说明**：如果字符串表达式是字符数据类型，则返回输入的长度(以字符为单位);否则，返回字符串表达式的长度(以字节为单位)(最小整数不小于位数除以 8)。

    
    
    SELECT CHAR_LENGTH('Elastic');
    
    CHAR_LENGTH('Elastic')
    ----------------------
    7

###'康卡特'

**Synopsis:**

    
    
    CONCAT(
        string_exp1, __string_exp2) __

**输入**：

__

|

字符串表达式。将"null"视为空字符串。   ---|---    __

|

字符串表达式。将"null"视为空字符串。   **输出**：字符串

**说明**：返回一个字符串，该字符串是将"string_exp1"连接到"string_exp2"的结果。

    
    
    SELECT CONCAT('Elasticsearch', ' SQL');
    
    CONCAT('Elasticsearch', ' SQL')
    -------------------------------
    Elasticsearch SQL

###'插入'

**Synopsis:**

    
    
    INSERT(
        source,      __start, __length, __replacement) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式。如果为"null"，则函数返回"null"。   __

|

整数表达式。如果为"null"，则函数返回"null"。   __

|

字符串表达式。如果为"null"，则函数返回"null"。   **输出**：字符串

**说明**：返回一个字符串，其中"长度"字符已从"源"中删除，从"开始"开始，"替换"已插入到"源"中，从"开始"开始。

    
    
    SELECT INSERT('Elastic ', 8, 1, 'search');
    
    INSERT('Elastic ', 8, 1, 'search')
    ----------------------------------
    Elasticsearch

###'LCASE'

**Synopsis:**

    
    
    LCASE(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回一个等于"string_exp"中的字符串，所有大写字符转换为小写。

    
    
    SELECT LCASE('Elastic');
    
    LCASE('Elastic')
    ----------------
    elastic

###'左'

**Synopsis:**

    
    
    LEFT(
        string_exp, __count) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式。如果为"null"，则函数返回"null"。如果为"0"或否定，则该函数返回一个空字符串。   **输出**：字符串

**说明**：返回"string_exp"最左侧的计数字符。

    
    
    SELECT LEFT('Elastic',3);
    
    LEFT('Elastic',3)
    -----------------
    Ela

###'长度'

**Synopsis:**

    
    
    LENGTH(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**说明**：返回"string_exp"中的字符数，不包括尾随空格。

    
    
    SELECT LENGTH('Elastic   ');
    
    LENGTH('Elastic   ')
    --------------------
    7

###'定位'

**Synopsis:**

    
    
    LOCATE(
        pattern, __source __[, start] __)

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

字符串表达式。如果为"null"，则函数返回"null"。   __

|

整数表达式;自选。如果"null"、"0"、"1"、否定或未指定，则搜索将从第一个字符位置开始。   **输出**：整数

**描述**：返回"源"中第一次出现的"模式"的起始位置。可选的"start"指定要用来开始搜索的字符位置。如果在"源"中找不到"模式"，则该函数返回"0"。

    
    
    SELECT LOCATE('a', 'Elasticsearch');
    
    LOCATE('a', 'Elasticsearch')
    ----------------------------
    3
    
    
    SELECT LOCATE('a', 'Elasticsearch', 5);
    
    LOCATE('a', 'Elasticsearch', 5)
    -------------------------------
    10

###'LTRIM'

**Synopsis:**

    
    
    LTRIM(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回"string_exp"的字符，删除前导空格。

    
    
    SELECT LTRIM('   Elastic');
    
    LTRIM('   Elastic')
    -------------------
    Elastic

###'OCTET_LENGTH'

**Synopsis:**

    
    
    OCTET_LENGTH(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**说明**：返回"string_exp"输入表达式的长度(以字节为单位)。

    
    
    SELECT OCTET_LENGTH('Elastic');
    
    OCTET_LENGTH('Elastic')
    -----------------------
    7

###'仓位'

**Synopsis:**

    
    
    POSITION(
        string_exp1, __string_exp2) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

字符串表达式。如果为"null"，则函数返回"null"。   **输出**：整数

**说明**：返回"string_exp1"在"string_exp2"中的位置。结果是一个精确的数字。

    
    
    SELECT POSITION('Elastic', 'Elasticsearch');
    
    POSITION('Elastic', 'Elasticsearch')
    ------------------------------------
    1

###'重复'

**Synopsis:**

    
    
    REPEAT(
        string_exp, __count) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式。如果为"0"、负数或"null"，则函数返回"null"。   **输出**：字符串

**说明**：返回由"string_exp"重复"计数"次数组成的字符串。

    
    
    SELECT REPEAT('La', 3);
    
     REPEAT('La', 3)
    ----------------
    LaLaLa

###"替换"

**Synopsis:**

    
    
    REPLACE(
        source,      __pattern, __replacement) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

字符串表达式。如果为"null"，则函数返回"null"。   __

|

字符串表达式。如果为"null"，则函数返回"null"。   **输出**：字符串

**描述**：在"源"中搜索"模式"的出现，并替换为"替换"。

    
    
    SELECT REPLACE('Elastic','El','Fant');
    
    REPLACE('Elastic','El','Fant')
    ------------------------------
    Fantastic

###'对'

**Synopsis:**

    
    
    RIGHT(
        string_exp, __count) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式。如果为"null"，则函数返回"null"。如果为"0"或否定，则该函数返回一个空字符串。   **输出**：字符串

**说明**：返回"string_exp"最右侧的计数字符。

    
    
    SELECT RIGHT('Elastic',3);
    
    RIGHT('Elastic',3)
    ------------------
    tic

###'RTRIM'

**Synopsis:**

    
    
    RTRIM(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回删除尾随空格的"string_exp"字符。

    
    
    SELECT RTRIM('Elastic   ');
    
    RTRIM('Elastic   ')
    -------------------
    Elastic

###'空间'

**Synopsis:**

    
    
    SPACE(count) __

**输入**：

__

|

整数表达式。如果为"null"或负数，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回由"计数"空格组成的字符串。

    
    
    SELECT SPACE(3);
    
       SPACE(3)
    ---------------

###'STARTS_WITH'

**Synopsis:**

    
    
    STARTS_WITH(
        source,   __pattern) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

字符串表达式。如果为"null"，则函数返回"null"。   **输出**：布尔值

**说明**：如果源表达式以指定的模式开头，则返回"true"，否则返回"false"。匹配区分大小写。

    
    
    SELECT STARTS_WITH('Elasticsearch', 'Elastic');
    
    STARTS_WITH('Elasticsearch', 'Elastic')
    --------------------------------
    true
    
    
    SELECT STARTS_WITH('Elasticsearch', 'ELASTIC');
    
    STARTS_WITH('Elasticsearch', 'ELASTIC')
    --------------------------------
    false

###'子字符串'

**Synopsis:**

    
    
    SUBSTRING(
        source, __start, __length) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式。如果为"null"，则函数返回"null"。   __

|

整数表达式。如果为"null"，则函数返回"null"。   **输出**：字符串

**说明**：返回派生自"源"的字符串，从"开始"为"长度"字符指定的字符位置开始。

    
    
    SELECT SUBSTRING('Elasticsearch', 0, 7);
    
    SUBSTRING('Elasticsearch', 0, 7)
    --------------------------------
    Elastic

###'修剪'

**Synopsis:**

    
    
    TRIM(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回"string_exp"的字符，删除前导和尾随空格。

    
    
    SELECT TRIM('   Elastic   ') AS trimmed;
    
    trimmed
    --------------
    Elastic

###'UCASE'

**Synopsis:**

    
    
    UCASE(string_exp) __

**输入**：

__

|

字符串表达式。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回一个等于输入的字符串，所有小写字符都转换为大写。

    
    
    SELECT UCASE('Elastic');
    
    UCASE('Elastic')
    ----------------
    ELASTIC

[« Mathematical Functions](sql-functions-math.md) [Type Conversion Functions
»](sql-functions-type-conversion.md)
