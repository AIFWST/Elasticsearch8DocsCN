

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« LIKE and RLIKE Operators](sql-like-rlike-operators.md) [Grouping
Functions »](sql-functions-grouping.md)

## 聚合函数

用于从一组输入值计算 _single_ 结果的函数。Elasticsearch SQL仅支持聚合函数和分组(隐式或显式)。

### 通用

###'AVG'

**Synopsis:**

    
    
    AVG(numeric_field) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**说明**：返回输入值的平均值(算术平均值)。

    
    
    SELECT AVG(salary) AS avg FROM emp;
    
          avg
    ---------------
    48248.55
    
    
    SELECT AVG(salary / 12.0) AS avg FROM emp;
    
          avg
    ---------------
    4020.7125

###'计数'

**Synopsis:**

    
    
    COUNT(expression) __

**输入**：

__

|

字段名称、通配符 ('*') 或任何数值。对于"COUNT(*)"或"COUNT()"，<literal>将考虑所有值，包括"null"或缺失值。对于"COUNT(<field_name>)"，"不考虑空"值。   ---|--- **输出**：数值

**说明**：返回输入值的总数(计数)。

    
    
    SELECT COUNT(*) AS count FROM emp;
    
         count
    ---------------
    100

###'计数(全部)'

**Synopsis:**

    
    
    COUNT(ALL field_name) __

**输入**：

__

|

字段名称。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**：数值

**说明**：返回所有_non null_输入值的总数(计数)。"COUNT()"<field_name>和"COUNT(ALL <field_name>)"是等价的。

    
    
    SELECT COUNT(ALL last_name) AS count_all, COUNT(DISTINCT last_name) count_distinct FROM emp;
    
       count_all   |  count_distinct
    ---------------+------------------
    100            |96
    
    
    SELECT COUNT(ALL CASE WHEN languages IS NULL THEN -1 ELSE languages END) AS count_all, COUNT(DISTINCT CASE WHEN languages IS NULL THEN -1 ELSE languages END) count_distinct FROM emp;
    
       count_all   |  count_distinct
    ---------------+---------------
    100            |6

###'计数(不同)'

**Synopsis:**

    
    
    COUNT(DISTINCT field_name) __

**输入**：

__

|

字段名称 ---|--- **输出**：数值。如果此字段仅包含"null"值，则该函数返回"null"。否则，该函数将忽略此字段中的"null"值。

**说明**：返回输入值中_distinct非null_值的总数。

    
    
    SELECT COUNT(DISTINCT hire_date) unique_hires, COUNT(hire_date) AS hires FROM emp;
    
      unique_hires  |     hires
    ----------------+---------------
    99              |100
    
    
    SELECT COUNT(DISTINCT DATE_TRUNC('YEAR', hire_date)) unique_hires, COUNT(DATE_TRUNC('YEAR', hire_date)) AS hires FROM emp;
    
     unique_hires  |     hires
    ---------------+---------------
    14             |100

###'第一/FIRST_VALUE'

**Synopsis:**

    
    
    FIRST(
        field_name               __[, ordering_field_name]) __

**输入**：

__

|

聚合的目标字段 ---|--- __

|

用于排序的可选字段**输出**：与输入类型相同

**说明**：返回按"ordering_field_name"列排序的"field_name"输入列的第一个非"null"值(如果存在)。如果未提供"ordering_field_name"，则仅使用"field_name"列进行排序。例如：

一 |b ---|--- 100

|

1    200

|

1    1

|

2    2

|

2    10

|

空 20

|

空 空

|

空 从 T 中选择第一个 (A)

将导致：

**第一(a)** --- 1 和

    
    
    SELECT FIRST(a, b) FROM t

将导致：

**首(a，b)** --- 100 从 EMP 中选择第一(first_name);          第一(first_name) -------------------- 亚历杭德罗选择性别，第一(first_name)来自 EMP 按性别排序 按性别排序;          性别 |  首(first_name) ------------+-------------------- 空 |  伯尼 F |  亚历杭德罗 M |  Amabile 从 EMP 中选择第一(first_name、birth_date);          第一(first_name，birth_date)-------------------------------- Remzi 选择性别，首先(first_name，birth_date)从EMP组中按性别排序;           性别 |  第一(first_name、birth_date) --------------+-------------------------------- 空 |  莉莲 F |  苏曼特 M |  雷姆齐

"FIRST_VALUE"是一个名称别名，可以用来代替"FIRST"，例如：

    
    
    SELECT gender, FIRST_VALUE(first_name, birth_date) FROM emp GROUP BY gender ORDER BY gender;
    
        gender    |   FIRST_VALUE(first_name, birth_date)
    --------------+--------------------------------------
    null          |   Lillian
    F             |   Sumant
    M             |   Remzi
    
    
    SELECT gender, FIRST_VALUE(SUBSTRING(first_name, 2, 6), birth_date) AS "first" FROM emp GROUP BY gender ORDER BY gender;
    
        gender     |     first
    ---------------+---------------
    null           |illian
    F              |umant
    M              |emzi

"FIRST"不能在 HAVING 子句中使用。

"FIRST"不能与类型为"text"的列一起使用，除非该字段也另存为关键字。

###'最后/LAST_VALUE'

**Synopsis:**

    
    
    LAST(
        field_name               __[, ordering_field_name]) __

**输入**：

__

|

聚合的目标字段 ---|--- __

|

用于排序的可选字段**输出**：与输入类型相同

**描述**：它是"FIRST/FIRST_VALUE"的反义词。返回按"ordering_field_name"列降序排序的"field_name"输入列的最后一个非"null"值(如果存在)。如果未提供"ordering_field_name"，则仅使用"field_name"列进行排序。例如：

一 |b ---|--- 10

|

1    20

|

1    1

|

2    2

|

2    100

|

空 200

|

空 空

|

空 从 T 中选择最后一个 (A)

将导致：

**最后(a)** --- 200 和

    
    
    SELECT LAST(a, b) FROM t

将导致：

**最后(a，b)** --- 2 从 EMP 中选择最后(first_name);          上一篇(first_name) ------------------- 兹冯科 选择性别， 最后(first_name) 来自 EMP 按性别分组 按性别排序;          性别 |  尾页(first_name) ------------+------------------- 空 |  帕特里西奥· |  星林 M |  兹冯科 从 emp 中选择最后(first_name、birth_date);          最后(first_name、birth_date) ------------------------------- 希拉里选择性别， 最后(first_name， birth_date) 从 EMP 分组按性别排序 按性别排序;          性别 |  尾页(first_name、birth_date) -----------+------------------------------- 空 |  埃伯哈特 F |  瓦尔迪奥迪奥 M |  希拉里

"LAST_VALUE"是一个名称别名，可以用来代替"LAST"，例如：

    
    
    SELECT gender, LAST_VALUE(first_name, birth_date) FROM emp GROUP BY gender ORDER BY gender;
    
       gender  |   LAST_VALUE(first_name, birth_date)
    -----------+-------------------------------------
    null       |   Eberhardt
    F          |   Valdiodio
    M          |   Hilari
    
    
    SELECT gender, LAST_VALUE(SUBSTRING(first_name, 3, 8), birth_date) AS "last" FROM emp GROUP BY gender ORDER BY gender;
    
        gender     |     last
    ---------------+---------------
    null           |erhardt
    F              |ldiodio
    M              |lari

"LAST"不能用于"HAVING"子句。

"LAST"不能与"text"类型的列一起使用，除非该字段也"另存为关键字"。

###'最大'

**Synopsis:**

    
    
    MAX(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**：与输入相同类型

**说明**：返回字段"field_name"中输入值的最大值。

    
    
    SELECT MAX(salary) AS max FROM emp;
    
          max
    ---------------
    74999
    
    
    SELECT MAX(ABS(salary / -12.0)) AS max FROM emp;
    
           max
    -----------------
    6249.916666666667

类型为"文本"或"关键字"的字段上的"MAX"被翻译成"LAST/LAST_VALUE"，因此，它不能在"HAVING"子句中使用。

###'分钟'

**Synopsis:**

    
    
    MIN(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**：与输入相同类型

**说明**：返回字段"field_name"中输入值的最小值。

    
    
    SELECT MIN(salary) AS min FROM emp;
    
          min
    ---------------
    25324

类型为"text"或"关键字"的字段上的"MIN"被翻译成"FIRST/FIRST_VALUE"，因此不能在"HAVING"子句中使用。

###'总和'

**Synopsis:**

    
    
    SUM(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**：整数输入为"bigint"，浮点输入为"double"

**说明**：返回字段"field_name"中输入值的总和。

    
    
    SELECT SUM(salary) AS sum FROM emp;
    
          sum
    ---------------
    4824855
    
    
    SELECT ROUND(SUM(salary / 12.0), 1) AS sum FROM emp;
    
          sum
    ---------------
    402071.3

###Statistics

###'骨症'

**Synopsis:**

    
    
    KURTOSIS(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

量化字段"field_name"中输入值分布的形状。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, KURTOSIS(salary) AS k FROM emp;
    
          min      |      max      |        k
    ---------------+---------------+------------------
    25324          |74999          |2.0444718929142986

"KURTOSIS"不能用于标量函数或运算符之上，而只能直接用于字段。因此，例如，不允许以下内容并返回错误：

    
    
     SELECT KURTOSIS(salary / 12.0), gender FROM emp GROUP BY gender

###'疯狂'

**Synopsis:**

    
    
    MAD(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

测量字段"field_name"中输入值的变异性。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, AVG(salary) AS avg, MAD(salary) AS mad FROM emp;
    
          min      |      max      |      avg      |      mad
    ---------------+---------------+---------------+---------------
    25324          |74999          |48248.55       |10096.5
    
    
    SELECT MIN(salary / 12.0) AS min, MAX(salary / 12.0) AS max, AVG(salary/ 12.0) AS avg, MAD(salary / 12.0) AS mad FROM emp;
    
           min        |       max       |      avg      |       mad
    ------------------+-----------------+---------------+-----------------
    2110.3333333333335|6249.916666666667|4020.7125      |841.3750000000002

###'百分位数'

**Synopsis:**

    
    
    PERCENTILE(
        field_name,         __percentile[, __method[, __method_parameter]]) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|---    __

|

数值表达式(必须是常量，而不是基于字段)。如果为"null"，则函数返回"null"。   __

|

百分位数算法近似的可选字符串文本")。可能的值："摘要"或"hdr"。默认为"摘要"。   __

|

配置百分位数算法近似值的可选数字文本")。为"摘要"配置"压缩"或为"hdr"配置"number_of_significant_value_digits"。默认值与支持算法的默认值相同。   **输出**："双精度"数值

**描述**：

返回字段"field_name"中输入值的第 n 个百分位数(由"numeric_exp"参数表示)。

    
    
    SELECT languages, PERCENTILE(salary, 95) AS "95th" FROM emp
           GROUP BY languages;
    
       languages   |      95th
    ---------------+-----------------
    null           |74482.4
    1              |71122.8
    2              |70271.4
    3              |71926.0
    4              |69352.15
    5              |56371.0
    
    
    SELECT languages, PERCENTILE(salary / 12.0, 95) AS "95th" FROM emp
           GROUP BY languages;
    
       languages   |       95th
    ---------------+------------------
    null           |6206.866666666667
    1              |5926.9
    2              |5855.949999999999
    3              |5993.833333333333
    4              |5779.345833333333
    5              |4697.583333333333
    
    
    SELECT
        languages,
        PERCENTILE(salary, 97.3, 'tdigest', 100.0) AS "97.3_TDigest",
        PERCENTILE(salary, 97.3, 'hdr', 3) AS "97.3_HDR"
    FROM emp
    GROUP BY languages;
    
       languages   | 97.3_TDigest    |   97.3_HDR
    ---------------+-----------------+---------------
    null           |74720.036        |74992.0
    1              |72316.132        |73712.0
    2              |71792.436        |69936.0
    3              |73326.23999999999|74992.0
    4              |71753.281        |74608.0
    5              |61176.16000000001|56368.0

###'PERCENTILE_RANK'

**Synopsis:**

    
    
    PERCENTILE_RANK(
        field_name,         __value[, __method[, __method_parameter]]) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|---    __

|

数值表达式(必须是常量，而不是基于字段)。如果为"null"，则函数返回"null"。   __

|

百分位数算法近似的可选字符串文本")。可能的值："摘要"或"hdr"。默认为"摘要"。   __

|

配置百分位数算法近似值的可选数字文本")。为"摘要"配置"压缩"或为"hdr"配置"number_of_significant_value_digits"。默认值与支持算法的默认值相同。   **输出**："双精度"数值

**描述**：

返回字段"field_name"中输入值的第 n 个百分位数(由"numeric_exp"参数表示)。

    
    
    SELECT languages, PERCENTILE_RANK(salary, 65000) AS rank FROM emp GROUP BY languages;
    
       languages   |      rank
    ---------------+-----------------
    null           |73.65766569962062
    1              |73.7291625157734
    2              |88.88005607010643
    3              |79.43662623295829
    4              |85.70446389643493
    5              |96.79075152940749
    
    
    SELECT languages, PERCENTILE_RANK(salary/12, 5000) AS rank FROM emp GROUP BY languages;
    
       languages   |       rank
    ---------------+------------------
    null           |66.91240875912409
    1              |66.70766707667076
    2              |84.13266895048271
    3              |61.052992625621684
    4              |76.55646443990001
    5              |94.00696864111498
    
    
    SELECT
        languages,
        ROUND(PERCENTILE_RANK(salary, 65000, 'tdigest', 100.0), 2) AS "rank_TDigest",
        ROUND(PERCENTILE_RANK(salary, 65000, 'hdr', 3), 2) AS "rank_HDR"
    FROM emp
    GROUP BY languages;
    
       languages   | rank_TDigest  |   rank_HDR
    ---------------+---------------+---------------
    null           |73.66          |80.0
    1              |73.73          |73.33
    2              |88.88          |89.47
    3              |79.44          |76.47
    4              |85.7           |83.33
    5              |96.79          |95.24

###'偏度'

**Synopsis:**

    
    
    SKEWNESS(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

量化字段"field_name"中输入值的不对称分布。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, SKEWNESS(salary) AS s FROM emp;
    
          min      |      max      |        s
    ---------------+---------------+------------------
    25324          |74999          |0.2707722118423227

"偏度"不能在标量函数之上使用，而只能直接用于远场。因此，例如，不允许以下内容并返回错误：

    
    
     SELECT SKEWNESS(ROUND(salary / 12.0, 2), gender FROM emp GROUP BY gender

###'STDDEV_POP'

**Synopsis:**

    
    
    STDDEV_POP(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

返回字段"field_name"中输入值的总体标准偏差。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, STDDEV_POP(salary) AS stddev FROM emp;
    
          min      |      max      |      stddev
    ---------------+---------------+------------------
    25324          |74999          |13765.125502787832
    
    
    SELECT MIN(salary / 12.0) AS min, MAX(salary / 12.0) AS max, STDDEV_POP(salary / 12.0) AS stddev FROM emp;
    
           min        |       max       |     stddev
    ------------------+-----------------+-----------------
    2110.3333333333335|6249.916666666667|1147.093791898986

###'STDDEV_SAMP'

**Synopsis:**

    
    
    STDDEV_SAMP(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

返回字段"field_name"中输入值的示例标准偏差。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, STDDEV_SAMP(salary) AS stddev FROM emp;
    
          min      |      max      |      stddev
    ---------------+---------------+------------------
    25324          |74999          |13834.471662090747
    
    
    SELECT MIN(salary / 12.0) AS min, MAX(salary / 12.0) AS max, STDDEV_SAMP(salary / 12.0) AS stddev FROM emp;
    
           min        |       max       |     stddev
    ------------------+-----------------+-----------------
    2110.3333333333335|6249.916666666667|1152.872638507562

###'SUM_OF_SQUARES'

**Synopsis:**

    
    
    SUM_OF_SQUARES(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

返回字段"field_name"中输入值的平方和。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, SUM_OF_SQUARES(salary) AS sumsq
           FROM emp;
    
          min      |      max      |     sumsq
    ---------------+---------------+----------------
    25324          |74999          |2.51740125721E11
    
    
    SELECT MIN(salary / 24.0) AS min, MAX(salary / 24.0) AS max, SUM_OF_SQUARES(salary / 24.0) AS sumsq FROM emp;
    
           min        |       max        |       sumsq
    ------------------+------------------+-------------------
    1055.1666666666667|3124.9583333333335|4.370488293767361E8

###'VAR_POP'

**Synopsis:**

    
    
    VAR_POP(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

返回字段"field_name"中输入值的总体方差。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, VAR_POP(salary) AS varpop FROM emp;
    
          min      |      max      |     varpop
    ---------------+---------------+----------------
    25324          |74999          |1.894786801075E8
    
    
    SELECT MIN(salary / 24.0) AS min, MAX(salary / 24.0) AS max, VAR_POP(salary / 24.0) AS varpop FROM emp;
    
           min        |       max        |      varpop
    ------------------+------------------+------------------
    1055.1666666666667|3124.9583333333335|328956.04185329855

###'VAR_SAMP'

**Synopsis:**

    
    
    VAR_SAMP(field_name) __

**输入**：

__

|

数值字段。如果此字段仅包含"null"值，则函数返回"null"。否则，该函数将忽略此字段中的"null"值。   ---|--- **输出**："双精度"数值

**描述**：

返回字段"field_name"中输入值的样本方差。

    
    
    SELECT MIN(salary) AS min, MAX(salary) AS max, VAR_SAMP(salary) AS varsamp FROM emp;
    
          min      |      max      |     varsamp
    ---------------+---------------+----------------
    25324          |74999          |1.913926061691E8
    
    
    SELECT MIN(salary / 24.0) AS min, MAX(salary / 24.0) AS max, VAR_SAMP(salary / 24.0) AS varsamp FROM emp;
    
           min        |       max        |     varsamp
    ------------------+------------------+----------------
    1055.1666666666667|3124.9583333333335|332278.830154847

[« LIKE and RLIKE Operators](sql-like-rlike-operators.md) [Grouping
Functions »](sql-functions-grouping.md)
