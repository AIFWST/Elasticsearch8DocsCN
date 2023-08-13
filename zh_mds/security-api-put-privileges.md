

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Create API key API](security-api-create-api-key.md) [Create or update
role mappings API »](security-api-put-role-mapping.md)

## 创建或更新应用程序权限API

添加或更新应用程序权限。

###Request

"发布/_security/特权"

"放置/_security/特权"

###Prerequisites

若要使用此 API，必须具有以下任一条件：

* "manage_security"群集权限(或更大的权限，如"全部");_or_ * 请求中引用的应用程序的 _"管理应用程序权限"_ 全局权限

###Description

此 API 创建或更新权限。要删除权限，请使用删除应用程序权限 API。

有关详细信息，请参阅应用程序权限。

要检查用户的应用程序权限，请使用具有权限 API。

### 请求正文

正文是一个 JSON 对象，其中字段的名称是应用程序名称，每个字段的值是一个对象。此内部对象中的字段是权限的名称，每个值都是一个 JSON 对象，其中包括以下字段：

`actions`

     (array-of-string) A list of action names that are granted by this privilege. This field must exist and cannot be an empty array. 
`metadata`

     (object) Optional meta-data. Within the `metadata` object, keys that begin with `_` are reserved for system usage. 

###Validation

应用程序名称

    

应用程序名称由 _前缀_ 组成，带有符合以下规则的可选 _后缀_：

* 前缀必须以小写 ASCII 字母开头 * 前缀必须仅包含 ASCII 字母或数字 * 前缀长度必须至少为 3 个字符 * 如果后缀存在，则必须以"-"或"_"开头 * 后缀不能包含以下任何字符："\"、"/"、"*"、"？"、"<"、">"、"|"、""、"*" * 名称的任何部分都不能包含空格。

权限名称

     Privilege names must begin with a lowercase ASCII letter and must contain only ASCII letters and digits along with the characters `_`, `-` and `.`
Action names

     Action names can contain any number of printable ASCII characters and must contain at least one of the following characters: `/` `*`, `:`

### 响应正文

成功的调用会返回一个 JSON 结构，该结构显示权限是否已创建或更新。

###Examples

要添加单个权限，请将 PUT 或 POST 请求提交到"/_security/privilege/"端点。例如：

    
    
    PUT /_security/privilege
    {
      "myapp": {
        "read": {
          "actions": [ __"data:read/*" , __"action:login" ],
            "metadata": { __"description": "Read access to myapp"
            }
          }
        }
    }

__

|

这些字符串在"myapp"应用程序中具有重要意义。Elasticsearch没有赋予它们任何意义。   ---|---    __

|

此处使用通配符 ('*') 意味着此权限授予对以"data：read/"开头的所有操作的访问权限。Elasticsearch 不会为这些操作分配任何意义。但是，如果请求包含应用程序权限，例如"data：read/users"或"data：read/settings"，则 hasprivileges API 尊重通配符的使用并返回"true"。   __

|

元数据对象是可选的。               { "myapp"： { "read"： { "created"： true __} } }

__

|

更新现有权限时，"created"设置为 false。   ---|--- 要添加多个权限，请向"/_security/特权/"端点提交 POST 请求。例如：

    
    
    PUT /_security/privilege
    {
      "app01": {
        "read": {
          "actions": [ "action:login", "data:read/*" ]
        },
        "write": {
          "actions": [ "action:login", "data:write/*" ]
        }
      },
      "app02": {
        "all": {
          "actions": [ "*" ]
        }
      }
    }

成功的调用会返回一个 JSON 结构，该结构显示权限是否已创建或更新。

    
    
    {
      "app02": {
        "all": {
          "created": true
        }
      },
      "app01": {
        "read": {
          "created": true
        },
        "write": {
          "created": true
        }
      }
    }

[« Create API key API](security-api-create-api-key.md) [Create or update
role mappings API »](security-api-put-role-mapping.md)
