

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« Frozen Indices](sql-index-frozen.md) [Comparison Operators »](sql-
operators.md)

## 函数和运算符

Elasticsearch SQL 提供了一套全面的内置运算符和函数：

*运营商

    * [`Equality (=)`](sql-operators.html#sql-operators-equality "Equality \(=\)")
    * [`Null safe Equality (<=>)`](sql-operators.html#sql-operators-null-safe-equality "Null safe Equality \(<=>\)")
    * [`Inequality (<> or !=)`](sql-operators.html#sql-operators-inequality "Inequality \(<> or !=\)")
    * [`Comparison (<, <=, >, >=)`](sql-operators.html#sql-operators-comparison "Comparison \(<, <=, >, >=\)")
    * [`BETWEEN`](sql-operators.html#sql-operators-between "BETWEEN")
    * [`IS NULL/IS NOT NULL`](sql-operators.html#sql-operators-is-null "IS NULL/IS NOT NULL")
    * [`IN (<value1>, <value2>, ...)`](sql-operators.html#sql-operators-in "IN \(<value1>, <value2>, ...\)")
    * [`AND`](sql-operators-logical.html#sql-operators-and "AND")
    * [`OR`](sql-operators-logical.html#sql-operators-or "OR")
    * [`NOT`](sql-operators-logical.html#sql-operators-not "NOT")
    * [`Add (+)`](sql-operators-math.html#sql-operators-plus "Add \(+\)")
    * [`Subtract (infix -)`](sql-operators-math.html#sql-operators-subtract "Subtract \(infix -\)")
    * [`Negate (unary -)`](sql-operators-math.html#sql-operators-negate "Negate \(unary -\)")
    * [`Multiply (*)`](sql-operators-math.html#sql-operators-multiply "Multiply \(*\)")
    * [`Divide (/)`](sql-operators-math.html#sql-operators-divide "Divide \(/\)")
    * [`Modulo or Remainder(%)`](sql-operators-math.html#sql-operators-remainder "Modulo or Remainder\(%\)")
    * [`Cast (::)`](sql-operators-cast.html#sql-operators-cast-cast "Cast \(::\)")

* 喜欢和喜欢运算符

    * [`LIKE`](sql-like-rlike-operators.html#sql-like-operator "LIKE")
    * [`RLIKE`](sql-like-rlike-operators.html#sql-rlike-operator "RLIKE")

* 聚合函数

    * [`AVG`](sql-functions-aggs.html#sql-functions-aggs-avg "AVG")
    * [`COUNT`](sql-functions-aggs.html#sql-functions-aggs-count "COUNT")
    * [`COUNT(ALL)`](sql-functions-aggs.html#sql-functions-aggs-count-all "COUNT\(ALL\)")
    * [`COUNT(DISTINCT)`](sql-functions-aggs.html#sql-functions-aggs-count-distinct "COUNT\(DISTINCT\)")
    * [`FIRST/FIRST_VALUE`](sql-functions-aggs.html#sql-functions-aggs-first "FIRST/FIRST_VALUE")
    * [`LAST/LAST_VALUE`](sql-functions-aggs.html#sql-functions-aggs-last "LAST/LAST_VALUE")
    * [`MAX`](sql-functions-aggs.html#sql-functions-aggs-max "MAX")
    * [`MIN`](sql-functions-aggs.html#sql-functions-aggs-min "MIN")
    * [`SUM`](sql-functions-aggs.html#sql-functions-aggs-sum "SUM")
    * [`KURTOSIS`](sql-functions-aggs.html#sql-functions-aggs-kurtosis "KURTOSIS")
    * [`MAD`](sql-functions-aggs.html#sql-functions-aggs-mad "MAD")
    * [`PERCENTILE`](sql-functions-aggs.html#sql-functions-aggs-percentile "PERCENTILE")
    * [`PERCENTILE_RANK`](sql-functions-aggs.html#sql-functions-aggs-percentile-rank "PERCENTILE_RANK")
    * [`SKEWNESS`](sql-functions-aggs.html#sql-functions-aggs-skewness "SKEWNESS")
    * [`STDDEV_POP`](sql-functions-aggs.html#sql-functions-aggs-stddev-pop "STDDEV_POP")
    * [`STDDEV_SAMP`](sql-functions-aggs.html#sql-functions-aggs-stddev-samp "STDDEV_SAMP")
    * [`SUM_OF_SQUARES`](sql-functions-aggs.html#sql-functions-aggs-sum-squares "SUM_OF_SQUARES")
    * [`VAR_POP`](sql-functions-aggs.html#sql-functions-aggs-var-pop "VAR_POP")
    * [`VAR_SAMP`](sql-functions-aggs.html#sql-functions-aggs-var-samp "VAR_SAMP")

* 分组函数

    * [`HISTOGRAM`](sql-functions-grouping.html#sql-functions-grouping-histogram "HISTOGRAM")

* 日期时间运算符 * 日期时间函数

    * [`CURRENT_DATE/CURDATE`](sql-functions-datetime.html#sql-functions-current-date "CURRENT_DATE/CURDATE")
    * [`CURRENT_TIME/CURTIME`](sql-functions-datetime.html#sql-functions-current-time "CURRENT_TIME/CURTIME")
    * [`CURRENT_TIMESTAMP`](sql-functions-datetime.html#sql-functions-current-timestamp "CURRENT_TIMESTAMP")
    * [`DATE_ADD/DATEADD/TIMESTAMP_ADD/TIMESTAMPADD`](sql-functions-datetime.html#sql-functions-datetime-add "DATE_ADD/DATEADD/TIMESTAMP_ADD/TIMESTAMPADD")
    * [`DATE_DIFF/DATEDIFF/TIMESTAMP_DIFF/TIMESTAMPDIFF`](sql-functions-datetime.html#sql-functions-datetime-diff "DATE_DIFF/DATEDIFF/TIMESTAMP_DIFF/TIMESTAMPDIFF")
    * [`DATE_FORMAT`](sql-functions-datetime.html#sql-functions-datetime-dateformat "DATE_FORMAT")
    * [`DATE_PARSE`](sql-functions-datetime.html#sql-functions-datetime-dateparse "DATE_PARSE")
    * [`DATETIME_FORMAT`](sql-functions-datetime.html#sql-functions-datetime-datetimeformat "DATETIME_FORMAT")
    * [`DATETIME_PARSE`](sql-functions-datetime.html#sql-functions-datetime-datetimeparse "DATETIME_PARSE")
    * [`FORMAT`](sql-functions-datetime.html#sql-functions-datetime-format "FORMAT")
    * [`DATE_PART/DATEPART`](sql-functions-datetime.html#sql-functions-datetime-part "DATE_PART/DATEPART")
    * [`DATE_TRUNC/DATETRUNC`](sql-functions-datetime.html#sql-functions-datetime-trunc "DATE_TRUNC/DATETRUNC")
    * [`DAY_OF_MONTH/DOM/DAY`](sql-functions-datetime.html#sql-functions-datetime-day "DAY_OF_MONTH/DOM/DAY")
    * [`DAY_OF_WEEK/DAYOFWEEK/DOW`](sql-functions-datetime.html#sql-functions-datetime-dow "DAY_OF_WEEK/DAYOFWEEK/DOW")
    * [`DAY_OF_YEAR/DOY`](sql-functions-datetime.html#sql-functions-datetime-doy "DAY_OF_YEAR/DOY")
    * [`DAY_NAME/DAYNAME`](sql-functions-datetime.html#sql-functions-datetime-dayname "DAY_NAME/DAYNAME")
    * [`EXTRACT`](sql-functions-datetime.html#sql-functions-datetime-extract "EXTRACT")
    * [`HOUR_OF_DAY/HOUR`](sql-functions-datetime.html#sql-functions-datetime-hour "HOUR_OF_DAY/HOUR")
    * [`ISO_DAY_OF_WEEK/ISODAYOFWEEK/ISODOW/IDOW`](sql-functions-datetime.html#sql-functions-datetime-isodow "ISO_DAY_OF_WEEK/ISODAYOFWEEK/ISODOW/IDOW")
    * [`ISO_WEEK_OF_YEAR/ISOWEEKOFYEAR/ISOWEEK/IWOY/IW`](sql-functions-datetime.html#sql-functions-datetime-isoweek "ISO_WEEK_OF_YEAR/ISOWEEKOFYEAR/ISOWEEK/IWOY/IW")
    * [`MINUTE_OF_DAY`](sql-functions-datetime.html#sql-functions-datetime-minuteofday "MINUTE_OF_DAY")
    * [`MINUTE_OF_HOUR/MINUTE`](sql-functions-datetime.html#sql-functions-datetime-minute "MINUTE_OF_HOUR/MINUTE")
    * [`MONTH_OF_YEAR/MONTH`](sql-functions-datetime.html#sql-functions-datetime-month "MONTH_OF_YEAR/MONTH")
    * [`MONTH_NAME/MONTHNAME`](sql-functions-datetime.html#sql-functions-datetime-monthname "MONTH_NAME/MONTHNAME")
    * [`NOW`](sql-functions-datetime.html#sql-functions-now "NOW")
    * [`SECOND_OF_MINUTE/SECOND`](sql-functions-datetime.html#sql-functions-datetime-second "SECOND_OF_MINUTE/SECOND")
    * [`QUARTER`](sql-functions-datetime.html#sql-functions-datetime-quarter "QUARTER")
    * [`TIME_PARSE`](sql-functions-datetime.html#sql-functions-datetime-timeparse "TIME_PARSE")
    * [`TO_CHAR`](sql-functions-datetime.html#sql-functions-datetime-to_char "TO_CHAR")
    * [`TODAY`](sql-functions-datetime.html#sql-functions-today "TODAY")
    * [`WEEK_OF_YEAR/WEEK`](sql-functions-datetime.html#sql-functions-datetime-week "WEEK_OF_YEAR/WEEK")
    * [`YEAR`](sql-functions-datetime.html#sql-functions-datetime-year "YEAR")

* 全文搜索功能

    * [`MATCH`](sql-functions-search.html#sql-functions-search-match "MATCH")
    * [`QUERY`](sql-functions-search.html#sql-functions-search-query "QUERY")
    * [`SCORE`](sql-functions-search.html#sql-functions-search-score "SCORE")

* 数学函数

    * [`ABS`](sql-functions-math.html#sql-functions-math-abs "ABS")
    * [`CBRT`](sql-functions-math.html#sql-functions-math-cbrt "CBRT")
    * [`CEIL/CEILING`](sql-functions-math.html#sql-functions-math-ceil "CEIL/CEILING")
    * [`E`](sql-functions-math.html#sql-functions-math-e "E")
    * [`EXP`](sql-functions-math.html#sql-functions-math-exp "EXP")
    * [`EXPM1`](sql-functions-math.html#sql-functions-math-expm1 "EXPM1")
    * [`FLOOR`](sql-functions-math.html#sql-functions-math-floor "FLOOR")
    * [`LOG`](sql-functions-math.html#sql-functions-math-log "LOG")
    * [`LOG10`](sql-functions-math.html#sql-functions-math-log10 "LOG10")
    * [`PI`](sql-functions-math.html#sql-functions-math-pi "PI")
    * [`POWER`](sql-functions-math.html#sql-functions-math-power "POWER")
    * [`RANDOM/RAND`](sql-functions-math.html#sql-functions-math-random "RANDOM/RAND")
    * [`ROUND`](sql-functions-math.html#sql-functions-math-round "ROUND")
    * [`SIGN/SIGNUM`](sql-functions-math.html#sql-functions-math-sign "SIGN/SIGNUM")
    * [`SQRT`](sql-functions-math.html#sql-functions-math-sqrt "SQRT")
    * [`TRUNCATE/TRUNC`](sql-functions-math.html#sql-functions-math-truncate "TRUNCATE/TRUNC")
    * [`ACOS`](sql-functions-math.html#sql-functions-math-acos "ACOS")
    * [`ASIN`](sql-functions-math.html#sql-functions-math-asin "ASIN")
    * [`ATAN`](sql-functions-math.html#sql-functions-math-atan "ATAN")
    * [`ATAN2`](sql-functions-math.html#sql-functions-math-atan2 "ATAN2")
    * [`COS`](sql-functions-math.html#sql-functions-math-cos "COS")
    * [`COSH`](sql-functions-math.html#sql-functions-math-cosh "COSH")
    * [`COT`](sql-functions-math.html#sql-functions-math-cot "COT")
    * [`DEGREES`](sql-functions-math.html#sql-functions-math-degrees "DEGREES")
    * [`RADIANS`](sql-functions-math.html#sql-functions-math-radians "RADIANS")
    * [`SIN`](sql-functions-math.html#sql-functions-math-sin "SIN")
    * [`SINH`](sql-functions-math.html#sql-functions-math-sinh "SINH")
    * [`TAN`](sql-functions-math.html#sql-functions-math-tan "TAN")

* 字符串函数

    * [`ASCII`](sql-functions-string.html#sql-functions-string-ascii "ASCII")
    * [`BIT_LENGTH`](sql-functions-string.html#sql-functions-string-bit-length "BIT_LENGTH")
    * [`CHAR`](sql-functions-string.html#sql-functions-string-char "CHAR")
    * [`CHAR_LENGTH`](sql-functions-string.html#sql-functions-string-char-length "CHAR_LENGTH")
    * [`CONCAT`](sql-functions-string.html#sql-functions-string-concat "CONCAT")
    * [`INSERT`](sql-functions-string.html#sql-functions-string-insert "INSERT")
    * [`LCASE`](sql-functions-string.html#sql-functions-string-lcase "LCASE")
    * [`LEFT`](sql-functions-string.html#sql-functions-string-left "LEFT")
    * [`LENGTH`](sql-functions-string.html#sql-functions-string-length "LENGTH")
    * [`LOCATE`](sql-functions-string.html#sql-functions-string-locate "LOCATE")
    * [`LTRIM`](sql-functions-string.html#sql-functions-string-ltrim "LTRIM")
    * [`OCTET_LENGTH`](sql-functions-string.html#sql-functions-string-octet-length "OCTET_LENGTH")
    * [`POSITION`](sql-functions-string.html#sql-functions-string-position "POSITION")
    * [`REPEAT`](sql-functions-string.html#sql-functions-string-repeat "REPEAT")
    * [`REPLACE`](sql-functions-string.html#sql-functions-string-replace "REPLACE")
    * [`RIGHT`](sql-functions-string.html#sql-functions-string-right "RIGHT")
    * [`RTRIM`](sql-functions-string.html#sql-functions-string-rtrim "RTRIM")
    * [`SPACE`](sql-functions-string.html#sql-functions-string-space "SPACE")
    * [`SUBSTRING`](sql-functions-string.html#sql-functions-string-substring "SUBSTRING")
    * [`TRIM`](sql-functions-string.html#sql-functions-string-trim "TRIM")
    * [`UCASE`](sql-functions-string.html#sql-functions-string-ucase "UCASE")

* 类型转换函数

    * [`CAST`](sql-functions-type-conversion.html#sql-functions-type-conversion-cast "CAST")
    * [`CONVERT`](sql-functions-type-conversion.html#sql-functions-type-conversion-convert "CONVERT")

* 条件函数和表达式

    * [`CASE`](sql-functions-conditional.html#sql-functions-conditional-case "CASE")
    * [`COALESCE`](sql-functions-conditional.html#sql-functions-conditional-coalesce "COALESCE")
    * [`GREATEST`](sql-functions-conditional.html#sql-functions-conditional-greatest "GREATEST")
    * [`IFNULL`](sql-functions-conditional.html#sql-functions-conditional-ifnull "IFNULL")
    * [`IIF`](sql-functions-conditional.html#sql-functions-conditional-iif "IIF")
    * [`ISNULL`](sql-functions-conditional.html#sql-functions-conditional-isnull "ISNULL")
    * [`LEAST`](sql-functions-conditional.html#sql-functions-conditional-least "LEAST")
    * [`NULLIF`](sql-functions-conditional.html#sql-functions-conditional-nullif "NULLIF")
    * [`NVL`](sql-functions-conditional.html#sql-functions-conditional-nvl "NVL")

* 地理功能

    * [`ST_AsWKT`](sql-functions-geo.html#sql-functions-geo-st-as-wkt "ST_AsWKT")
    * [`ST_Distance`](sql-functions-geo.html#sql-functions-geo-st-distance "ST_Distance")
    * [`ST_GeometryType`](sql-functions-geo.html#sql-functions-geo-st-geometrytype "ST_GeometryType")
    * [`ST_WKTToSQL`](sql-functions-geo.html#sql-functions-geo-st-wkt-to-sql "ST_WKTToSQL")
    * [`ST_X`](sql-functions-geo.html#sql-functions-geo-st-x "ST_X")
    * [`ST_Y`](sql-functions-geo.html#sql-functions-geo-st-y "ST_Y")
    * [`ST_Z`](sql-functions-geo.html#sql-functions-geo-st-z "ST_Z")

* 系统功能

    * [`DATABASE`](sql-functions-system.html#sql-functions-system-database "DATABASE")
    * [`USER`](sql-functions-system.html#sql-functions-system-user "USER")

[« Frozen Indices](sql-index-frozen.md) [Comparison Operators »](sql-
operators.md)
