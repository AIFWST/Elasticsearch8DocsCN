

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Definitions](api-definitions.md)

[« Definitions](api-definitions.md) [Migration guide »](breaking-
changes.md)

## 角色映射资源

角色映射资源具有以下属性：

`enabled`

     (Boolean) Mappings that have `enabled` set to `false` are ignored when role mapping is performed. 
`metadata`

     (object) Additional metadata that helps define which roles are assigned to each user. Within the `metadata` object, keys beginning with `_` are reserved for system usage. 
`roles`

     (list) A list of roles that are granted to the users that match the role mapping rules. 
`rules`

    

(对象)确定映射应匹配哪些用户的规则。规则是使用 JSON DSL 表示的逻辑条件。DSL 支持以下规则类型：

`any`

     (array of rules) If **any** of its children are true, it evaluates to `true`. 
`all`

     (array of rules) If **all** of its children are true, it evaluates to `true`. 
`field`

     (object) See [Field rules](role-mapping-resources.html#mapping-roles-rule-field "Field rules"). 
`except`

     (object) A single rule as an object. Only valid as a child of an `all` rule. If its child is `false`, the `except` is `true`. 

#### 字段规则

"字段"规则是角色映射表达式的主要构建基块。它采用单个对象作为其值，并且该对象必须包含键为 _F_ 和值 _V_ 的单个成员。字段规则查找 _F_within 用户对象的值，然后测试用户值 _是否与提供的值 _V_ 匹配。

字段规则中指定的值可以是以下类型之一：

类型 |描述 |示例 ---|---|--- 简单字符串

|

与提供的值完全匹配。

|

"esadmin""通配符字符串

|

使用通配符匹配提供的值。

|

'"*，dc=example，dc=com"' 正则表达式

|

使用 Lucene 正则表达式匹配提供的值。

|

'"/.*-admin[0-9]*/"' 编号

|

匹配等效的数值。

|

"7"空

|

匹配空值或缺失值。

|

"空"数组

|

根据上述定义测试数组中的每个元素。元素匹配If_any_，则匹配成功。

|

'"admin"， "operator"]' ##### 用户字段[编辑

评估规则所依据的_user object_具有以下字段：

`username`

     (string) The username by which the Elasticsearch security features knows this user. For example, `"username": "jsmith"`. 
`dn`

     (string) The _Distinguished Name_ of the user. For example, `"dn": "cn=jsmith,ou=users,dc=example,dc=com",`. 
`groups`

     (array of strings) The groups to which the user belongs. For example, `"groups" : [ "cn=admin,ou=groups,dc=example,dc=com","cn=esusers,ou=groups,dc=example,dc=com ]`. 
`metadata`

     (object) Additional metadata for the user. For example, `"metadata": { "cn": "John Smith" }`. 
`realm`

     (object) The realm that authenticated the user. The only field in this object is the realm name. For example, `"realm": { "name": "ldap1" }`. 

"组"字段是多值的;一个用户可以属于多个组。当对多值字段应用"字段"规则时，如果至少_at one_ 个成员值匹配，则认为该规则匹配。例如，以下规则匹配属于"admin"组成员的任何用户，无论他们属于任何其他组：

    
    
    { "field" : { "groups" : "admin" } }

有关特定于领域的其他详细信息，请参阅 Active Directory 和 LDAPrealms。

[« Definitions](api-definitions.md) [Migration guide »](breaking-
changes.md)
