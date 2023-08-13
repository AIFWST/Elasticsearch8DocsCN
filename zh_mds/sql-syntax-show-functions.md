

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL Language](sql-spec.md)

[« SHOW COLUMNS](sql-syntax-show-columns.md) [SHOW TABLES »](sql-syntax-
show-tables.md)

## 显示函数

**Synopsis:**

    
    
    SHOW FUNCTIONS [LIKE pattern]? __

__

|

SQL 匹配模式 ---|--- **描述**：列出所有 SQL 函数及其类型。"LIKE"子句可用于将名称列表限制为给定模式。

    
    
    SHOW FUNCTIONS;
    
          name       |     type
    -----------------+---------------
    AVG              |AGGREGATE
    COUNT            |AGGREGATE
    FIRST            |AGGREGATE
    FIRST_VALUE      |AGGREGATE
    LAST             |AGGREGATE
    LAST_VALUE       |AGGREGATE
    MAX              |AGGREGATE
    MIN              |AGGREGATE
    SUM              |AGGREGATE
    KURTOSIS         |AGGREGATE
    MAD              |AGGREGATE
    PERCENTILE       |AGGREGATE
    PERCENTILE_RANK  |AGGREGATE
    SKEWNESS         |AGGREGATE
    STDDEV_POP       |AGGREGATE
    STDDEV_SAMP      |AGGREGATE
    SUM_OF_SQUARES   |AGGREGATE
    VAR_POP          |AGGREGATE
    VAR_SAMP         |AGGREGATE
    HISTOGRAM        |GROUPING
    CASE             |CONDITIONAL
    COALESCE         |CONDITIONAL
    GREATEST         |CONDITIONAL
    IFNULL           |CONDITIONAL
    IIF              |CONDITIONAL
    ISNULL           |CONDITIONAL
    LEAST            |CONDITIONAL
    NULLIF           |CONDITIONAL
    NVL              |CONDITIONAL
    CURDATE          |SCALAR
    CURRENT_DATE     |SCALAR
    CURRENT_TIME     |SCALAR
    CURRENT_TIMESTAMP|SCALAR
    CURTIME          |SCALAR
    DATEADD          |SCALAR
    DATEDIFF         |SCALAR
    DATEPART         |SCALAR
    DATETIME_FORMAT  |SCALAR
    DATETIME_PARSE   |SCALAR
    DATETRUNC        |SCALAR
    DATE_ADD         |SCALAR
    DATE_DIFF        |SCALAR
    DATE_FORMAT      |SCALAR
    DATE_PARSE       |SCALAR
    DATE_PART        |SCALAR
    DATE_TRUNC       |SCALAR
    DAY              |SCALAR
    DAYNAME          |SCALAR
    DAYOFMONTH       |SCALAR
    DAYOFWEEK        |SCALAR
    DAYOFYEAR        |SCALAR
    DAY_NAME         |SCALAR
    DAY_OF_MONTH     |SCALAR
    DAY_OF_WEEK      |SCALAR
    DAY_OF_YEAR      |SCALAR
    DOM              |SCALAR
    DOW              |SCALAR
    DOY              |SCALAR
    FORMAT           |SCALAR
    HOUR             |SCALAR
    HOUR_OF_DAY      |SCALAR
    IDOW             |SCALAR
    ISODAYOFWEEK     |SCALAR
    ISODOW           |SCALAR
    ISOWEEK          |SCALAR
    ISOWEEKOFYEAR    |SCALAR
    ISO_DAY_OF_WEEK  |SCALAR
    ISO_WEEK_OF_YEAR |SCALAR
    IW               |SCALAR
    IWOY             |SCALAR
    MINUTE           |SCALAR
    MINUTE_OF_DAY    |SCALAR
    MINUTE_OF_HOUR   |SCALAR
    MONTH            |SCALAR
    MONTHNAME        |SCALAR
    MONTH_NAME       |SCALAR
    MONTH_OF_YEAR    |SCALAR
    NOW              |SCALAR
    QUARTER          |SCALAR
    SECOND           |SCALAR
    SECOND_OF_MINUTE |SCALAR
    TIMESTAMPADD     |SCALAR
    TIMESTAMPDIFF    |SCALAR
    TIMESTAMP_ADD    |SCALAR
    TIMESTAMP_DIFF   |SCALAR
    TIME_PARSE       |SCALAR
    TODAY            |SCALAR
    TO_CHAR          |SCALAR
    WEEK             |SCALAR
    WEEK_OF_YEAR     |SCALAR
    YEAR             |SCALAR
    ABS              |SCALAR
    ACOS             |SCALAR
    ASIN             |SCALAR
    ATAN             |SCALAR
    ATAN2            |SCALAR
    CBRT             |SCALAR
    CEIL             |SCALAR
    CEILING          |SCALAR
    COS              |SCALAR
    COSH             |SCALAR
    COT              |SCALAR
    DEGREES          |SCALAR
    E                |SCALAR
    EXP              |SCALAR
    EXPM1            |SCALAR
    FLOOR            |SCALAR
    LOG              |SCALAR
    LOG10            |SCALAR
    MOD              |SCALAR
    PI               |SCALAR
    POWER            |SCALAR
    RADIANS          |SCALAR
    RAND             |SCALAR
    RANDOM           |SCALAR
    ROUND            |SCALAR
    SIGN             |SCALAR
    SIGNUM           |SCALAR
    SIN              |SCALAR
    SINH             |SCALAR
    SQRT             |SCALAR
    TAN              |SCALAR
    TRUNC            |SCALAR
    TRUNCATE         |SCALAR
    ASCII            |SCALAR
    BIT_LENGTH       |SCALAR
    CHAR             |SCALAR
    CHARACTER_LENGTH |SCALAR
    CHAR_LENGTH      |SCALAR
    CONCAT           |SCALAR
    INSERT           |SCALAR
    LCASE            |SCALAR
    LEFT             |SCALAR
    LENGTH           |SCALAR
    LOCATE           |SCALAR
    LTRIM            |SCALAR
    OCTET_LENGTH     |SCALAR
    POSITION         |SCALAR
    REPEAT           |SCALAR
    REPLACE          |SCALAR
    RIGHT            |SCALAR
    RTRIM            |SCALAR
    SPACE            |SCALAR
    STARTS_WITH      |SCALAR
    SUBSTRING        |SCALAR
    TRIM             |SCALAR
    UCASE            |SCALAR
    CAST             |SCALAR
    CONVERT          |SCALAR
    DATABASE         |SCALAR
    USER             |SCALAR
    ST_ASTEXT        |SCALAR
    ST_ASWKT         |SCALAR
    ST_DISTANCE      |SCALAR
    ST_GEOMETRYTYPE  |SCALAR
    ST_GEOMFROMTEXT  |SCALAR
    ST_WKTTOSQL      |SCALAR
    ST_X             |SCALAR
    ST_Y             |SCALAR
    ST_Z             |SCALAR
    SCORE            |SCORE

可以根据模式自定义返回的函数列表。

它可以是完全匹配的：

    
    
    SHOW FUNCTIONS LIKE 'ABS';
    
         name      |     type
    ---------------+---------------
    ABS            |SCALAR

一个字符的通配符：

    
    
    SHOW FUNCTIONS LIKE 'A__';
    
         name      |     type
    ---------------+---------------
    AVG            |AGGREGATE
    ABS            |SCALAR

匹配零个或多个字符的通配符：

    
    
    SHOW FUNCTIONS LIKE 'A%';
    
         name      |     type
    ---------------+---------------
    AVG            |AGGREGATE
    ABS            |SCALAR
    ACOS           |SCALAR
    ASIN           |SCALAR
    ATAN           |SCALAR
    ATAN2          |SCALAR
    ASCII          |SCALAR

或者当然，上述内容的变体：

    
    
    SHOW FUNCTIONS LIKE '%DAY%';
    
         name      |     type
    ---------------+---------------
    DAY            |SCALAR
    DAYNAME        |SCALAR
    DAYOFMONTH     |SCALAR
    DAYOFWEEK      |SCALAR
    DAYOFYEAR      |SCALAR
    DAY_NAME       |SCALAR
    DAY_OF_MONTH   |SCALAR
    DAY_OF_WEEK    |SCALAR
    DAY_OF_YEAR    |SCALAR
    HOUR_OF_DAY    |SCALAR
    ISODAYOFWEEK   |SCALAR
    ISO_DAY_OF_WEEK|SCALAR
    MINUTE_OF_DAY  |SCALAR
    TODAY          |SCALAR

[« SHOW COLUMNS](sql-syntax-show-columns.md) [SHOW TABLES »](sql-syntax-
show-tables.md)
