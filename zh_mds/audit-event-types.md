

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Enable audit logging](enable-audit-
logging.md)

[« Enable audit logging](enable-audit-logging.md) [Logfile audit output
»](audit-log-output.md)

## 审计事件

审核安全事件时，单个客户端请求可能会跨多个群集节点生成多个审核事件。通用的"request.id"属性可用于关联关联的事件。

使用 'elasticsearch.yml' 中的 'xpack.security.audit.logfile.events.include' 设置来指定要包含在审计输出中的事件类型。

某些审核事件需要"security_config_change"事件类型来审核相关事件操作。受影响的审核事件的说明指示是否需要该事件类型。

`access_denied`

    

当经过身份验证的用户尝试执行他们没有必要权限执行的操作时记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:30:06,949+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"transport", "event.action":
    "access_denied", "authentication.type":"REALM", "user.name":"user1",
    "user.realm":"default_native", "user.roles":["test_role"], "origin.type":
    "rest", "origin.address":"[::1]:52434", "request.id":"yKOgWn2CRQCKYgZRz3phJw",
    "action":"indices:admin/auto_create", "request.name":"CreateIndexRequest",
    "indices":["<index-{now/d+1d}>"]}

`access_granted`

    

当经过身份验证的用户尝试执行他们具有执行必要权限的操作时记录。将仅为非系统用户记录这些事件。

如果要为所有用户(包括内部用户，如"_xpack")添加"access_granted"事件，请在事件类型列表中添加"system_access_granted"以及"access_granted"。默认情况下不包括"system_access_granted"权限，以避免日志混乱。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:30:06,947+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"transport", "event.action":
    "access_granted", "authentication.type":"REALM", "user.name":"user1", "user
    realm":"default_native", "user.roles":["test_role"], "origin.type":"rest",
    "origin.address":"[::1]:52434", "request.id":"yKOgWn2CRQCKYgZRz3phJw",
    "action":"indices:data/write/bulk", "request.name":"BulkRequest"}

`anonymous_access_denied`

    

当请求因缺少身份验证凭据而被拒绝时记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T21:56:43,608+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"rest", "event.action":
    "anonymous_access_denied", "origin.type":"rest", "origin.address":
    "[::1]:50543", "url.path":"/twitter/_async_search", "url.query":"pretty",
    "request.method":"POST", "request.id":"TqA9OisyQ8WTl1ivJUV1AA"}

`authentication_failed`

    

当身份验证凭据无法与已知用户匹配时记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:10:15,510+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"rest", "event.action":
    "authentication_failed", "user.name":"elastic", "origin.type":"rest",
    "origin.address":"[::1]:51504", "url.path":"/_security/user/user1",
    "url.query":"pretty", "request.method":"POST",
    "request.id":"POv8p_qeTl2tb5xoFl0HIg"}

`authentication_success`

    

在用户成功进行身份验证时记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:03:35,018+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"rest", "event.action":
    "authentication_success", "authentication.type":"REALM", "user.name":
    "elastic", "user.realm":"reserved", "origin.type":"rest", "origin.address":
    "[::1]:51014", "realm":"reserved", "url.path":"/twitter/_search",
    "url.query":"pretty", "request.method":"POST",
    "request.id":"nHV3UMOoSiu-TaSPWCfxGg"}

`change_disable_user`

    

在调用启用用户 API 以禁用本机用户或内置用户时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T23:17:28,308+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.
    action":"change_disable_user", "request.id":"qvLIgw_eTvyK3cgV-GaLVg",
    "change":{"disable":{"user":{"name":"user1"}}}}

`change_enable_user`

    

在调用启用用户 API 以启用本机用户或内置用户时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T23:17:34,843+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.
    action":"change_enable_user", "request.id":"BO3QU3qeTb-Ei0G0rUOalQ",
    "change":{"enable":{"user":{"name":"user1"}}}}

`change_password`

    

在调用更改密码 API 以更改本机或内置用户的密码时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2019-12-30T22:19:41,345+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.
    action":"change_password", "request.id":"bz5a1Cc3RrebDMitMGGNCw",
    "change":{"password":{"user":{"name":"user1"}}}}

`create_service_token`

    

调用创建服务帐户令牌 API 为服务帐户创建新的基于索引的令牌时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2021-04-30T23:17:42,952+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.
    action":"create_service_token", "request.id":"az9a1Db5QrebDMacQ8yGKc",
    "create":{"service_token":{"namespace":"elastic","service":"fleet-server","name":"token1"}}}`

`connection_denied`

    

当传入的 TCP 连接未通过特定配置文件的 IP 筛选器时记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T21:47:31,526+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"ip_filter", "event.action":
    "connection_denied", "origin.type":"rest", "origin.address":"10.10.0.20:52314",
    "transport.profile":".http", "rule":"deny 10.10.0.0/16"}

`connection_granted`

    

当传入的 TCP 连接通过特定配置文件的 IP 筛选器时记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T21:47:31,526+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"ip_filter", "event.action":
    "connection_granted", "origin.type":"rest", "origin.address":"[::1]:52314",
    "transport.profile":".http", "rule":"allow ::1,127.0.0.1"}

`create_apikey`

    

调用创建 API 密钥或授予 API 密钥 API 来创建新的 API 密钥时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:33:52,521+0200", "node.id":
    "9clhpgjJRR-iKzOw20xBNQ", "event.type":"security_config_change", "event.action":
    "create_apikey", "request.id":"9FteCmovTzWHVI-9Gpa_vQ", "create":{"apikey":
    {"name":"test-api-key-1","expiration":"10d","role_descriptors":[{"cluster":
    ["monitor","manage_ilm"],"indices":[{"names":["index-a*"],"privileges":
    ["read","maintenance"]},{"names":["in*","alias*"],"privileges":["read"],
    "field_security":{"grant":["field1*","@timestamp"],"except":["field11"]}}],
    "applications":[],"run_as":[]},{"cluster":["all"],"indices":[{"names":
    ["index-b*"],"privileges":["all"]}],"applications":[],"run_as":[]}],
    "metadata":{"application":"my-application","environment":{"level": 1,
    "tags":["dev","staging"]}}}}}

`change_apikey`

    

调用更新 API 密钥 API 以更新现有 API 密钥的属性时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:33:52,521+0200", "node.id":
    "9clhpgjJRR-iKzOw20xBNQ", "event.type":"security_config_change", "event.action":
    "change_apikey", "request.id":"9FteCmovTzWHVI-9Gpa_vQ", "change":{"apikey":
    {"id":"zcwN3YEBBmnjw-K-hW5_","role_descriptors":[{"cluster":
    ["monitor","manage_ilm"],"indices":[{"names":["index-a*"],"privileges":
    ["read","maintenance"]},{"names":["in*","alias*"],"privileges":["read"],
    "field_security":{"grant":["field1*","@timestamp"],"except":["field11"]}}],
    "applications":[],"run_as":[]},{"cluster":["all"],"indices":[{"names":
    ["index-b*"],"privileges":["all"]}],"applications":[],"run_as":[]}],
    "metadata":{"application":"my-application","environment":{"level": 1,
    "tags":["dev","staging"]}}}}}

`change_apikeys`

    

在调用批量更新 API 密钥 API 以更新多个现有 API 密钥的属性时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit","timestamp":"2020-12-31T00:33:52,521+0200","node.id":
    "9clhpgjJRR-iKzOw20xBNQ","event.type":"security_config_change",
    "event.action":"change_apikeys","request.id":"9FteCmovTzWHVI-9Gpa_vQ",
    "change":{"apikeys":
    {"ids":["zcwN3YEBBmnjw-K-hW5_","j7c0WYIBqecB5CbVR6Oq"],"role_descriptors":
    [{"cluster":["monitor","manage_ilm"],"indices":[{"names":["index-a*"],"privileges":
    ["read","maintenance"]},{"names":["in*","alias*"],"privileges":["read"],
    "field_security":{"grant":["field1*","@timestamp"],"except":["field11"]}}],
    "applications":[],"run_as":[]},{"cluster":["all"],"indices":[{"names":
    ["index-b*"],"privileges":["all"]}],"applications":[],"run_as":[]}],
    "metadata":{"application":"my-application","environment":{"level":1,
    "tags":["dev","staging"]}}}}}

`delete_privileges`

    

调用删除应用程序权限 API 以删除一个或多个应用程序权限时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:39:30,246+0200", "node.id":
    "9clhpgjJRR-iKzOw20xBNQ", "event.type":"security_config_change", "event.
    action":"delete_privileges", "request.id":"7wRWVxxqTzCKEspeSP7J8g",
    "delete":{"privileges":{"application":"myapp","privileges":["read"]}}}

`delete_role`

    

调用删除角色 API 删除角色时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:08:11,678+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.action":
    "delete_role", "request.id":"155IKq3zQdWq-12dgKZRnw",
    "delete":{"role":{"name":"my_admin_role"}}}

`delete_role_mapping`

    

调用删除角色映射 API 以删除角色映射时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:12:09,349+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.
    action":"delete_role_mapping", "request.id":"Stim-DuoSTCWom0S_xhf8g",
    "delete":{"role_mapping":{"name":"mapping1"}}}

`delete_service_token`

    

调用删除服务帐户令牌 API 以删除服务帐户的基于索引的令牌时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2021-04-30T23:17:42,952+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.
    action":"delete_service_token", "request.id":"az9a1Db5QrebDMacQ8yGKc",
    "delete":{"service_token":{"namespace":"elastic","service":"fleet-server","name":"token1"}}}

`delete_user`

    

在调用删除用户 API 以删除特定本机用户时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:19:41,345+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change",
    "event.action":"delete_user", "request.id":"au5a1Cc3RrebDMitMGGNCw",
    "delete":{"user":{"name":"jacknich"}}}

`invalidate_apikeys`

    

在调用失效的 API 密钥 API 以使一个或多个 API 密钥失效时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:36:30,247+0200", "node.id":
    "9clhpgjJRR-iKzOw20xBNQ", "event.type":"security_config_change", "event.
    action":"invalidate_apikeys", "request.id":"7lyIQU9QTFqSrTxD0CqnTQ",
    "invalidate":{"apikeys":{"owned_by_authenticated_user":false,
    "user":{"name":"myuser","realm":"native1"}}}}

`put_privileges`

    

调用创建或更新权限 API 以添加或更新一个或多个应用程序权限时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:39:07,779+0200", "node.id":
    "9clhpgjJRR-iKzOw20xBNQ", "event.type":"security_config_change",
    "event.action":"put_privileges", "request.id":"1X2VVtNgRYO7FmE0nR_BGA",
    "put":{"privileges":[{"application":"myapp","name":"read","actions":
    ["data:read/*","action:login"],"metadata":{"description":"Read access to myapp"}}]}}

`put_role`

    

调用创建或更新角色 API 来创建或更新角色时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:27:01,978+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change",
    "event.action":"put_role", "request.id":"tDYQhv5CRMWM4Sc5Zkk2cQ",
    "put":{"role":{"name":"test_role","role_descriptor":{"cluster":["all"],
    "indices":[{"names":["apm*"],"privileges":["all"],"field_security":
    {"grant":["granted"]},"query":"{\"term\": {\"service.name\": \"bar\"}}"},
    {"names":["apm-all*"],"privileges":["all"],"query":"{\"term\":
    {\"service.name\": \"bar2\"}}"}],"applications":[],"run_as":[]}}}}

`put_role_mapping`

    

调用创建或更新角色映射 API 以创建或更新角色映射时记录。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-31T00:11:13,932+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change", "event.
    action":"put_role_mapping", "request.id":"kg4h1l_kTDegnLC-0A-XxA",
    "put":{"role_mapping":{"name":"mapping1","roles":["user"],"rules":
    {"field":{"username":"*"}},"enabled":true,"metadata":{"version":1}}}}

`put_user`

    

调用创建或更新用户 API 以创建或更新本机用户时记录。请注意，用户更新也可以更改用户的密码。

您必须包含"security_config_change"事件类型才能审核相关事件操作。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:10:09,749+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"security_config_change",
    "event.action":"put_user", "request.id":"VIiSvhp4Riim_tpkQCVSQA",
    "put":{"user":{"name":"user1","enabled":false,"roles":["admin","other_role1"],
    "full_name":"Jack Sparrow","email":"jack@blackpearl.com",
    "has_password":true,"metadata":{"cunning":10}}}}

`realm_authentication_failed`

    

为未能提供有效身份验证令牌的每个领域记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:10:15,510+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"rest", "event.action":
    "realm_authentication_failed", "user.name":"elastic", "origin.type":"rest",
    "origin.address":"[::1]:51504", "realm":"myTestRealm1", "url.path":
    "/_security/user/user1", "url.query":"pretty", "request.method":"POST",
    "request.id":"POv8p_qeTl2tb5xoFl0HIg"}

`run_as_denied`

    

当经过身份验证的用户尝试以其他用户身份运行，而他们没有必要的权限时记录。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:49:34,859+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"transport", "event.action":
    "run_as_denied", "user.name":"user1", "user.run_as.name":"user1",
    "user.realm":"default_native", "user.run_as.realm":"default_native",
    "user.roles":["test_role"], "origin.type":"rest", "origin.address":
    "[::1]:52662", "request.id":"RcaSt872RG-R_WJBEGfYXA",
    "action":"indices:data/read/search", "request.name":"SearchRequest", "indices":["alias1"]}

`run_as_granted`

    

当经过身份验证的用户尝试以其他用户身份运行时记录，该用户具有执行此操作所需的权限。

Example

    
    
    {"type":"audit", "timestamp":"2020-12-30T22:44:42,068+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type":"transport", "event.action":
    "run_as_granted", "user.name":"elastic", "user.run_as.name":"user1",
    "user.realm":"reserved", "user.run_as.realm":"default_native",
    "user.roles":["superuser"], "origin.type":"rest", "origin.address":
    "[::1]:52623", "request.id":"dGqPTdEQSX2TAPS3cvc1qA", "action":
    "indices:data/read/search", "request.name":"SearchRequest", "indices":["alias1"]}

`system_access_granted`

    

仅记录内部用户的"access_granted"事件，例如"_xpack"。如果除了"access_granted"之外还包括此设置，则会为 _all_ 用户记录"access_granted"事件。

默认情况下禁用此事件类型，以避免日志混乱。

`tampered_request`

    

在安全功能检测到请求已被篡改时记录。通常与"搜索/滚动"请求有关，当滚动 ID 被认为已被篡改时。

Example

    
    
    {"type":"audit", "timestamp":"2019-11-27T22:00:00,947+0200", "node.id":
    "0RMNyghkQYCc_gVd1G6tZQ", "event.type": "rest", "event.action":
    "tampered_request", "origin.address":"[::1]:50543", "url.path":
    "/twitter/_async_search", "url.query":"pretty", "request.method":"POST",
    "request.id":"TqA9OisyQ8WTl1ivJUV1AA"}

### 审核事件属性

审核事件的格式为 JSON 文档，并且每个事件都打印在审核日志中的单独行上。条目本身不包含行尾分隔符。有关详细信息，请参阅日志条目格式。

以下列表显示了所有审核事件类型通用的属性：

`@timestamp`

     The time, in ISO9601 format, when the event occurred. 
`node.name`

     The name of the node. This can be changed in the `elasticsearch.yml` config file. 
`node.id`

     The node id. This is automatically generated and is persistent across full cluster restarts. 
`host.ip`

     The bound IP address of the node, with which the node can be communicated with. 
`host.name`

     The unresolved node's hostname. 
`event.type`

     The internal processing layer that generated the event: `rest`, `transport`, `ip_filter` or `security_config_change`. This is different from `origin.type` because a request originating from the REST API is translated to a number of transport messages, generating audit events with `origin.type: rest` and `event.type: transport`. 
`event.action`

    

发生的事件类型："anonymous_access_denied"、"authentication_failed"、"authentication_success"、"realm_authentication_failed"、"access_denied"、"access_granted"、"connection_denied"、"connection_granted"、"tampered_request"、"run_as_denied"或"run_as_granted"。

此外，如果"event.type"等于"security_config_change"，则"event.action"属性采用以下值之一："put_user"、"change_password"、"put_role"、"put_role_mapping"、"change_enable_user"、"change_disable_user"、"put_privileges"、"create_apikey"、"delete_user"、"delete_role"、"delete_role_mapping"、"invalidate_apikeys"、"delete_privileges"、"change_apikey"或"change_apikeys"。

`request.id`

     A synthetic identifier that can be used to correlate the events associated with a particular REST request. 

此外，类型"rest"、"transport"和"ip_filter"(但不是"security_config_change")的所有事件都具有以下额外属性，这些属性显示有关请求客户端的更多详细信息：

`origin.address`

     The source IP address of the request associated with this event. This could be the address of the remote client, the address of another cluster node, or the local node's bound address, if the request originated locally. Unless the remote client connects directly to the cluster, the _client address_ will actually be the address of the first OSI layer 3 proxy in front of the cluster. 
`origin.type`

     The origin type of the request associated with this event: `rest` (request originated from a REST API request), `transport` (request was received on the transport channel), or `local_node` (the local node issued the request). 
`opaque_id`

     The value of the `X-Opaque-Id` HTTP header (if present) of the request associated with this event. See more: [`X-Opaque-Id` HTTP header - API conventions](api-conventions.html#x-opaque-id "X-Opaque-Id HTTP header")
`trace_id`

     The identifier extracted from the `traceparent` HTTP header (if present) of the request associated with this event. It allows to surface audit logs into the Trace Logs feature of Elastic APM. 
`x_forwarded_for`

     The verbatim value of the `X-Forwarded-For` HTTP request header (if present) of the request associated with the audit event. This header is commonly added by proxies when they forward requests and the value is the address of the proxied client. When a request crosses multiple proxies the header is a comma delimited list with the last value being the address of the second to last proxy server (the address of the last proxy server is designated by the `origin.address` field). 

### 审核"休息"事件类型的事件属性

"event.type"等于"rest"的事件具有以下"event.action"属性值之一："authentication_success"、"anonymous_access_denied"、"authentication_failed"、"realm_authentication_failed"、"tampered_request"或"run_as_denied"。这些事件还具有以下额外属性(除了公共属性)：

`url.path`

     The path part of the URL (between the port and the query string) of the REST request associated with this event. This is URL encoded. 
`url.query`

     The query part of the URL (after "?", if present) of the REST request associated with this event. This is URL encoded. 
`request.method`

     The HTTP method of the REST request associated with this event. It is one of GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, TRACE and CONNECT. 
`request.body`

     The full content of the REST request associated with this event, if enabled. This contains the HTTP request body. The body is escaped as a string value according to the JSON RFC 4627. 

### 审核"传输"事件类型的事件属性

"event.type"等于"传输"的事件具有以下"event.action"属性值之一："authentication_success"、"anonymous_access_denied"、"authentication_failed"、"realm_authentication_failed"、"access_granted"、"access_denied"、"run_as_granted"、"run_as_denied"或"tampered_request"。这些事件还具有以下额外属性(除了常见属性)：

`action`

     The name of the transport action that was executed. This is like the URL for a REST request. 
`indices`

     The indices names array that the request associated with this event pertains to (when applicable). 
`request.name`

     The name of the request handler that was executed. 

### 审核"ip_filter"事件类型的事件属性

"event.type"等于"ip_filter"的事件具有以下"event.action"属性值之一："connection_granted"或"connection_denied"。这些事件还具有以下额外属性(除了常见属性)：

`transport_profile`

     The transport profile the request targeted. 
`rule`

     The [IP filtering](ip-filtering.html "Restricting connections with IP filtering") rule that denied the request. 

### 审核"security_config_change"事件类型的事件属性

属性等于"event.type"等于"security_config_change"的事件具有以下"event.action"属性值之一："put_user"、"change_password"、"put_role"、"put_role_mapping"、"change_enable_user"、"change_disable_user"、"put_privileges"、"create_apikey"、"delete_user"、"delete_role"、"delete_role_mapping"、"invalidate_apikeys"、"delete_privileges"、"change_apikey"或"change_apikeys"。

这些事件还具有以下额外属性中的**一个**(除了公共属性之外)，这些属性特定于"event.type"属性。属性的值是一个嵌套的 JSON 对象：

`put`

     The object representation of the security config that is being created, or the overwrite of an existing config. It contains the config for a `user`, `role`, `role_mapping`, or for application `privileges`. 
`delete`

     The object representation of the security config that is being deleted. It can be the config for a `user`, `role`, `role_mapping` or for application `privileges`. 
`change`

     The object representation of the security config that is being changed. It can be the `password`, `enable` or `disable`, config object for native or built-in users. If an API key is updated, the config object will be an `apikey`. 
`create`

     The object representation of the new security config that is being created. This is currently only used for API keys auditing. If the API key is created using the [create API key API](security-api-create-api-key.html "Create API key API") it only contains an `apikey` config object. If the API key is created using the [grant API key API](security-api-grant-api-key.html "Grant API key API") it also contains a `grant` config object. 
`invalidate`

     The object representation of the security configuration that is being invalidated. The only config that currently supports invalidation is `apikeys`, through the [invalidate API key API](security-api-invalidate-api-key.html "Invalidate API key API"). 

上面提到的安全配置对象的架构如下。它们与相应安全 API 的请求正文非常相似。

`user`

    

像这样的对象：

    
    
    `{"name": <string>, "enabled": <boolean>, "roles": <string_list>,
    "full_name": <string>, "email": <string>, "has_password": <boolean>,
    "metadata": <object>}`.

如果为空，则省略"full_name"、"电子邮件"和"元数据"字段。

`role`

    

像这样的对象：

    
    
    `{"name": <string>, "role_descriptor": {"cluster": <string_list>, "global":
    {"application":{"manage":{<string>:<string_list>}}}, "indices": [                             {"names": <string_list>, "privileges": <string_list>, "field_security":
    {"grant": <string_list>, "except": <string_list>}, "query": <string>,
    "allow_restricted_indices": <boolean>}], "applications":[{"application": <string>,
    "privileges": <string_list>, "resources": <string_list>}], "run_as": <string_list>,
    "metadata": <object>}}`.

如果为空，则省略"全局"、"field_security"、"除外"、"查询"、"allow_restricted_indices"和"元数据"字段。

`role_mapping`

    

像这样的对象：

    
    
    `{"name": <string>, "roles": <string_list>, "role_templates": [{"template": <string>,
    "format": <string>}], "rules": <object>, "enabled": <boolean>, "metadata": <object>}`.

如果为空，则省略"角色"和"role_templates"字段。"rules"对象具有递归嵌套的架构，与映射角色的 API 请求中传递的架构相同。

`privileges`

    

对象数组，如下所示：

    
    
    `{"application": <string>, "name": <string>, "actions": <string_list>,
    "metadata": <object>}`.

`password`

    

一个简单的对象，如下所示：

    
    
    `{"user":{"name": <string>}}`

`enable`

    

一个简单的对象，如下所示：

    
    
    `{"user":{"name": <string>}}`

`disable`

    

一个简单的对象，如下所示：

    
    
    `{"user":{"name": <string>}}`

`apikey`

    

像这样的对象：

    
    
    `{"id": <string>, "name": <string>, "expiration": <string>, "role_descriptors": [<object>],
    "metadata": [<object>]}`

"role_descriptors"对象与作为上述"角色"配置对象一部分的"role_descriptor"对象具有相同的架构。

API 密钥更新的对象将有所不同，因为它不包含"名称"或"过期"。

`grant`

    

像这样的对象：

    
    
    `{"type": <string>, "user": {"name": <string>, "has_password": <boolean>},
    "has_access_token": <boolean>}`

`apikeys`

    

像这样的对象：

    
    
    `{"ids": <string_list>, "name": <string>, "owned_by_authenticated_user":
    <boolean>, "user":{"name": <string>, "realm": <string>}}`

批量 API 密钥更新的对象将有所不同，因为它不包含"名称"、"owned_by_authenticated_user"或"用户"。相反，它可能包括"元数据"和"role_descriptors"，它们与上面"apikey"配置对象中的字段具有相同的架构。

`service_token`

    

像这样的对象：

    
    
    `{"namespace":<string>,"service":<string>,"name":<string>}`

### 特定事件的额外审核事件属性

除了前面描述的事件之外，还有一些事件具有更多属性：

* "authentication_success"：

`realm`

     The name of the realm that successfully authenticated the user. If authenticated using an API key, this is the special value of `_es_api_key`. This is a shorthand attribute for the same information that is described by the `user.realm`, `user.run_by.realm` and `authentication.type` attributes. 
`user.name`

     The name of the _effective_ user. This is usually the same as the _authenticated_ user, but if using the [run as authorization functionality](run-as-privilege.html "Submitting requests on behalf of other users") this instead denotes the name of the _impersonated_ user. If authenticated using an API key, this is the name of the API key owner. If authenticated using a service account token, this is the service account principal, i.e. `namespace/service_name`. 
`user.realm`

     Name of the realm to which the _effective_ user belongs. If authenticated using an API key, this is the name of the realm to which the API key owner belongs. 
`user.run_by.name`

     This attribute is present only if the request is using the [run as authorization functionality](run-as-privilege.html "Submitting requests on behalf of other users") and denotes the name of the _authenticated_ user, which is also known as the _impersonator_. 
`user.run_by.realm`

     Name of the realm to which the _authenticated_ ( _impersonator_ ) user belongs. This attribute is provided only if the request uses the [run as authorization functionality](run-as-privilege.html "Submitting requests on behalf of other users"). 
`authentication.type`

     Method used to authenticate the user. Possible values are `REALM`, `API_KEY`, `TOKEN`, `ANONYMOUS` or `INTERNAL`. 
`apikey.id`

     API key ID returned by the [create API key](security-api-create-api-key.html "Create API key API") request. This attribute is only provided for authentication using an API key. 
`apikey.name`

     API key name provided in the [create API key](security-api-create-api-key.html "Create API key API") request. This attribute is only provided for authentication using an API key. 
`authentication.token.name`

     Name of the [service account](service-accounts.html "Service accounts") token. This attribute is only provided for authentication using a service account token. 
`authentication.token.type`

     Type of the [service account](service-accounts.html "Service accounts") token. This attribute is only provided for authentication using a service account token. 

* "authentication_failed"：

`user.name`

     The name of the user that failed authentication. If the request authentication token is invalid or unparsable, this information might be missing. 
`authentication.token.name`

     Name of the [service account](service-accounts.html "Service accounts") token. This attribute is only provided for authentication using a service account token. If the request authentication token is invalid or unparsable, this information might be missing. 
`authentication.token.type`

     Type of the [service account](service-accounts.html "Service accounts") token. This attribute is only provided for authentication using a service account token. If the request authentication token is invalid or unparsable, this information might be missing. 

* "realm_authentication_failed"：

`user.name`

     The name of the user that failed authentication. 
`realm`

     The name of the realm that rejected this authentication. **This event is generated for each consulted realm in the chain.**

* "run_as_denied"和"run_as_granted"：

`user.roles`

     The role names as an array of the _authenticated_ user which is being granted or denied the _impersonation_ action. If authenticated as a [service account](service-accounts.html "Service accounts"), this is always an empty array. 
`user.name`

     The name of the _authenticated_ user which is being granted or denied the _impersonation_ action. 
`user.realm`

     The realm name that the _authenticated_ user belongs to. 
`user.run_as.name`

     The name of the user as which the _impersonation_ action is granted or denied. 
`user.run_as.realm`

     The realm name of that the _impersonated_ user belongs to. 

* "access_granted"和"access_denied"：

`user.roles`

     The role names of the user as an array. If authenticated using an API key, this contains the role names of the API key owner. If authenticated as a [service account](service-accounts.html "Service accounts"), this is always an empty array. 
`user.name`

     The name of the _effective_ user. This is usually the same as the _authenticated_ user, but if using the [run as authorization functionality](run-as-privilege.html "Submitting requests on behalf of other users") this instead denotes the name of the _impersonated_ user. If authenticated using an API key, this is the name of the API key owner. 
`user.realm`

     Name of the realm to which the _effective_ user belongs. If authenticated using an API key, this is the name of the realm to which the API key owner belongs. 
`user.run_by.name`

     This attribute is present only if the request is using the [run as authorization functionality](run-as-privilege.html "Submitting requests on behalf of other users") and denoted the name of the _authenticated_ user, which is also known as the _impersonator_. 
`user.run_by.realm`

     This attribute is present only if the request is using the [run as authorization functionality](run-as-privilege.html "Submitting requests on behalf of other users") and denotes the name of the realm that the _authenticated_ ( _impersonator_ ) user belongs to. 
`authentication.type`

     Method used to authenticate the user. Possible values are `REALM`, `API_KEY`, `TOKEN`, `ANONYMOUS` or `INTERNAL`. 
`apikey.id`

     API key ID returned by the [create API key](security-api-create-api-key.html "Create API key API") request. This attribute is only provided for authentication using an API key. 
`apikey.name`

     API key name provided in the [create API key](security-api-create-api-key.html "Create API key API") request. This attribute is only provided for authentication using an API key. 
`authentication.token.name`

     Name of the [service account](service-accounts.html "Service accounts") token. This attribute is only provided for authentication using a service account token. 
`authentication.token.type`

     Type of the [service account](service-accounts.html "Service accounts") token. This attribute is only provided for authentication using a service account token. 

[« Enable audit logging](enable-audit-logging.md) [Logfile audit output
»](audit-log-output.md)
