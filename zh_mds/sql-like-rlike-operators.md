

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Cast Operators](sql-operators-cast.md) [Aggregate Functions »](sql-
functions-aggs.md)

## 喜欢和喜欢

"LIKE"和"RLIKE"运算符通常用于根据字符串模式过滤数据。它们通常作用于放置在运算符左侧的字段，但也可以作用于常量(文字)表达式。运算符的右侧表示模式。两者都可以在"SELECT"语句的"WHERE"子句中使用，但"LIKE"也可以在其他地方使用，例如定义索引模式或跨各种SHOW命令。本节仅涵盖"选择...哪里..."用法。

"LIKE"/"RLIKE"与全文搜索谓词之间的一个显着区别是，前者作用于精确字段，而后者也作用于分析字段。如果与"LIKE"/"RLIKE"一起使用的字段没有精确规范化的子字段(关键字类型)，则Elasticsearch SQL将无法运行查询。如果字段是精确字段或具有精确子字段，它将按原样使用它，或者即使未在语句中显式指定，它也将自动使用确切的子字段。

###'赞'

**Synopsis:**

    
    
    expression        __LIKE constant_exp __

__

|

通常是一个字段或常量表达式 ---|--- __

|

模式**描述**：SQL"LIKE"运算符用于使用通配符将值与类似值进行比较。有两个通配符与"LIKE"运算符一起使用：

* 百分号 (%) * 下划线 (_)

百分号表示零个、一个或多个字符。下划线表示单个数字或字符。这些符号可以用于组合。

没有其他字符具有特殊含义或充当通配符。在其他语言中经常用作通配符的字符("*"或"？")被视为普通字符。

    
    
    SELECT author, name FROM library WHERE name LIKE 'Dune%';
    
        author     |     name
    ---------------+---------------
    Frank Herbert  |Dune
    Frank Herbert  |Dune Messiah

如果需要匹配通配符本身，也可以使用转义字符。这可以通过在"LIKE ..."运算符后使用"ESCAPE [escape_character]"语句来完成：

    
    
    SELECT name, author FROM library WHERE name LIKE 'Dune/%' ESCAPE '/';

在上面的示例中，"/"被定义为一个转义字符，如果需要在模式中专门匹配这些字符，则需要将其放置在"%"或"_"字符之前。默认情况下，没有定义转义字符。

尽管在Elasticsearch SQL中搜索或过滤时，"LIKE"是一个有效的选项，但全文搜索谓词"MATCH"和"QUERY"更快，功能更强大，并且是首选的替代方案。

###'RLIKE'

**Synopsis:**

    
    
    expression         __RLIKE constant_exp __

__

|

通常是一个字段或常量表达式 ---|--- __

|

模式**描述**：此运算符类似于"LIKE"，但用户不限于基于带有百分号('%')和下划线('_')的固定模式搜索字符串;在这种情况下，模式是一个正则表达式，它允许构造更灵活的模式。

有关支持的语法，请参阅_Regular表达式syntax_。

    
    
    SELECT author, name FROM library WHERE name RLIKE 'Child.* Dune';
    
        author     |      name
    ---------------+----------------
    Frank Herbert  |Children of Dune

尽管在Elasticsearch SQL中搜索或过滤时，"RLIKE"是一个有效的选项，但全文搜索谓词"MATCH"和"QUERY"更快，功能更强大，并且是首选的替代方案。

### 首选全文搜索谓词

使用"LIKE"/"RLIKE"时，请考虑使用全文搜索谓词，它们更快，功能更强大，并提供按相关性排序的选项(可以根据它们的匹配程度返回结果)。

例如：

**LIKE/RLIKE**

|

**查询/匹配** ---|--- ''foo LIKE 'bar'''

|

''MATCH(foo， 'bar')'' ''foo LIKE 'bar' 和焦油像 'goo'''

|

''MATCH('foo^2， tar^5'， 'bar goo'， 'operator=and')'' ''foo LIKE 'barr'''

|

''QUERY('foo： bar~')'' 'foo LIKE 'bar' AND tar LIKE 'goo'''

|

''QUERY('foo： bar AND tar： goo')'' ''foo RLIKE 'ba.*'''

|

''MATCH(foo， 'ba'， 'fuzziness=AUTO：1，5')'' ''foo RLIKE 'b.{1}r'''

|

''MATCH(foo， 'br'， 'fuzziness=1')'' « 强制转换运算符聚合函数 »