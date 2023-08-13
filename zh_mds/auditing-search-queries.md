

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Enable audit logging](enable-audit-
logging.md)

[« Logfile audit events ignore policies](audit-log-ignore-policy.md)
[Restricting connections with IP filtering »](ip-filtering.md)

## 审核搜索查询

没有专门用于搜索查询的审核事件类型。分析搜索查询，然后进行处理;处理将触发已审核的授权操作。但是，当发生授权审核时，客户端提交的原始原始查询在下游无法访问。

但是，搜索查询包含在 HTTP 请求正文中，并且可以切换由协调节点上的 REST 层生成的某些审核事件，以将请求正文输出到审核日志中。因此，必须审核请求正文才能审核搜索查询。

要使某些审核事件包含请求正文，请在"elasticsearch.yml"文件中编辑以下设置：

    
    
    xpack.security.audit.logfile.events.emit_request_body: true

审核时不执行筛选，因此当审核事件包含请求正文时，可能会以纯文本形式审核敏感数据。此外，请求正文可能包含恶意内容，这些内容可能会破坏使用审核日志的分析器。

请求正文作为转义的 JSON 字符串值 (RFC 4627) 打印到"request.body"事件属性。

并非所有事件都包含 'request.body' 属性，即使切换了上述设置也是如此。执行的操作是："authentication_success"、"authentication_failed"、"realm_authentication_failed"、"tampered_request"、"run_as_denied"和"anonymous_access_denied"。"request.body"属性仅打印在协调节点(处理 RESTrequest 的节点)上。默认情况下，不包括这些事件类型中的大多数。

一个很好的实用建议是将"authentication_success"添加到已审核的事件类型中(将其添加到"xpack.security.audit.logfile.events.include"中的列表中)，因为默认情况下不会审核此事件类型。

通常，包含列表还包含其他事件类型，例如"access_granted"或"access_denied"。

[« Logfile audit events ignore policies](audit-log-ignore-policy.md)
[Restricting connections with IP filtering »](ip-filtering.md)
