

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Comparison Operators](sql-operators.md) [Math Operators »](sql-operators-
math.md)

## 逻辑运算符

用于计算一个或两个表达式的布尔运算符。

###'和'

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no > 10000 AND emp_no < 10005 ORDER BY emp_no LIMIT 5;

###'或'

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no < 10003 OR emp_no = 10005 ORDER BY emp_no LIMIT 5;

###'不'

    
    
    SELECT last_name l FROM "test_emp" WHERE NOT emp_no = 10000 LIMIT 5;

[« Comparison Operators](sql-operators.md) [Math Operators »](sql-operators-
math.md)
