

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Grouping Functions](sql-functions-grouping.md) [Full-Text Search
Functions »](sql-functions-search.md)

## 日期/时间和间隔函数和运算符

Elasticsearch SQL提供了广泛的工具来执行日期/时间操作。

###Intervals

在处理日期/时间时，一个常见的要求围绕着"间隔"的概念，这是一个值得在Elasticsearch和Elasticsearch SQL上下文中探索的主题。

Elasticsearch 在索引名称和查询中都全面支持日期数学。InsideElasticsearch SQL 通过在表名中传递表达式来支持前者，而后者则通过标准 SQL'INTERVAL' 获得支持。

下表显示了 Elasticsearch 和 Elasticsearch SQL 之间的映射：

**Elasticsearch**

|

**Elasticsearch SQL** ---|--- **Index/Table datetime math** '<index-{now/M{YYYY.MM}}>' **查询日期/时间数学** '1y'

|

"间隔 1 年" "2M"

|

"间隔 2 个月" "3W"

|

"间隔 21 天" "4D"

|

"间隔 4 天" "5 小时"

|

"间隔 5 小时" "6m"

|

"间隔 6 分钟" "7s"

|

"间隔 7 秒""间隔"允许将"年"和"月"混合在一起_或_"天"、"小时"、"分钟"和"秒"。

Elasticsearch SQL也接受每个时间单位的复数形式(例如，"YEAR"和"YEARS"都是有效的)。

以下可能的组合示例：

**Interval**

|

**描述** ---|--- "间隔'1-2'年到月"

|

1年零2个月"间隔'3 4'天到小时'

|

3天4小时"间隔'5 6：12'天到分钟"

|

5 天 6 小时 12 分钟"间隔 '3 4：56：01' 每天到秒"

|

3 天 4 小时 56 分 1 秒"间隔'2 3：45：01.23456789' 天到秒

|

2 天、3 小时、45 分钟、1 秒和 234567890 纳秒"间隔"123：45"小时到分钟"

|

123 小时 45 分钟"间隔'65：43：21.0123'小时到秒"

|

65 小时 43 分 21 秒和 12300000 纳秒"间隔'45：01.23'分钟到秒"

|

45 分钟，1 秒和 230000000 纳秒 ###Comparisonedit

日期/时间字段可以使用相等 ('=') 和 'IN' 运算符与日期数学表达式进行比较：

    
    
    SELECT hire_date FROM emp WHERE hire_date = '1987-03-01||+4y/y';
    
           hire_date
    ------------------------
    1991-01-26T00:00:00.000Z
    1991-10-22T00:00:00.000Z
    1991-09-01T00:00:00.000Z
    1991-06-26T00:00:00.000Z
    1991-08-30T00:00:00.000Z
    1991-12-01T00:00:00.000Z
    
    
    SELECT hire_date FROM emp WHERE hire_date IN ('1987-03-01||+2y/M', '1987-03-01||+3y/M');
    
           hire_date
    ------------------------
    1989-03-31T00:00:00.000Z
    1990-03-02T00:00:00.000Z

###Operators

基本算术运算符("+"、"-"、"*")支持日期/时间参数，如下所示：

    
    
    SELECT INTERVAL 1 DAY + INTERVAL 53 MINUTES AS result;
    
        result
    ---------------
    +1 00:53:00
    
    
    SELECT CAST('1969-05-13T12:34:56' AS DATETIME) + INTERVAL 49 YEARS AS result;
    
           result
    --------------------
    2018-05-13T12:34:56Z
    
    
    SELECT - INTERVAL '49-1' YEAR TO MONTH result;
    
        result
    ---------------
    -49-1
    
    
    SELECT INTERVAL '1' DAY - INTERVAL '2' HOURS AS result;
    
        result
    ---------------
    +0 22:00:00
    
    
    SELECT CAST('2018-05-13T12:34:56' AS DATETIME) - INTERVAL '2-8' YEAR TO MONTH AS result;
    
           result
    --------------------
    2015-09-13T12:34:56Z
    
    
    SELECT -2 * INTERVAL '3' YEARS AS result;
    
        result
    ---------------
    -6-0

###Functions

以日期/时间为目标的函数。

###'CURRENT_DATE/CURDATE'

**Synopsis:**

    
    
    CURRENT_DATE
    CURRENT_DATE()
    CURDATE()

**输入** ： _无_

**输出**：日期

**说明**：返回当前查询到达服务器的日期(无时间部分)。它既可以用作关键字："CURRENT_DATE"，也可以用作没有参数的函数："CURRENT_DATE()"。

与CURRENT_DATE不同，'CURDATE()' 只能用作带有 noarguments 的函数，而不能用作关键字。

此方法始终为同一查询中的每次匹配返回相同的值。

    
    
    SELECT CURRENT_DATE AS result;
    
             result
    ------------------------
    2018-12-12
    
    
    SELECT CURRENT_DATE() AS result;
    
             result
    ------------------------
    2018-12-12
    
    
    SELECT CURDATE() AS result;
    
             result
    ------------------------
    2018-12-12

通常，此函数(及其孪生 TODAY())函数用于相对日期筛选：

    
    
    SELECT first_name FROM emp WHERE hire_date > TODAY() - INTERVAL 35 YEARS ORDER BY first_name ASC LIMIT 5;
    
     first_name
    ------------
    Alejandro
    Amabile
    Anneke
    Anoosh
    Basil

###'CURRENT_TIME/CURTIME'

**Synopsis:**

    
    
    CURRENT_TIME
    CURRENT_TIME([precision]) __CURTIME

**输入**：

__

|

小数位数;可选 ---|--- **输出**：时间

**说明**：返回当前查询到达服务器的时间。作为一个函数，'CURRENT_TIME()' 接受 _precision_ 作为用于舍入第二个小数位数(纳秒)的可选参数。default_precision_为 3，这意味着将返回毫秒级精度电流时间。

此方法始终为同一查询中的每次匹配返回相同的值。

    
    
    SELECT CURRENT_TIME AS result;
    
             result
    ------------------------
    12:31:27.237Z
    
    
    SELECT CURRENT_TIME() AS result;
    
             result
    ------------------------
    12:31:27.237Z
    
    
    SELECT CURTIME() AS result;
    
             result
    ------------------------
    12:31:27.237Z
    
    
    SELECT CURRENT_TIME(1) AS result;
    
             result
    ------------------------
    12:31:27.2Z

通常，此函数用于相对日期/时间筛选：

    
    
    SELECT first_name FROM emp WHERE CAST(hire_date AS TIME) > CURRENT_TIME() - INTERVAL 20 MINUTES ORDER BY first_name ASC LIMIT 5;
    
      first_name
    ---------------
    Alejandro
    Amabile
    Anneke
    Anoosh
    Arumugam

目前，使用大于 6 的 _precision_ 不会对函数的输出产生任何影响，因为返回的秒小数位数的最大数为 6。

###'CURRENT_TIMESTAMP'

**Synopsis:**

    
    
    CURRENT_TIMESTAMP
    CURRENT_TIMESTAMP([precision]) __

**输入**：

__

|

小数位数;可选---|--- **输出**：日期/时间

**说明**：返回当前查询到达服务器的日期/时间。作为一个函数，'CURRENT_TIMESTAMP()' 接受 _precision_ 作为用于舍入第二个小数位数(纳秒)的可选参数。默认值 _precision_ 为 3，表示将返回毫秒精度的当前日期/时间。

此方法始终为同一查询中的每次匹配返回相同的值。

    
    
    SELECT CURRENT_TIMESTAMP AS result;
    
             result
    ------------------------
    2018-12-12T14:48:52.448Z
    
    
    SELECT CURRENT_TIMESTAMP() AS result;
    
             result
    ------------------------
    2018-12-12T14:48:52.448Z
    
    
    SELECT CURRENT_TIMESTAMP(1) AS result;
    
             result
    ------------------------
    2018-12-12T14:48:52.4Z

通常，此函数(及其孪生 NOW())函数用于相对日期/时间筛选：

    
    
    SELECT first_name FROM emp WHERE hire_date > NOW() - INTERVAL 100 YEARS ORDER BY first_name ASC LIMIT 5;
    
      first_name
    ---------------
    Alejandro
    Amabile
    Anneke
    Anoosh
    Arumugam

目前，使用大于 6 的 _precision_ 不会对函数的输出产生任何影响，因为返回的秒小数位数的最大数为 6。

###'DATE_ADD/DATEADD/TIMESTAMP_ADD/TIMESTAMPADD'

**Synopsis:**

    
    
    DATE_ADD(
        string_exp, __integer_exp, __datetime_exp) __

**输入**：

__

|

字符串表达式，表示要添加到日期/日期时间的日期/时间单位。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式表示上述单位应添加到日期/日期时间的次数，如果使用负值，则会导致从日期/日期时间中减去。如果为"null"，则函数返回"null"。   __

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   **输出**：日期时间

**描述**：将给定数量的日期/时间单位添加到日期/日期时间。如果单位数为负数，则从日期/日期时间中减去。

如果第二个参数是长整型，则有可能被截断，因为将从该长值中提取和使用整数值。

要添加/减去的日期时间单位---**单位**

|

**缩写**年份

|

年， 年， 年年 季度

|

季度、QQ、Q 月

|

月， 毫米， 米 一年中的一天

|

哎呀，哎呀

|

天， 日， 天， 天周

|

周， 周， WW 工作日

|

工作日，DW 小时

|

小时，小时 分钟

|

分钟，英里，n 秒

|

秒， ss， s 毫秒

|

毫秒，毫秒微秒

|

微秒，微秒纳秒

|

纳秒， ns 选择 DATE_ADD('年'， 10， '2019-09-04T11：22：33.000Z'：:d atetime) 作为 "+10 年";             +10 年 ------------------------ 2029-09-04T11：22：33.000Z 选择 DATE_ADD("周"， 10， '2019-09-04T11：22：33.000Z'：:d atetime) 作为"+10 周";             +10 周 ------------------------ 2019-11-13T11：22：33.000Z 选择 DATE_ADD("秒"， -1234， '2019-09-04T11：22：33.000Z'：:d atetime) 作为"-1234 秒";             -1234 秒 ------------------------ 2019-09-04T11：01：59.000Z 选择 DATE_ADD('qq'， -417， '2019-09-04'：:d ate) AS "-417 季度";             -417 季度 ------------------------ 1915-06-04T00：00：00.000Z 选择 DATE_ADD("分钟"， 9235， "2019-09-04"：:d ate) 作为"+9235 分钟";             +9235分钟 ------------------------ 2019-09-10T09：55：00.000Z

###'DATE_DIFF/DATEDIFF/TIMESTAMP_DIFF/TIMESTAMPDIFF'

**Synopsis:**

    
    
    DATE_DIFF(
        string_exp, __datetime_exp, __datetime_exp) __

**输入**：

__

|

字符串表达式，表示以下两个日期/日期时间表达式之间的日期/时间单位差异。如果为"null"，则函数返回"null"。   ---|---    __

|

开始日期/日期时间表达式。如果为"null"，则函数返回"null"。   __

|

结束日期/日期时间表达式。如果为"null"，则函数返回"null"。   **输出**：整数

**描述**：从第三个参数中减去第二个参数，并以第一个参数中指定的单位的倍数返回它们的差值。如果第二个参数(开始)大于第三个参数(结束)，则返回负值。

日期时间差异单位 --- **单位**

|

**缩写**年份

|

年， 年， 年年 季度

|

季度、QQ、Q 月

|

月， 毫米， 米 一年中的一天

|

哎呀，哎呀

|

天， 日， 天， 天周

|

周， 周， WW 工作日

|

工作日，DW 小时

|

小时，小时 分钟

|

分钟，英里，n 秒

|

秒， ss， s 毫秒

|

毫秒，毫秒微秒

|

微秒，微秒纳秒

|

纳秒，ns SELECT DATE_DIFF('年'， '2019-09-04T11：22：33.000Z'：:d atetime， '2032-09-04T22：33：11.000Z'：:d atetime) AS "diffInYears";             diffInYears ------------------------ 13 SELECT DATE_DIFF('week'， '2019-09-04T11：22：33.000Z'：:d atetime， '2016-12-08T22：33：11.000Z'：:d atetime) AS "diffInWeek";             diffInWeek ------------------------ -143 SELECT DATE_DIFF('秒'， '2019-09-04T11：22：33.123Z'：:d atetime， '2019-07-12T22：33：11.321Z'：:d atetime) AS "diffInSeconds";             diffInSeconds ------------------------ -4625362 SELECT DATE_DIFF('qq'， '2019-09-04'：:d ate， '2025-04-25'：:d ate) AS "diffInQuarters";             差异季度 ------------------------ 23

对于"小时"和"分钟"，"DATEDIFF"不进行任何舍入，而是首先将 2 个日期上更详细的时间字段截断为零，然后计算减法。

    
    
    SELECT DATEDIFF('hours', '2019-11-10T12:10:00.000Z'::datetime, '2019-11-10T23:59:59.999Z'::datetime) AS "diffInHours";
    
          diffInHours
    ------------------------
    11
    
    
    SELECT DATEDIFF('minute', '2019-11-10T12:10:00.000Z'::datetime, '2019-11-10T12:15:59.999Z'::datetime) AS "diffInMinutes";
    
          diffInMinutes
    ------------------------
    5
    
    
    SELECT DATE_DIFF('minutes', '2019-09-04'::date, '2015-08-17T22:33:11.567Z'::datetime) AS "diffInMinutes";
    
          diffInMinutes
    ------------------------
    -2128407

###'DATE_FORMAT'

**Synopsis:**

    
    
    DATE_FORMAT(
        date_exp/datetime_exp/time_exp, __string_exp) __

**输入**：

__

|

日期/日期时间/时间表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

格式模式。如果为"null"或空字符串，则该函数返回"null"。   **输出**：字符串

**说明**：使用第二个参数中指定的格式以字符串形式返回日期/日期时间/时间。格式化模式是 MySQL DATE_FORMAT() 函数中使用的说明符之一。

如果第一个参数的类型是"time"，则第二个参数指定的模式不能包含与日期相关的单位(例如 _dd_ 、_MM_、_yyyy_ 等)。如果它包含此类单位，则返回错误。月份和日期说明符(%c，%D，%d，%e，%m)的范围从1开始，与MySQL不同，它们从零开始，因为MySQL允许存储不完整的日期，例如_2014-00-00_。在这种情况下，Elasticsearch 返回一个错误。

    
    
    SELECT DATE_FORMAT(CAST('2020-04-05' AS DATE), '%d/%m/%Y') AS "date";
    
          date
    ------------------
    05/04/2020
    
    
    SELECT DATE_FORMAT(CAST('2020-04-05T11:22:33.987654' AS DATETIME), '%d/%m/%Y %H:%i:%s.%f') AS "datetime";
    
          datetime
    ------------------
    05/04/2020 11:22:33.987654
    
    
    SELECT DATE_FORMAT(CAST('23:22:33.987' AS TIME), '%H %i %s.%f') AS "time";
    
          time
    ------------------
    23 22 33.987000

###'DATE_PARSE'

**Synopsis:**

    
    
    DATE_PARSE(
        string_exp, __string_exp) __

**输入**：

__

|

字符串形式的日期表达式。如果为"null"或空字符串，则该函数返回"null"。   ---|---    __

|

解析模式。如果为"null"或空字符串，则该函数返回"null"。   **输出**：日期

**说明**：通过使用第二个参数中指定的格式分析第一个参数来返回日期。使用的解析格式模式是来自'java.time.format.DateTimeFormatter'的模式。

如果解析模式不包含所有有效的日期单位(例如 _HH：mm：ss_、_dd-MM HH：mm：ss_ 等)，则会返回错误，因为函数需要返回包含日期部分的"date"类型的值。

    
    
    SELECT DATE_PARSE('07/04/2020', 'dd/MM/yyyy') AS "date";
    
       date
    -----------
    2020-04-07

生成的"日期"将具有用户通过"time_zone"/"时区"REST/驱动程序参数指定的时区，并且不应用转换。

    
    
    {
        "query" : "SELECT DATE_PARSE('07/04/2020', 'dd/MM/yyyy') AS \"date\"",
        "time_zone" : "Europe/Athens"
    }
    
       date
    ------------
    2020-04-07T00:00:00.000+03:00

###'DATETIME_FORMAT'

**Synopsis:**

    
    
    DATETIME_FORMAT(
        date_exp/datetime_exp/time_exp, __string_exp) __

**输入**：

__

|

日期/日期时间/时间表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

格式模式。如果为"null"或空字符串，则该函数返回"null"。   **输出**：字符串

**说明**：使用第二个参数中指定的格式以字符串形式返回日期/日期时间/时间。使用的格式模式是来自'java.time.format.DateTimeFormatter'的格式模式。

如果第一个参数的类型是"time"，则第二个参数指定的模式不能包含与日期相关的单位(例如 _dd_ 、_MM_、_yyyy_ 等)。如果它包含此类单位，则返回错误。

    
    
    SELECT DATETIME_FORMAT(CAST('2020-04-05' AS DATE), 'dd/MM/yyyy') AS "date";
    
          date
    ------------------
    05/04/2020
    
    
    SELECT DATETIME_FORMAT(CAST('2020-04-05T11:22:33.987654' AS DATETIME), 'dd/MM/yyyy HH:mm:ss.SS') AS "datetime";
    
          datetime
    ------------------
    05/04/2020 11:22:33.98
    
    
    SELECT DATETIME_FORMAT(CAST('11:22:33.987' AS TIME), 'HH mm ss.S') AS "time";
    
          time
    ------------------
    11 22 33.9

###'DATETIME_PARSE'

**Synopsis:**

    
    
    DATETIME_PARSE(
        string_exp, __string_exp) __

**输入**：

__

|

字符串形式的日期时间表达式。如果为"null"或空字符串，则该函数返回"null"。   ---|---    __

|

解析模式。如果为"null"或空字符串，则该函数返回"null"。   **输出**：日期时间

**说明**：通过使用第二个参数中指定的格式解析第一个参数来返回日期时间。使用的解析格式模式是来自'java.time.format.DateTimeFormatter'的模式。

如果解析模式仅包含日期或仅包含时间单位(e.g._dd/MM/yyyy_、_HH：mm：ss_ 等)，则会返回错误，因为函数需要返回必须同时包含两者的"datetime"类型的值。

    
    
    SELECT DATETIME_PARSE('07/04/2020 10:20:30.123', 'dd/MM/yyyy HH:mm:ss.SSS') AS "datetime";
    
          datetime
    ------------------------
    2020-04-07T10:20:30.123Z
    
    
    SELECT DATETIME_PARSE('10:20:30 07/04/2020 Europe/Berlin', 'HH:mm:ss dd/MM/yyyy VV') AS "datetime";
    
          datetime
    ------------------------
    2020-04-07T08:20:30.000Z

如果未在日期时间字符串表达式和解析模式中指定时区，则生成的"日期时间"将具有用户通过"time_zone"/"时区"REST/驱动程序参数指定的时区，并且不应用转换。

    
    
    {
        "query" : "SELECT DATETIME_PARSE('10:20:30 07/04/2020', 'HH:mm:ss dd/MM/yyyy') AS \"datetime\"",
        "time_zone" : "Europe/Athens"
    }
    
          datetime
    -----------------------------
    2020-04-07T10:20:30.000+03:00

###'TIME_PARSE'

**Synopsis:**

    
    
    TIME_PARSE(
        string_exp, __string_exp) __

**输入**：

__

|

字符串形式的时间表达式。如果为"null"或空字符串，则该函数返回"null"。   ---|---    __

|

解析模式。如果为"null"或空字符串，则该函数返回"null"。   **输出**：时间

**说明**：通过使用第二个参数中指定的格式解析第一个参数来返回时间。使用的解析格式模式是来自'java.time.format.DateTimeFormatter'的模式。

如果解析模式仅包含日期单位(例如 _dd/MM/yyyy_)，则返回错误，因为函数需要返回仅包含时间的"time"类型的值。

    
    
    SELECT TIME_PARSE('10:20:30.123', 'HH:mm:ss.SSS') AS "time";
    
         time
    ---------------
    10:20:30.123Z
    
    
    SELECT TIME_PARSE('10:20:30-01:00', 'HH:mm:ssXXX') AS "time";
    
         time
    ---------------
    11:20:30.000Z

如果未在时间字符串表达式和分析模式中指定时区，则生成的"time"将具有用户在Unix纪元日期("1970-01-01")通过"time_zone"/"时区"REST/驱动程序参数指定的时区的偏移量，并且不应用转换。

    
    
    {
        "query" : "SELECT DATETIME_PARSE('10:20:30', 'HH:mm:ss') AS \"time\"",
        "time_zone" : "Europe/Athens"
    }
    
          time
    ------------------------------------
    10:20:30.000+02:00

###'DATE_PART/日期部分'

**Synopsis:**

    
    
    DATE_PART(
        string_exp, __datetime_exp) __

**输入**：

__

|

字符串表达式，表示要从日期/日期时间中提取的单位。如果为"null"，则函数返回"null"。   ---|---    __

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   **输出**：整数

**描述**：从日期/日期时间中提取指定的单位。它类似于"EXTRACT"，但单位的名称和别名不同，并提供了更多选项(例如："TZOFFSET")。

要提取---日期时间单位**单位**

|

**缩写**年份

|

年， 年， 年年 季度

|

季度、QQ、Q 月

|

月， 毫米， 米 一年中的一天

|

哎呀，哎呀

|

天， 日， 天， 天周

|

周， 周， WW 工作日

|

工作日，DW 小时

|

小时，小时 分钟

|

分钟，英里，n 秒

|

秒， ss， s 毫秒

|

毫秒，毫秒微秒

|

微秒，微秒纳秒

|

纳秒，纳秒

|

tz 选择 DATE_PART('year'， '2019-09-22T11：22：33.123Z'：:d atetime) 作为"年";          年---------- 2019 选择DATE_PART('mi'， '2019-09-04T11：22：33.123Z'：:d atetime) AS mins;          分钟 ----------- 22 选择 DATE_PART("季度"，投射("2019-09-24' 作为日期))作为季度;          季度 ------------- 3 选择 DATE_PART("月"，投射("2019-09-24"作为日期))作为月份;          -------------月9日

对于"周"和"工作日"，使用非ISO计算提取单位，这意味着给定的一周被视为从星期日开始，而不是星期一。

    
    
    SELECT DATE_PART('week', '2019-09-22T11:22:33.123Z'::datetime) AS week;
    
       week
    ----------
    39

"tzoffset"返回表示时区偏移量的总分钟数(有符号)。

    
    
    SELECT DATE_PART('tzoffset', '2019-09-04T11:22:33.123+05:15'::datetime) AS tz_mins;
    
       tz_mins
    --------------
    315
    
    
    SELECT DATE_PART('tzoffset', '2019-09-04T11:22:33.123-03:49'::datetime) AS tz_mins;
    
       tz_mins
    --------------
    -229

###'DATE_TRUNC/DATETRUNC'

**Synopsis:**

    
    
    DATE_TRUNC(
        string_exp, __datetime_exp/interval_exp) __

**输入**：

__

|

字符串表达式，表示日期/日期时间/间隔应截断到的单位。如果为"null"，则函数返回"null"。   ---|---    __

|

日期/日期时间/间隔表达式。如果为"null"，则函数返回"null"。   **输出**：日期时间/间隔

**描述**：将所有低于指定字段的字段截断为指定单位的日期/日期时间/间隔为零(或一，表示天、星期几和月)。如果第一个参数是"周"，第二个参数是"间隔"类型，则会引发错误，因为"间隔"数据类型不支持"周"时间单位。

日期时间截断单位 --- **单位**

|

**缩写**千年

|

千年世纪

|

世纪十年

|

十年年

|

年， 年， 年年 季度

|

季度、QQ、Q 月

|

月， 月， 米周

|

周， 周， WW日

|

天， 日， 天， 小时

|

小时，小时 分钟

|

分钟，英里，n 秒

|

秒， ss， s 毫秒

|

毫秒，毫秒微秒

|

微秒，微秒纳秒

|

纳秒， ns 选择 DATE_TRUNC('千年'， '2019-09-04T11：22：33.123Z'：:d atetime) 作为千年;             千年------------------------ 2000-01-01T00：00：00.000Z 选择日期TRUNC("周"，"2019-08-24T11：22：33.123Z"：:d atetime) AS 周;             第 ------------------------ 周 2019-08-19T00：00：00.000Z 选择 DATE_TRUNC('mi'， '2019-09-04T11：22：33.123Z'：:d atetime) AS mins;             分钟------------------------ 2019-09-04T11：22：00.000Z 选择DATE_TRUNC("十年"，投射("2019-09-04"作为日期))作为十年;             几十年 ------------------------ 2010-01-01T00：00：00.000Z 选择日期TRUNC("季度"，投射("2019-09-04"作为日期))作为季度;             季度 ------------------------ 2019-07-01T00：00：00.000Z 选择DATE_TRUNC("世纪"，间隔"199-5"年到月)作为世纪;             世纪 ------------------ +100-0 选择 DATE_TRUNC("小时"，间隔"17 22：13：12"天到秒)作为小时;             小时 ------------------ +17 22：00：00 选择DATE_TRUNC("天"，间隔"19 15：24：19"天到秒)作为天;             第------------------天 +19 00：00：00

###'格式'

**Synopsis:**

    
    
    FORMAT(
        date_exp/datetime_exp/time_exp, __string_exp) __

**输入**：

__

|

日期/日期时间/时间表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

格式模式。如果为"null"或空字符串，则该函数返回"null"。   **输出**：字符串

**说明**：使用第二个参数中指定的格式以字符串形式返回日期/日期时间/时间。使用的格式模式是 SQL Server FormatSpecification Microsoft 中的格式模式。

如果第一个参数的类型是"time"，则第二个参数指定的模式不能包含与日期相关的单位(例如 _dd_ 、_MM_、_yyyy_ 等)。如果它包含此类单位，则返回错误。 格式说明符"F"的工作方式与格式说明符"f"类似。它将返回秒的小数部分，并且位数将与作为输入提供的"Fs"数量相同(最多 9 位)。结果将包含末尾附加的"0"，以匹配提供的"F"数。例如：对于时间部分 '10：20：30.1234' 和模式 'HH：mm：ss。FFFFFF"，函数的输出字符串将为："10：20：30.123400"。 格式说明符"y"将返回纪元年份，而不是一个/两个低位数字。例如：对于"2009"，"y"将返回"2009"而不是"9"。对于年份"43"，"y"格式说明符将返回"43"。\- 特殊字符，如"""、"\"和"%"将按原样返回，没有任何更改。例如：将日期"2020 年 9 月 17 日"格式化为"%M"将返回"%9"

    
    
    SELECT FORMAT(CAST('2020-04-05' AS DATE), 'dd/MM/yyyy') AS "date";
    
          date
    ------------------
    05/04/2020
    
    
    SELECT FORMAT(CAST('2020-04-05T11:22:33.987654' AS DATETIME), 'dd/MM/yyyy HH:mm:ss.ff') AS "datetime";
    
          datetime
    ------------------
    05/04/2020 11:22:33.98
    
    
    SELECT FORMAT(CAST('11:22:33.987' AS TIME), 'HH mm ss.f') AS "time";
    
          time
    ------------------
    11 22 33.9

###'TO_CHAR'

**Synopsis:**

    
    
    TO_CHAR(
        date_exp/datetime_exp/time_exp, __string_exp) __

**输入**：

__

|

日期/日期时间/时间表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

格式模式。如果为"null"或空字符串，则该函数返回"null"。   **输出**：字符串

**说明**：使用第二个参数中指定的格式以字符串形式返回日期/日期时间/时间。格式模式符合 PostgreSQLTemplate Patterns for Date/TimeFormatting。

如果第一个参数的类型是"time"，则第二个参数指定的模式不能包含与日期相关的单位(例如 _dd_ 、_MM_、_YYYY_ 等)。如果它包含此类单位，则返回错误。 在某些情况下，模式"TZ"和"tz"(时区缩写)的结果与PostgreSQL中"TO_CHAR"返回的结果不同。原因是JDK指定的时区缩写与PostgreSQL指定的时区缩写不同。此函数可能会显示实际的时区缩写，而不是 PostgreSQL 实现返回的通用"LMT"或空字符串或偏移量。两种实现之间的夏令日/日光标记也可能有所不同(例如，夏威夷将显示"HT"而不是"HST")。 不支持"FX"、"TM"、"SP"模式修饰符，将在输出中显示为"FX"、"TM"、"SP"文本。

    
    
    SELECT TO_CHAR(CAST('2020-04-05' AS DATE), 'DD/MM/YYYY') AS "date";
    
          date
    ------------------
    05/04/2020
    
    
    SELECT TO_CHAR(CAST('2020-04-05T11:22:33.987654' AS DATETIME), 'DD/MM/YYYY HH24:MI:SS.FF2') AS "datetime";
    
          datetime
    ------------------
    05/04/2020 11:22:33.98
    
    
    SELECT TO_CHAR(CAST('23:22:33.987' AS TIME), 'HH12 MI SS.FF1') AS "time";
    
          time
    ------------------
    11 22 33.9

###'DAY_OF_MONTH/DOM/DAY'

**Synopsis:**

    
    
    DAY_OF_MONTH(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取月份中的某天。

    
    
    SELECT DAY_OF_MONTH(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS day;
    
          day
    ---------------
    19

###'DAY_OF_WEEK/星期/道琼斯指数'

**Synopsis:**

    
    
    DAY_OF_WEEK(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取星期几。星期天是"1"，星期一是"2"，依此类推。

    
    
    SELECT DAY_OF_WEEK(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS day;
    
          day
    ---------------
    2

###'DAY_OF_YEAR/DOY'

**Synopsis:**

    
    
    DAY_OF_YEAR(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取一年中的某一天。

    
    
    SELECT DAY_OF_YEAR(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS day;
    
          day
    ---------------
    50

###'DAY_NAME/DAYNAME'

**Synopsis:**

    
    
    DAY_NAME(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**描述**：从文本格式的日期/日期时间中提取星期几("星期一"，"星期二"...

    
    
    SELECT DAY_NAME(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS day;
    
          day
    ---------------
    Monday

###'HOUR_OF_DAY/小时'

**Synopsis:**

    
    
    HOUR_OF_DAY(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取一天中的小时。

    
    
    SELECT HOUR_OF_DAY(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS hour;
    
         hour
    ---------------
    10

###'ISO_DAY_OF_WEEK/ISODAYOFWEEK/ISODOW/IDOW'

**Synopsis:**

    
    
    ISO_DAY_OF_WEEK(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：按照ISO 8601标准从日期/日期时间中提取星期几。星期一是"1"，星期二是"2"，依此类推。

    
    
    SELECT ISO_DAY_OF_WEEK(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS day;
    
          day
    ---------------
    1

###'ISO_WEEK_OF_YEAR/ISOWEEKOFYEAR/ISOWEEK/IWOY/IW'

**Synopsis:**

    
    
    ISO_WEEK_OF_YEAR(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：按照ISO 8601标准从日期/日期时间中提取一年中的一周。一年的第一周是一月份大部分时间(4 天或更多)的第一周。

    
    
    SELECT ISO_WEEK_OF_YEAR(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS week;
    
         week
    ---------------
    8

###'MINUTE_OF_DAY'

**Synopsis:**

    
    
    MINUTE_OF_DAY(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取一天中的分钟。

    
    
    SELECT MINUTE_OF_DAY(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS minute;
    
        minute
    ---------------
    623

###'MINUTE_OF_HOUR/分钟'

**Synopsis:**

    
    
    MINUTE_OF_HOUR(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取小时中的分钟。

    
    
    SELECT MINUTE_OF_HOUR(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS minute;
    
        minute
    ---------------
    23

###'MONTH_OF_YEAR/月'

**Synopsis:**

    
    
    MONTH(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取一年中的月份。

    
    
    SELECT MONTH_OF_YEAR(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS month;
    
         month
    ---------------
    2

###'MONTH_NAME/月名'

**Synopsis:**

    
    
    MONTH_NAME(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**描述**：从文本格式的日期/日期时间中提取月份("一月"，"二月"...

    
    
    SELECT MONTH_NAME(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS month;
    
         month
    ---------------
    February

###'现在'

**Synopsis:**

    
    
    NOW()

**输入** ： _无_

**输出**：日期时间

**描述**：此函数提供相同的功能 asCURRENT_TIMESTAMP() 函数：返回当前查询到达服务器的日期时间。此方法始终为同一查询中的每个匹配项返回相同的值。

    
    
    SELECT NOW() AS result;
    
             result
    ------------------------
    2018-12-12T14:48:52.448Z

通常，此函数(及其孪生CURRENT_TIMESTAMP())函数用于相对日期/时间筛选：

    
    
    SELECT first_name FROM emp WHERE hire_date > NOW() - INTERVAL 100 YEARS ORDER BY first_name ASC LIMIT 5;
    
      first_name
    ---------------
    Alejandro
    Amabile
    Anneke
    Anoosh
    Arumugam

###'SECOND_OF_MINUTE/秒'

**Synopsis:**

    
    
    SECOND_OF_MINUTE(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取分钟秒。

    
    
    SELECT SECOND_OF_MINUTE(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS second;
    
        second
    ---------------
    27

###'季度'

**Synopsis:**

    
    
    QUARTER(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：提取日期/日期时间所在的季度。

    
    
    SELECT QUARTER(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS quarter;
    
        quarter
    ---------------
    1

###"今天"

**Synopsis:**

    
    
    TODAY()

**输入** ： _无_

**输出**：日期

**描述**：此函数提供相同的功能 asCURRENT_DATE() 函数：返回当前查询到达服务器的日期。此方法始终为同一查询中的每次出现返回相同的值。

    
    
    SELECT TODAY() AS result;
    
             result
    ------------------------
    2018-12-12

通常，此函数(及其孪生CURRENT_TIMESTAMP())函数用于相对日期筛选：

    
    
    SELECT first_name FROM emp WHERE hire_date > TODAY() - INTERVAL 35 YEARS ORDER BY first_name ASC LIMIT 5;
    
     first_name
    ------------
    Alejandro
    Amabile
    Anneke
    Anoosh
    Basil

###'WEEK_OF_YEAR/周'

**Synopsis:**

    
    
    WEEK_OF_YEAR(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取一年中的一周。

    
    
    SELECT WEEK(CAST('1988-01-05T09:22:10Z' AS TIMESTAMP)) AS week, ISOWEEK(CAST('1988-01-05T09:22:10Z' AS TIMESTAMP)) AS isoweek;
    
          week     |   isoweek
    ---------------+---------------
    2              |1

###'年'

**Synopsis:**

    
    
    YEAR(datetime_exp) __

**输入**：

__

|

日期/日期时间表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数

**描述**：从日期/日期时间中提取年份。

    
    
    SELECT YEAR(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS year;
    
         year
    ---------------
    2018

###'摘录'

**Synopsis:**

    
    
    EXTRACT(
        datetime_function  __FROM datetime_exp) __

**输入**：

__

|

日期/时间函数名称 ---|--- __

|

日期/日期时间表达式 **输出** ： 整数

**描述**：通过指定日期时间函数的名称从日期/日期时间中提取字段。以下

    
    
    SELECT EXTRACT(DAY_OF_YEAR FROM CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS day;
    
          day
    ---------------
    50

相当于

    
    
    SELECT DAY_OF_YEAR(CAST('2018-02-19T10:23:27Z' AS TIMESTAMP)) AS day;
    
          day
    ---------------
    50

[« Grouping Functions](sql-functions-grouping.md) [Full-Text Search
Functions »](sql-functions-search.md)
