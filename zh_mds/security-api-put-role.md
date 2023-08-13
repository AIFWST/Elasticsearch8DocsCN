

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Create or update role mappings API](security-api-put-role-mapping.md)
[Create or update users API »](security-api-put-user.md)

## 创建或更新角色接口

在本机域中添加和更新角色。

###Request

"发布/_security/角色/<name>"

"放置/_security/角色/<name>"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

角色管理 API 通常是管理角色的首选方式，而不是使用基于文件的角色管理。创建或更新角色 API 无法更新角色文件中定义的角色。

### 路径参数

`name`

     (string) The name of the role. 

### 请求正文

可以在 PUT 或 POST 请求的正文中指定以下参数，这些参数与添加角色有关：

`applications`

    

(列表)应用程序特权条目的列表。

"申请"(必填)

     (string) The name of the application to which this entry applies 
`privileges`

     (list) A list of strings, where each element is the name of an application privilege or action. 
`resources`

     (list) A list resources to which the privileges are applied. 

`cluster`

     (list) A list of cluster privileges. These privileges define the cluster level actions that users with this role are able to execute. 
`global`

     (object) An object defining global privileges. A global privilege is a form of cluster privilege that is request-aware. Support for global privileges is currently limited to the management of application privileges. This field is optional. 
`indices`

    

(列表)索引权限条目的列表。

`field_security`

     (object) The document fields that the owners of the role have read access to. For more information, see [Setting up field and document level security](field-and-document-access-control.html "Setting up field and document level security"). 
`names` (required)

     (list) A list of indices (or index name patterns) to which the permissions in this entry apply. 
`privileges`(required)

     (list) The index level privileges that the owners of the role have on the specified indices. 
`query`

     A search query that defines the documents the owners of the role have read access to. A document within the specified indices must match this query in order for it to be accessible by the owners of the role. 

`metadata`

     (object) Optional meta-data. Within the `metadata` object, keys that begin with `_` are reserved for system usage. 
`run_as`

     (list) A list of users that the owners of this role can impersonate. For more information, see [Submitting requests on behalf of other users](run-as-privilege.html "Submitting requests on behalf of other users"). 

有关更多信息，请参阅定义角色。

###Examples

以下示例添加一个名为"my_admin_role"的角色：

    
    
    POST /_security/role/my_admin_role
    {
      "cluster": ["all"],
      "indices": [
        {
          "names": [ "index1", "index2" ],
          "privileges": ["all"],
          "field_security" : { // optional
            "grant" : [ "title", "body" ]
          },
          "query": "{\"match\": {\"title\": \"foo\"}}" // optional
        }
      ],
      "applications": [
        {
          "application": "myapp",
          "privileges": [ "admin", "read" ],
          "resources": [ "*" ]
        }
      ],
      "run_as": [ "other_user" ], // optional
      "metadata" : { // optional
        "version" : 1
      }
    }

成功的调用会返回一个 JSON 结构，该结构显示角色是否已创建或更新。

    
    
    {
      "role": {
        "created": true __}
    }

__

|

更新现有角色时，"created"设置为 false。   ---|--- 以下示例配置了一个可以在 JDBC 中运行 SQL 的角色：

    
    
    POST /_security/role/cli_or_drivers_minimal
    {
      "cluster": ["cluster:monitor/main"],
      "indices": [
        {
          "names": ["test"],
          "privileges": ["read", "indices:admin/get"]
        }
      ]
    }

[« Create or update role mappings API](security-api-put-role-mapping.md)
[Create or update users API »](security-api-put-user.md)
