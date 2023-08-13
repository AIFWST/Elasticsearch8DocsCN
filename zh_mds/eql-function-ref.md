

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[EQL
search](eql.md)

[« EQL syntax reference](eql-syntax.md) [EQL pipe reference »](eql-pipe-
ref.md)

## EQL 函数引用

Elasticsearch 支持以下 EQL 函数。

###'添加'

返回两个提供的增补的总和。

**Example**

    
    
    add(4, 5)                                           // returns 9
    add(4, 0.5)                                         // returns 4.5
    add(0.5, 0.25)                                      // returns 0.75
    add(4, -2)                                          // returns 2
    add(-2, -2)                                         // returns -4
    
    // process.args_count = 4
    add(process.args_count, 5)                          // returns 9
    add(process.args_count, 0.5)                        // returns 4.5
    
    // process.parent.args_count = 2
    add(process.args_count, process.parent.args_count)  // returns 6
    
    // null handling
    add(null, 4)                                        // returns null
    add(4. null)                                        // returns null
    add(null, process.args_count)                       // returns null
    add(process.args_count null)                        // returns null

**Syntax**

    
    
    add(<addend>, <addend>)

**Parameters:**

`<addend>`

    

(必需、整数或浮点数或"空")添加到添加。如果为"null"，则函数返回"null"。

需要两个补充。不能提供超过两个增补。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

**返回：** 整数、浮点数或"null"

###'之间'

提取源字符串中提供的"左"和"右"文本之间的子字符串。默认情况下，匹配区分大小写。

**Example**

    
    
    // file.path = "C:\\Windows\\System32\\cmd.exe"
    between(file.path, "System32\\\\", ".exe")                // returns "cmd"
    between(file.path, "system32\\\\", ".exe")                // returns ""
    between(file.path, "workspace\\\\", ".exe")               // returns ""
    
    // Make matching case-insensitive
    between~(file.path, "system32\\\\", ".exe")               // returns "cmd"
    
    // Greedy matching defaults to false.
    between(file.path, "\\\\", "\\\\", false)                 // returns "Windows"
    
    // Sets greedy matching to true
    between(file.path, "\\\\", "\\\\", true)                  // returns "Windows\\System32"
    
    // empty source string
    between("", "System32\\\\", ".exe")                       // returns ""
    between("", "", "")                                       // returns ""
    
    // null handling
    between(null, "System32\\\\", ".exe")                     // returns null

**Syntax**

    
    
    between(<source>, <left>, <right>[, <greedy_matching>])

**Parameters**

`<source>`

    

(必需，字符串或"空")源字符串。空字符串返回空字符串 ('""')，而不考虑 '<left>' 或 '<right>' 参数。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<left>`

    

(必需，字符串)要提取的子字符串左侧的文本。此文本应包含空格。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<right>`

    

(必需，字符串)要提取的子字符串右侧的文本。此文本应包含空格。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<greedy_matching>`

     (Optional, Boolean) If `true`, match the longest possible substring, similar to `.*` in regular expressions. If `false`, match the shortest possible substring, similar to `.*?` in regular expressions. Defaults to `false`. 

**返回：** 字符串或 'null'

###'cidrMatch'

如果 IP 地址包含在一个或多个提供的 CIDR 块中，则返回"true"。

**Example**

    
    
    // source.address = "192.168.152.12"
    cidrMatch(source.address, "192.168.0.0/16")               // returns true
    cidrMatch(source.address, "192.168.0.0/16", "10.0.0.0/8") // returns true
    cidrMatch(source.address, "10.0.0.0/8")                   // returns false
    cidrMatch(source.address, "10.0.0.0/8", "10.128.0.0/9")   // returns false
    
    // null handling
    cidrMatch(null, "10.0.0.0/8")                             // returns null
    cidrMatch(source.address, null)                           // returns null

**Syntax**

    
    
    `cidrMatch(<ip_address>, <cidr_block>[, ...])`

**Parameters**

`<ip_address>`

    

(必需，字符串或"空")IP地址。支持IPv4和IPv6地址。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持"ip"字段数据类型。

`<cidr_block>`

     (Required†[1], string or `null`) CIDR block you wish to search. If `null`, the function returns `null`. 

**返回：** 布尔值或"空值"

###'concat'

返回所提供值的串联字符串。

**Example**

    
    
    concat("process is ", "regsvr32.exe")         // returns "process is regsvr32.exe"
    concat("regsvr32.exe", " ", 42)               // returns "regsvr32.exe 42"
    concat("regsvr32.exe", " ", 42.5)             // returns "regsvr32.exe 42.5"
    concat("regsvr32.exe", " ", true)             // returns "regsvr32.exe true"
    concat("regsvr32.exe")                        // returns "regsvr32.exe"
    
    // process.name = "regsvr32.exe"
    concat(process.name, " ", 42)                 // returns "regsvr32.exe 42"
    concat(process.name, " ", 42.5)               // returns "regsvr32.exe 42.5"
    concat("process is ", process.name)           // returns "process is regsvr32.exe"
    concat(process.name, " ", true)               // returns "regsvr32.exe true"
    concat(process.name)                          // returns "regsvr32.exe"
    
    // process.arg_count = 4
    concat(process.name, " ", process.arg_count)  // returns "regsvr32.exe 4"
    
    // null handling
    concat(null, "regsvr32.exe")                  // returns null
    concat(process.name, null)                    // returns null
    concat(null)                                  // returns null

**Syntax**

    
    
    concat(<value>[, <value>])

**Parameters**

`<value>`

    

(必填†[1])要连接的值。如果任何参数为"null"，则该函数返回"null"。

如果使用字段作为参数，则此参数不支持"文本"字段数据类型。

**返回：** 字符串或 'null'

###"除"

返回提供的除数和除数的商。

如果除数和除数都是整数，则"除法"函数_舍入_将任何返回的浮点数转换为最接近的整数。为避免四舍五入，请将股息或除数转换为浮动。

**Example**

"process.args_count"字段是包含进程参数计数的"长"整数字段。

用户可能希望以下 EQL 查询仅匹配值为"4"process.args_count"的事件。

    
    
    process where divide(4, process.args_count) == 1

但是，EQL 查询匹配"process.args_count"值为"3"或"4"的事件。

对于"process.args_count"值为"3"的事件，"除法"函数返回浮点数"1.333..."，该数向下舍入为"1"。

要仅匹配"process.args_count"值为"4"的事件，请将除数或除数转换为浮动值。

以下 EQL 查询将整数"4"更改为等效的浮点数"4.0"。

    
    
    process where divide(4.0, process.args_count) == 1

**Example**

    
    
    divide(4, 2)                                            // returns 2
    divide(4, 3)                                            // returns 1
    divide(4, 3.0)                                          // returns 1.333...
    divide(4, 0.5)                                          // returns 8
    divide(0.5, 4)                                          // returns 0.125
    divide(0.5, 0.25)                                       // returns 2.0
    divide(4, -2)                                           // returns -2
    divide(-4, -2)                                          // returns 2
    
    // process.args_count = 4
    divide(process.args_count, 2)                           // returns 2
    divide(process.args_count, 3)                           // returns 1
    divide(process.args_count, 3.0)                         // returns 1.333...
    divide(12, process.args_count)                          // returns 3
    divide(process.args_count, 0.5)                         // returns 8
    divide(0.5, process.args_count)                         // returns 0.125
    
    // process.parent.args_count = 2
    divide(process.args_count, process.parent.args_count)   // returns 2
    
    // null handling
    divide(null, 4)                                         // returns null
    divide(4, null)                                         // returns null
    divide(null, process.args_count)                        // returns null
    divide(process.args_count, null)                        // returns null

**Syntax**

    
    
    divide(<dividend>, <divisor>)

**Parameters**

`<dividend>`

    

(必需、整数或浮点数或"空")分红除法。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

`<divisor>`

    

(必需、整数或浮点数或"空")除数除以。如果为"null"，则函数返回"null"。此值不能为零 ('0')。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

**返回：** 整数、浮点数或空值

###'结束于'

如果源字符串以提供的子字符串结尾，则返回"true"。默认情况下，匹配区分大小写。

**Example**

    
    
    endsWith("regsvr32.exe", ".exe")          // returns true
    endsWith("regsvr32.exe", ".EXE")          // returns false
    endsWith("regsvr32.exe", ".dll")          // returns false
    endsWith("", "")                          // returns true
    
    // Make matching case-insensitive
    endsWith~("regsvr32.exe", ".EXE")         // returns true
    
    // file.name = "regsvr32.exe"
    endsWith(file.name, ".exe")               // returns true
    endsWith(file.name, ".dll")               // returns false
    
    // file.extension = ".exe"
    endsWith("regsvr32.exe", file.extension)  // returns true
    endsWith("ntdll.dll", file.name)          // returns false
    
    // null handling
    endsWith("regsvr32.exe", null)            // returns null
    endsWith("", null)                        // returns null
    endsWith(null, ".exe")                    // returns null
    endsWith(null, null)                      // returns null

**Syntax**

    
    
    endsWith(<source>, <substring>)

**Parameters**

`<source>`

    

(必需，字符串或"空")源字符串。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<substring>`

    

(必需，字符串或"空")要搜索的子字符串。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

**返回：** 布尔值或"空值"

###'索引'

返回提供的子字符串在源字符串中的第一个位置。默认情况下，匹配区分大小写。

如果提供了可选的起始位置，则此函数返回子字符串在开始位置处或之后的第一次出现。

**Example**

    
    
    // url.domain = "subdomain.example.com"
    indexOf(url.domain, "d")        // returns 3
    indexOf(url.domain, "D")        // returns null
    indexOf(url.domain, ".")        // returns 9
    indexOf(url.domain, ".", 9)     // returns 9
    indexOf(url.domain, ".", 10)    // returns 17
    indexOf(url.domain, ".", -6)    // returns 9
    
    // Make matching case-insensitive
    indexOf~(url.domain, "D")        // returns 4
    
    // empty strings
    indexOf("", "")                 // returns 0
    indexOf(url.domain, "")         // returns 0
    indexOf(url.domain, "", 9)      // returns 9
    indexOf(url.domain, "", 10)     // returns 10
    indexOf(url.domain, "", -6)     // returns 0
    
    // missing substrings
    indexOf(url.domain, "z")        // returns null
    indexOf(url.domain, "z", 9)     // returns null
    
    // start position is higher than string length
    indexOf(url.domain, ".", 30)    // returns null
    
    // null handling
    indexOf(null, ".", 9)           // returns null
    indexOf(url.domain, null, 9)    // returns null
    indexOf(url.domain, ".", null)  // returns null

**Syntax**

    
    
    indexOf(<source>, <substring>[, <start_pos>])

**Parameters**

`<source>`

    

(必需，字符串或"空")源字符串。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<substring>`

    

(必需，字符串或"空")要搜索的子字符串。

如果此参数为 'null' 或 '' 字符串<source>不包含此子字符串，则该函数返回 'null'。

如果 '' <start_pos>为正数，则空字符串 ('""') 返回 '<start_pos>'。否则，空字符串返回"0"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<start_pos>`

    

(可选、整数或"空")匹配的起始位置。该函数不会在此函数之前返回仓位。默认为"0"。

仓位为零索引。负偏移量被视为"0"。

如果此参数为 'null' 或大于 '' 字符串的长度<source>，则该函数返回 'null'。

如果使用字段作为参数，则此参数仅支持以下数值字段数据类型：

* "长" * "整数" * "短" * "字节"

**返回：** 整数或 'null'

###'长度'

返回所提供字符串的字符长度，包括空格和标点符号。

**Example**

    
    
    length("explorer.exe")         // returns 12
    length("start explorer.exe")   // returns 18
    length("")                     // returns 0
    length(null)                   // returns null
    
    // process.name = "regsvr32.exe"
    length(process.name)           // returns 12

**Syntax**

    
    
    length(<string>)

**Parameters**

`<string>`

    

(必需，字符串或"空")要为其返回字符长度的字符串。如果为"null"，则函数返回"null"。空字符串返回"0"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

**返回：** 整数或 'null'

###'模'

返回提供的除数和除数的除数的剩余部分。

**Example**

    
    
    modulo(10, 6)                                       // returns 4
    modulo(10, 5)                                       // returns 0
    modulo(10, 0.5)                                     // returns 0
    modulo(10, -6)                                      // returns 4
    modulo(-10, -6)                                     // returns -4
    
    // process.args_count = 10
    modulo(process.args_count, 6)                       // returns 4
    modulo(process.args_count, 5)                       // returns 0
    modulo(106, process.args_count)                     // returns 6
    modulo(process.args_count, -6)                      // returns 4
    modulo(process.args_count, 0.5)                     // returns 0
    
    // process.parent.args_count = 6
    modulo(process.args_count, process.parent.args_count)  // returns 4
    
    // null handling
    modulo(null, 5)                                     // returns null
    modulo(7, null)                                     // returns null
    modulo(null, process.args_count)                    // returns null
    modulo(process.args_count, null)                    // returns null

**Syntax**

    
    
    modulo(<dividend>, <divisor>)

**Parameters**

`<dividend>`

    

(必需、整数或浮点数或"空")分红除法。如果为"null"，则函数返回"null"。浮点数返回"0"。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

`<divisor>`

    

(必需、整数或浮点数或"空")除数除以。如果为"null"，则函数返回"null"。浮点数返回"0"。此值不能为零 ('0')。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

**返回：** 整数、浮点数或"null"

###'乘法'

返回两个提供的因子的乘积。

**Example**

    
    
    multiply(2, 2)                                           // returns 4
    multiply(0.5, 2)                                         // returns 1
    multiply(0.25, 2)                                        // returns 0.5
    multiply(-2, 2)                                          // returns -4
    multiply(-2, -2)                                         // returns 4
    
    // process.args_count = 2
    multiply(process.args_count, 2)                          // returns 4
    multiply(0.5, process.args_count)                        // returns 1
    multiply(0.25, process.args_count)                       // returns 0.5
    
    // process.parent.args_count = 3
    multiply(process.args_count, process.parent.args_count)  // returns 6
    
    // null handling
    multiply(null, 2)                                        // returns null
    multiply(2, null)                                        // returns null

**Syntax**

    
    
    multiply(<factor, <factor>)

**Parameters**

`<factor>`

    

(必需、整数或浮点数或"空")乘以的因素。如果为"null"，则函数返回"null"。

需要两个因素。不能提供超过两个因素。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

**返回：** 整数、浮点数或"null"

###'数字'

将字符串转换为相应的整数或浮点数。

**Example**

    
    
    number("1337")              // returns 1337
    number("42.5")              // returns 42.5
    number("deadbeef", 16)      // returns 3735928559
    
    // integer literals beginning with "0x" are auto-detected as hexadecimal
    number("0xdeadbeef")        // returns 3735928559
    number("0xdeadbeef", 16)    // returns 3735928559
    
    // "+" and "-" are supported
    number("+1337")             // returns 1337
    number("-1337")             // returns -1337
    
    // surrounding whitespace is ignored
    number("  1337  ")          // returns 1337
    
    // process.pid = "1337"
    number(process.pid)         // returns 1337
    
    // null handling
    number(null)                // returns null
    number(null, 16)            // returns null
    
    // strings beginning with "0x" are treated as hexadecimal (base 16),
    // even if the <base_num> is explicitly null.
    number("0xdeadbeef", null) // returns 3735928559
    
    // otherwise, strings are treated as decimal (base 10)
    // if the <base_num> is explicitly null.
    number("1337", null)        // returns 1337

**Syntax**

    
    
    number(<string>[, <base_num>])

**Parameters**

`<string>`

    

(必需，字符串或"空")要转换为整数或浮点数的字符串。如果此值是字符串，则它必须是以下值之一：

* 整数的字符串表示形式(例如，"42"") * 浮点数的字符串表示形式(例如，"9.5"") * 如果指定了 '' 参数，则在<base_num>基本表示法中包含整数文本的字符串(例如0xDECAFBAD，十六进制或基数为 '16')

以"0x"开头的字符串会自动检测为十六进制，并使用默认的"<base_num>16"。

支持"-"和"+"，两者之间没有空格。周围的空格将被忽略。不支持空字符串 ('""')。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

如果此参数为"null"，则函数返回"null"。

`<base_num>`

    

(可选、整数或"空")用于转换字符串的基数或基数。如果"<string>"以"0x"开头，则此参数默认为"16"(十六进制)。否则，它默认为基数"10"。

如果此参数显式为"null"，则使用默认值。

不支持将字段作为参数。

**返回：** 整数或浮点数或"空"

###'开始于'

如果源字符串以提供的子字符串开头，则返回"true"。默认情况下，匹配区分大小写。

**Example**

    
    
    startsWith("regsvr32.exe", "regsvr32")  // returns true
    startsWith("regsvr32.exe", "Regsvr32")  // returns false
    startsWith("regsvr32.exe", "explorer")  // returns false
    startsWith("", "")                      // returns true
    
    // Make matching case-insensitive
    startsWith~("regsvr32.exe", "Regsvr32")  // returns true
    
    // process.name = "regsvr32.exe"
    startsWith(process.name, "regsvr32")    // returns true
    startsWith(process.name, "explorer")    // returns false
    
    // process.name = "regsvr32"
    startsWith("regsvr32.exe", process.name) // returns true
    startsWith("explorer.exe", process.name) // returns false
    
    // null handling
    startsWith("regsvr32.exe", null)        // returns null
    startsWith("", null)                    // returns null
    startsWith(null, "regsvr32")            // returns null
    startsWith(null, null)                  // returns null

**Syntax**

    
    
    startsWith(<source>, <substring>)

**Parameters**

`<source>`

    

(必需，字符串或"空")源字符串。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<substring>`

    

(必需，字符串或"空")要搜索的子字符串。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

**返回：** 布尔值或"空值"

###'字符串'

将值转换为字符串。

**Example**

    
    
    string(42)               // returns "42"
    string(42.5)             // returns "42.5"
    string("regsvr32.exe")   // returns "regsvr32.exe"
    string(true)             // returns "true"
    
    // null handling
    string(null)             // returns null

**Syntax**

    
    
    string(<value>)

**Parameters**

`<value>`

    

(必填)要转换为字符串的值。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数不支持"文本"字段数据类型。

**返回：** 字符串或 'null'

###'字符串包含'

如果源字符串包含提供的子字符串，则返回"true"。默认情况下，匹配区分大小写。

**Example**

    
    
    // process.command_line = "start regsvr32.exe"
    stringContains(process.command_line, "regsvr32")  // returns true
    stringContains(process.command_line, "Regsvr32")  // returns false
    stringContains(process.command_line, "start ")    // returns true
    stringContains(process.command_line, "explorer")  // returns false
    
    // Make matching case-insensitive
    stringContains~(process.command_line, "Regsvr32")  // returns false
    
    // process.name = "regsvr32.exe"
    stringContains(command_line, process.name)        // returns true
    
    // empty strings
    stringContains("", "")                            // returns false
    stringContains(process.command_line, "")          // returns false
    
    // null handling
    stringContains(null, "regsvr32")                  // returns null
    stringContains(process.command_line, null)        // returns null

**Syntax**

    
    
    stringContains(<source>, <substring>)

**Parameters**

`<source>`

     (Required, string or `null`) Source string to search. If `null`, the function returns `null`. 

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

`<substring>`

     (Required, string or `null`) Substring to search for. If `null`, the function returns `null`. 

如果使用字段作为参数，则此参数仅支持以下字段数据类型：

* "关键字"系列中的类型 * 带有"关键字"子字段的"文本"字段

**返回：** 布尔值或"空值"

###'子字符串'

从提供的开始和结束位置的源字符串中提取子字符串。

如果未提供结束位置，则该函数将提取剩余的字符串。

**Example**

    
    
    substring("start regsvr32.exe", 6)        // returns "regsvr32.exe"
    substring("start regsvr32.exe", 0, 5)     // returns "start"
    substring("start regsvr32.exe", 6, 14)    // returns "regsvr32"
    substring("start regsvr32.exe", -4)       // returns ".exe"
    substring("start regsvr32.exe", -4, -1)   // returns ".ex"

**Syntax**

    
    
    substring(<source>, <start_pos>[, <end_pos>])

**Parameters**

`<source>`

     (Required, string) Source string. 
`<start_pos>`

    

(必需，整数)提取的起始位置。

如果此位置高于""<end_pos>位置或""字符串的长度<source>，则该函数返回空字符串。

仓位为零索引。支持负偏移。

`<end_pos>`

    

(可选，整数)用于提取的专用结束位置。如果未提供此位置，则该函数返回剩余的字符串。

仓位为零索引。支持负偏移。

**返回：**字符串

###'减法'

返回提供的减号和减号之间的差值。

**Example**

    
    
    subtract(10, 2)                                          // returns 8
    subtract(10.5, 0.5)                                      // returns 10
    subtract(1, 0.2)                                         // returns 0.8
    subtract(-2, 4)                                          // returns -8
    subtract(-2, -4)                                         // returns 8
    
    // process.args_count = 10
    subtract(process.args_count, 6)                          // returns 4
    subtract(process.args_count, 5)                          // returns 5
    subtract(15, process.args_count)                         // returns 5
    subtract(process.args_count, 0.5)                        // returns 9.5
    
    // process.parent.args_count = 6
    subtract(process.args_count, process.parent.args_count)  // returns 4
    
    // null handling
    subtract(null, 2)                                        // returns null
    subtract(2, null)                                        // returns null

**Syntax**

    
    
    subtract(<minuend>, <subtrahend>)

**Parameters**

`<minuend>`

    

(必需、整数或浮点数或"空")减去减法。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

`<subtrahend>`

    

(可选，整数或浮点数或"空")减去减法。如果为"null"，则函数返回"null"。

如果使用字段作为参数，则此参数仅支持"数字"字段数据类型。

**返回：** 整数、浮点数或"null"

[1] 此参数接受多个参数。

[« EQL syntax reference](eql-syntax.md) [EQL pipe reference »](eql-pipe-
ref.md)
