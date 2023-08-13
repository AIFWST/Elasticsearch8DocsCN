

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Functions and Operators](sql-functions.md) [Logical Operators »](sql-
operators-logical.md)

## 比较运算符

用于与一个或多个表达式进行比较的布尔运算符。

### '平等(=)'

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no = 10000 LIMIT 5;

### '空安全相等(<=>)'

    
    
    SELECT 'elastic' <=> null AS "equals";
    
        equals
    ---------------
    false
    
    
    SELECT null <=> null AS "equals";
    
        equals
    ---------------
    true

### '不平等 (<> 或！=)'

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no <> 10000 ORDER BY emp_no LIMIT 5;

### '比较 (<， <=， >，>=)'

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no < 10003 ORDER BY emp_no LIMIT 5;

###'之间'

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no BETWEEN 9990 AND 10003 ORDER BY emp_no;

### 'IS NULL/IS NOTNULL'

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no IS NOT NULL AND gender IS NULL;

### 'IN (<value1><value2>， ,...)`

    
    
    SELECT last_name l FROM "test_emp" WHERE emp_no IN (10000, 10001, 10002, 999) ORDER BY emp_no LIMIT 5;

[« Functions and Operators](sql-functions.md) [Logical Operators »](sql-
operators-logical.md)
