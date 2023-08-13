

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Secure settings](secure-settings.md) [Circuit breaker settings
»](circuit-breaker.md)

## 审核安全设置

您可以使用审核日志记录来记录与安全相关的事件，例如身份验证失败、拒绝连接和数据访问事件。此外，还会记录通过 API 对安全配置的更改，例如创建、更新和删除本机和内置用户、角色、角色映射和 API 密钥。

审核日志仅在某些订阅级别可用。有关详细信息，请参阅 https://www.elastic.co/subscriptions。

如果已配置，则必须在群集中的每个节点上设置审核设置。静态设置，如"xpack.security.audit.enabled"，必须在每个节点上的"elasticsearch.yml"中配置。对于动态审核设置，请使用群集更新设置 API 来确保所有节点上的设置相同。

### 常规审核设置

`xpack.security.audit.enabled`

    

(静态)设置为"true"以在节点上启用审核。默认值为"false"。这会将审核事件放在<clustername>每个节点上名为"_audit.json"的专用文件中。

如果启用，则必须在群集中所有节点上的"elasticsearch.yml"中配置此设置。

### 审核事件设置

可以使用以下设置来控制事件和有关记录内容的其他一些信息：

`xpack.security.audit.logfile.events.include`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Specifies the [kind of events](audit-event-types.html "Audit events") to print in the auditing output. In addition, `_all` can be used to exhaustively audit all the events, but this is usually discouraged since it will get very verbose. The default list value contains: `access_denied, access_granted, anonymous_access_denied, authentication_failed, connection_denied, tampered_request, run_as_denied, run_as_granted, security_config_change`. 

`xpack.security.audit.logfile.events.exclude`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Excludes the specified [kind of events](audit-event-types.html "Audit events") from the include list. This is useful in the case where the `events.include` setting contains the special value `_all`. The default is the empty list. 

`xpack.security.audit.logfile.events.emit_request_body`

    

(动态)指定是否将来自 REST 请求的完整请求正文作为某些类型的审核事件的属性包含在内。此设置可用于审核搜索查询。

默认值为"false"，因此不会打印请求正文。

请注意，在审核事件中包含请求正文时，可能会以纯文本形式审核敏感数据，即使所有安全 API(例如更改用户密码的 API)在审核时都过滤掉了凭据。

### 本地节点信息设置

`xpack.security.audit.logfile.emit_node_name`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Specifies whether to include the [node name](important-settings.html#node-name "Node name setting") as a field in each audit event. The default value is `false`. 

`xpack.security.audit.logfile.emit_node_host_address`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Specifies whether to include the node's IP address as a field in each audit event. The default value is `false`. 

`xpack.security.audit.logfile.emit_node_host_name`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Specifies whether to include the node's host name as a field in each audit event. The default value is `false`. 

`xpack.security.audit.logfile.emit_node_id`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Specifies whether to include the node id as a field in each audit event. Unlike [node name](important-settings.html#node-name "Node name setting"), whose value might change if the administrator changes the setting in the config file, the node id will persist across cluster restarts and the administrator cannot change it. The default value is `true`. 

### 审核日志文件事件忽略策略

以下设置会影响忽略策略，这些策略可以精细控制将哪些审核事件打印到日志文件。具有相同策略名称的所有设置组合在一起形成一个策略。如果某个事件与任何策略的所有条件匹配，则会忽略该事件，并且不会打印该事件。大多数审核事件都受忽略策略的约束。唯一的例外是"security_config_change"类型的事件，除非完全排除，否则无法过滤掉。

`xpack.security.audit.logfile.events.ignore_filters.<policy_name>.users`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A list of user names or wildcards. The specified policy will not print audit events for users matching these values. 

`xpack.security.audit.logfile.events.ignore_filters.<policy_name>.realms`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A list of authentication realm names or wildcards. The specified policy will not print audit events for users in these realms. 

`xpack.security.audit.logfile.events.ignore_filters.<policy_name>.actions`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A list of action names or wildcards. Action name can be found in the `action` field of the audit event. The specified policy will not print audit events for actions matching these values. 

`xpack.security.audit.logfile.events.ignore_filters.<policy_name>.roles`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A list of role names or wildcards. The specified policy will not print audit events for users that have these roles. If the user has several roles, some of which are **not** covered by the policy, the policy will **not** cover this event. 

`xpack.security.audit.logfile.events.ignore_filters.<policy_name>.indices`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A list of index names or wildcards. The specified policy will not print audit events when all the indices in the event match these values. If the event concerns several indices, some of which are **not** covered by the policy, the policy will **not** cover this event. 

[« Secure settings](secure-settings.md) [Circuit breaker settings
»](circuit-breaker.md)
