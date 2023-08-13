

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Clear service account token caches API](security-api-clear-service-token-
caches.md) [Create or update application privileges API »](security-api-put-
privileges.md)

## 创建接口密钥接口

创建用于访问的 API 密钥，而无需基本身份验证。

###Request

"发布/_security/api_key"

"放/_security/api_key"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_own_api_key"群集权限。

如果用于对此请求进行身份验证的凭据是 API 密钥，则派生的 API 密钥不能具有任何权限。如果指定权限，API 将返回错误。请参阅"role_descriptors"下的注释。

###Description

API 密钥由自动启用的 Elasticsearch API 密钥服务创建。有关禁用 API 密钥服务的说明，请参阅 API 密钥服务设置。

成功的请求会返回一个 JSON 结构，其中包含 API 密钥、其唯一 ID 及其名称。如果适用，它还会返回 API 密钥的过期信息(以毫秒为单位)。

默认情况下，API 密钥永不过期。您可以在创建 API 密钥时指定过期信息。

有关与 API 密钥服务相关的配置设置，请参阅 API 密钥服务设置。

### 请求正文

可以在 POST 或 PUTrequest 的正文中指定以下参数：

`name`

     (Required, string) Specifies the name for this API key. 

`role_descriptors`

    

(可选，对象)此 API 密钥的角色描述符。此参数是可选的。如果未指定或为空数组，则 API 密钥将具有经过身份验证user_的权限的_point时间快照。如果提供角色描述符，则生成的权限将是 API 密钥权限和经过身份验证的用户权限的交集，从而限制了 API 密钥的访问范围。

由于此权限交集的计算方式，除非在没有任何权限的情况下创建派生密钥，否则无法创建作为另一个 API 密钥的子级的 API 密钥。在这种情况下，必须显式指定没有权限的角色描述符。派生的 API 密钥可用于身份验证;它无权调用Elasticsearch API。

`applications`

    

(列表)应用程序特权条目的列表。

"申请"(必填)

     (string) The name of the application to which this entry applies 
`privileges` (required)

     (list) A list of strings, where each element is the name of an application privilege or action. 
`resources` (required)

     (list) A list resources to which the privileges are applied. 

`cluster`

     (list) A list of cluster privileges. These privileges define the cluster level actions that API keys are able to execute. 
`global`

     (object) An object defining global privileges. A global privilege is a form of cluster privilege that is request-aware. Support for global privileges is currently limited to the management of application privileges. This field is optional. 
`indices`

    

(列表)索引权限条目的列表。

`field_security`

     (object) The document fields that the API keys have read access to. For more information, see [Setting up field and document level security](field-and-document-access-control.html "Setting up field and document level security"). 
`names` (required)

     (list) A list of indices (or index name patterns) to which the permissions in this entry apply. 
`privileges`(required)

     (list) The index level privileges that the API keys have on the specified indices. 
`query`

     A search query that defines the documents the API keys have read access to. A document within the specified indices must match this query in order for it to be accessible by the API keys. 

`metadata`

     (object) Optional meta-data. Within the `metadata` object, keys that begin with `_` are reserved for system usage. 
`restriction`

    

(对象)允许角色描述符生效的可选限制。更多信息，请参见角色限制。

`workflows`

    

(列表)API 密钥受限的工作流列表。有关完整列表，请参阅工作流。

为了使用角色限制，必须使用单角色描述符创建 API 密钥。

`run_as`

     (list) A list of users that the API keys can impersonate. For more information, see [Submitting requests on behalf of other users](run-as-privilege.html "Submitting requests on behalf of other users"). 

`expiration`

     (Optional, string) Expiration time for the API key. By default, API keys never expire. 
`metadata`

     (Optional, object) Arbitrary metadata that you want to associate with the API key. It supports nested data structure. Within the `metadata` object, keys beginning with `_` are reserved for system usage. 

###Examples

以下示例创建一个 API 密钥：

    
    
    POST /_security/api_key
    {
      "name": "my-api-key",
      "expiration": "1d",   __"role_descriptors": { __"role-a": {
          "cluster": ["all"],
          "indices": [
            {
              "names": ["index-a*"],
              "privileges": ["read"]
            }
          ]
        },
        "role-b": {
          "cluster": ["all"],
          "indices": [
            {
              "names": ["index-b*"],
              "privileges": ["all"]
            }
          ]
        }
      },
      "metadata": {
        "application": "my-application",
        "environment": {
           "level": 1,
           "trusted": true,
           "tags": ["dev", "staging"]
        }
      }
    }

__

|

正在生成的 API 密钥的可选过期时间。如果未提供过期时间，则 API 密钥不会过期。   ---|---    __

|

此 API 密钥的可选角色描述符。如果未提供，则应用经过身份验证的用户的权限。   成功的调用会返回提供 API 密钥信息的 JSON 结构。

    
    
    {
      "id": "VuaCfGcBCdbkQm-e5aOx",        __"name": "my-api-key",
      "expiration": 1544068612110, __"api_key": "ui2lp2axTNmsyakw9tvNnw", __"encoded": "VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw==" __}

__

|

此 API 密钥的唯一"id"---|--- __

|

此 API 密钥的可选过期时间(以毫秒为单位) __

|

生成的 API 密钥 __

|

API 密钥凭据，它是由冒号 ("：") 连接的 UTF-8 表示形式的 Base64 编码，由"id"和"api_key"连接。   要使用生成的 API 密钥，请发送带有"授权"标头的请求，该标头包含"ApiKey"前缀，后跟 API 密钥凭据(响应中的"编码"值)。

    
    
    curl -H "Authorization: ApiKey VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw==" \
    http://localhost:9200/_cluster/health\?pretty __

__

|

如果您的节点将"xpack.security.http.ssl.enabled"设置为"true"，则必须在创建API密钥时指定"https"---|--- 在类 Unix 系统上，可以使用以下命令创建"编码"值：

    
    
    echo -n "VuaCfGcBCdbkQm-e5aOx:ui2lp2axTNmsyakw9tvNnw" | base64 __

__

|

使用 '-n' 以便 'echo' 命令不会打印尾随换行符 ---|--- 以下示例创建一个 API 密钥，该密钥限制为"search_application_query"工作流，该工作流仅允许调用搜索应用程序搜索 API：

    
    
    POST /_security/api_key
    {
      "name": "my-restricted-api-key",
      "role_descriptors": {
        "my-restricted-role-descriptor": {
          "indices": [
            {
              "names": ["my-search-app"],
              "privileges": ["read"]
            }
          ],
          "restriction":  {
            "workflows": ["search_application_query"]
          }
        }
      }
    }

[« Clear service account token caches API](security-api-clear-service-token-
caches.md) [Create or update application privileges API »](security-api-put-
privileges.md)
