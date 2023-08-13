

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Full-Text Search Functions](sql-functions-search.md) [String Functions
»](sql-functions-string.md)

## 数学函数

所有数学和三角函数都要求其输入(如果适用)为数字。

###Generic

###'ABS'

**Synopsis:**

    
    
    ABS(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：数字

**说明**：返回"numeric_exp"的绝对值。转弯类型与输入类型相同。

    
    
    SELECT ABS(-123.5), ABS(55);
    
      ABS(-123.5)  |    ABS(55)
    ---------------+---------------
    123.5          |55

###'CBRT'

**Synopsis:**

    
    
    CBRT(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的立方根。

    
    
    SELECT CBRT(-125.5);
    
       CBRT(-125.5)
    -------------------
    -5.0066577974783435

###'天花板/天花板'

**Synopsis:**

    
    
    CEIL(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数或长数值

**说明**：返回大于或等于'numeric_exp'的最小整数。

    
    
    SELECT CEIL(125.01), CEILING(-125.99);
    
     CEIL(125.01)  |CEILING(-125.99)
    ---------------+----------------
    126            |-125

###'E'

**Synopsis:**

    
    
    E()

**输入** ： _无_

**输出** ： '2.718281828459045'

**描述**：返回欧拉数。

    
    
    SELECT E(), CEIL(E());
    
           E()       |   CEIL(E())
    -----------------+---------------
    2.718281828459045|3

###'经验"

**Synopsis:**

    
    
    EXP(numeric_exp) __

**输入**：

__

|

浮点数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**描述**：返回numeric_exp enumeric_exp幂的欧拉数。

    
    
    SELECT EXP(1), E(), EXP(2), E() * E();
    
         EXP(1)      |       E()       |     EXP(2)     |     E() * E()
    -----------------+-----------------+----------------+------------------
    2.718281828459045|2.718281828459045|7.38905609893065|7.3890560989306495

###'EXPM1'

**Synopsis:**

    
    
    EXPM1(numeric_exp) __

**输入**：

__

|

浮点数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**描述**：返回欧拉数的幂numeric_exp减去 1 (enumeric_exp \- 1)。

    
    
    SELECT E(), EXP(2), EXPM1(2);
    
           E()       |     EXP(2)     |    EXPM1(2)
    -----------------+----------------+----------------
    2.718281828459045|7.38905609893065|6.38905609893065

###'地板'

**Synopsis:**

    
    
    FLOOR(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：整数或长数值

**说明**：返回小于或等于'numeric_exp'的最大整数。

    
    
    SELECT FLOOR(125.01), FLOOR(-125.99);
    
     FLOOR(125.01) |FLOOR(-125.99)
    ---------------+---------------
    125            |-126

###'日志'

**Synopsis:**

    
    
    LOG(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的自然对数。

    
    
    SELECT EXP(3), LOG(20.085536923187668);
    
          EXP(3)      |LOG(20.085536923187668)
    ------------------+-----------------------
    20.085536923187668|3.0

###'LOG10'

**Synopsis:**

    
    
    LOG10(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回 'numeric_exp' 的底数 10 对数。

    
    
    SELECT LOG10(5), LOG(5)/LOG(10);
    
         LOG10(5)     |    LOG(5)/LOG(10)
    ------------------+-----------------------
    0.6989700043360189|0.6989700043360187

###'PI'

**Synopsis:**

    
    
    PI()

**输入** ： _无_

**输出** ： '3.141592653589793'

**说明**：返回 PI 编号。

    
    
    SELECT PI();
    
          PI()
    -----------------
    3.141592653589793

###'电源'

**Synopsis:**

    
    
    POWER(
        numeric_exp, __integer_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式。如果为"null"，则函数返回"null"。   **输出**：双精度数值

**说明**：返回"numeric_exp"的值，以"integer_exp"的幂。

    
    
    SELECT POWER(3, 2), POWER(3, 3);
    
      POWER(3, 2)  |  POWER(3, 3)
    ---------------+---------------
    9.0            |27.0
    
    
    SELECT POWER(5, -1), POWER(5, -2);
    
      POWER(5, -1) |  POWER(5, -2)
    ---------------+---------------
    0.2            |0.04

###'随机/兰特'

**Synopsis:**

    
    
    RANDOM(seed) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**描述**：使用给定种子返回随机双精度值。

    
    
    SELECT RANDOM(123);
    
       RANDOM(123)
    ------------------
    0.7231742029971469

###'圆形'

**Synopsis:**

    
    
    ROUND(
        numeric_exp      __[, integer_exp]) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式;自选。如果为"null"，则函数返回"null"。   **输出**：数字

**说明**：返回四舍五入到小数点右侧的"integer_exp"位的"numeric_exp"。如果"integer_exp"为负数，则"numeric_exp"四舍五入为 |"integer_exp"|位置位于小数点左侧。如果省略"integer_exp"，则该函数将执行，就好像"integer_exp"将为 0 一样。因此，数字数据类型与"numeric_exp"的数据类型相同。

    
    
    SELECT ROUND(-345.153, 1) AS rounded;
    
        rounded
    ---------------
    -345.2
    
    
    SELECT ROUND(-345.153, -1) AS rounded;
    
        rounded
    ---------------
    -350.0

###'签名/签名'

**Synopsis:**

    
    
    SIGN(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出** ： [-1， 0， 1]

**说明**：返回"numeric_exp"符号的指示符。如果"numeric_exp"小于零，则返回 –1。如果"numeric_exp"等于零，则返回 0。如果"numeric_exp"大于零，则返回 1。

    
    
    SELECT SIGN(-123), SIGN(0), SIGN(415);
    
      SIGN(-123)   |    SIGN(0)    |   SIGN(415)
    ---------------+---------------+---------------
    -1             |0              |1

###'SQRT'

**Synopsis:**

    
    
    SQRT(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的平方根。

    
    
    SELECT SQRT(EXP(2)), E(), SQRT(25);
    
      SQRT(EXP(2))   |       E()       |   SQRT(25)
    -----------------+-----------------+---------------
    2.718281828459045|2.718281828459045|5.0

###'TRUNCATE/TRUNC'

**Synopsis:**

    
    
    TRUNCATE(
        numeric_exp      __[, integer_exp]) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

整数表达式;自选。如果为"null"，则函数返回"null"。   **输出**：数字

**说明**：返回截断为"integer_exp"位的小数点右侧的"numeric_exp"。如果"integer_exp"为负数，则"numeric_exp"改为|"integer_exp"|位置位于小数点左侧。如果省略"integer_exp"，则该函数将执行，就好像"integer_exp"将为 0 一样。返回的数值数据类型与 'numeric_exp' 的数据类型相同。

    
    
    SELECT TRUNC(-345.153, 1) AS trimmed;
    
        trimmed
    ---------------
    -345.1
    
    
    SELECT TRUNCATE(-345.153, -1) AS trimmed;
    
        trimmed
    ---------------
    -340.0

###Trigonometric

###'ACOS'

**Synopsis:**

    
    
    ACOS(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的反角余弦作为角度，以弧度表示。

    
    
    SELECT ACOS(COS(PI())), PI();
    
     ACOS(COS(PI())) |      PI()
    -----------------+-----------------
    3.141592653589793|3.141592653589793

###'ASIN'

**Synopsis:**

    
    
    ASIN(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的反弧正弦作为角度，以弧度表示。

    
    
    SELECT ROUND(DEGREES(ASIN(0.7071067811865475))) AS "ASIN(0.707)", ROUND(SIN(RADIANS(45)), 3) AS "SIN(45)";
    
      ASIN(0.707)  |    SIN(45)
    ---------------+---------------
    45.0           |0.707

###'阿坦'

**Synopsis:**

    
    
    ATAN(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的反正切值作为角度，以弧度表示。

    
    
    SELECT DEGREES(ATAN(TAN(RADIANS(90))));
    
    DEGREES(ATAN(TAN(RADIANS(90))))
    -------------------------------
    90.0

###'阿坦2'

**Synopsis:**

    
    
    ATAN2(
        ordinate, __abscisa) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|---    __

|

数值表达式。如果为"null"，则函数返回"null"。   **输出**：双精度数值

**说明**：返回指定为角度的"纵坐标"和"横坐标"的反正切值，以弧度表示。

    
    
    SELECT ATAN2(5 * SIN(RADIANS(45)), 5 * COS(RADIANS(45))) AS "ATAN2(5*SIN(45), 5*COS(45))", RADIANS(45);
    
    ATAN2(5*SIN(45), 5*COS(45))|   RADIANS(45)
    ---------------------------+------------------
    0.7853981633974483         |0.7853981633974483

###'COS'

**Synopsis:**

    
    
    COS(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的余弦值，其中"numeric_exp"是以弧度表示的角度。

    
    
    SELECT COS(RADIANS(180)), POWER(SIN(RADIANS(54)), 2) + POWER(COS(RADIANS(54)), 2) AS pythagorean_identity;
    
    COS(RADIANS(180))|pythagorean_identity
    -----------------+--------------------
    -1.0             |1.0

###'COSH'

**Synopsis:**

    
    
    COSH(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的双曲余弦。

    
    
    SELECT COSH(5), (POWER(E(), 5) + POWER(E(), -5)) / 2 AS "(e^5 + e^-5)/2";
    
         COSH(5)     | (e^5 + e^-5)/2
    -----------------+-----------------
    74.20994852478785|74.20994852478783

###'婴儿床'

**Synopsis:**

    
    
    COT(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的余切线，其中"numeric_exp"是以弧度表示的角度。

    
    
    SELECT COT(RADIANS(30)) AS "COT(30)", COS(RADIANS(30)) / SIN(RADIANS(30)) AS "COS(30)/SIN(30)";
    
         COT(30)      | COS(30)/SIN(30)
    ------------------+------------------
    1.7320508075688774|1.7320508075688776

###"度"

**Synopsis:**

    
    
    DEGREES(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**描述**：从弧度转换为度)。

    
    
    SELECT DEGREES(PI() * 2), DEGREES(PI());
    
    DEGREES(PI() * 2)| DEGREES(PI())
    -----------------+---------------
    360.0            |180.0

###'弧度'

**Synopsis:**

    
    
    RADIANS(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**描述**：从度转换)托拉度。

    
    
    SELECT RADIANS(90), PI()/2;
    
       RADIANS(90)    |      PI()/2
    ------------------+------------------
    1.5707963267948966|1.5707963267948966

###"罪恶"

**Synopsis:**

    
    
    SIN(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的正弦值，其中"numeric_exp"是以弧度表示的角度。

    
    
    SELECT SIN(RADIANS(90)), POWER(SIN(RADIANS(67)), 2) + POWER(COS(RADIANS(67)), 2) AS pythagorean_identity;
    
    SIN(RADIANS(90))|pythagorean_identity
    ----------------+--------------------
    1.0             |1.0

###'新"

**Synopsis:**

    
    
    SINH(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的双曲正弦。

    
    
    SELECT SINH(5), (POWER(E(), 5) - POWER(E(), -5)) / 2 AS "(e^5 - e^-5)/2";
    
         SINH(5)     | (e^5 - e^-5)/2
    -----------------+-----------------
    74.20321057778875|74.20321057778874

###'谭'

**Synopsis:**

    
    
    TAN(numeric_exp) __

**输入**：

__

|

数值表达式。如果为"null"，则函数返回"null"。   ---|--- **输出**：双精度数值

**说明**：返回"numeric_exp"的切线，其中"numeric_exp"是以弧度表示的角度。

    
    
    SELECT TAN(RADIANS(66)) AS "TAN(66)", SIN(RADIANS(66))/COS(RADIANS(66)) AS "SIN(66)/COS(66)=TAN(66)";
    
         TAN(66)      |SIN(66)/COS(66)=TAN(66)
    ------------------+-----------------------
    2.2460367739042164|2.246036773904216

[« Full-Text Search Functions](sql-functions-search.md) [String Functions
»](sql-functions-string.md)
