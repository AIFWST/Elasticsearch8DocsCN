

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Enable audit logging](enable-audit-
logging.md)

[« Logfile audit output](audit-log-output.md) [Auditing search queries
»](auditing-search-queries.md)

## 日志文件审核事件忽略策略

全面的审计跟踪对于确保问责制是必要的。它在事件响应期间提供了巨大的价值，甚至可以用于证明合规性。

审计系统的缺点表现为不可避免的性能损失。事实上，审计跟踪花费了 _I/O ops_，这些不再可用于用户的查询。有时，审计跟踪的详细程度可能会成为由"包含"和"排除"定义的事件类型限制无法缓解的问题。

**审核事件忽略策略**是调整审核跟踪详细程度的更好方法。这些策略定义与将be_ignored_的审核事件匹配的规则(读作：未打印)。规则与审计事件的属性值匹配，并补充"包含"或"排除"方法。想象一下，审计事件的语料库和策略切断了不需要的事件。除了唯一的例外，所有审核事件都受忽略策略的约束。例外是类型为"security_config_change"的事件，除非完全排除，否则无法过滤掉。

当利用审计事件忽略策略时，您承认潜在的责任差距，这些差距可能使非法行为无法检测到。每当系统架构发生变化时，请花点时间查看这些策略。

策略是一组命名的筛选规则。每个筛选规则都适用于单个事件属性，即"用户"、"领域"、"操作"、"角色"或"索引"属性之一。筛选规则定义一个 Lucene 正则表达式列表，其中的 **any** 必须与审核事件属性的值匹配，规则才能匹配。如果包含策略的规则与事件匹配，则策略与事件匹配。如果审核事件与 **any** 策略匹配，则忽略该事件，因此不会打印该事件。所有其他不匹配的事件都照常打印。

所有策略都在"xpack.security.audit.logfile.events.ignore_filters"设置命名空间下定义。例如，以下名为 _example1_ 的策略匹配来自the_kibana_system_或_admin_user_主体的事件，这些主体通过通配符形式的索引 _app-logs*_ 进行操作：

    
    
    xpack.security.audit.logfile.events.ignore_filters:
      example1:
        users: ["kibana_system", "admin_user"]
        indices: ["app-logs*"]

由_kibana_system_用户生成的审计事件和操作过多的索引(其中一些与索引通配符不匹配)将不匹配。正如预期的那样，所有其他用户生成的操作(甚至仅在与 _index_ 筛选器匹配的索引上运行)也与此策略不匹配。

不同类型的审核事件可能具有不同的属性。如果事件不包含某些策略为其定义筛选器的属性，则该事件将与策略不匹配。例如，无论用户的角色如何，以下策略都不会匹配"authentication_success"或"authentication_failed"事件，因为这些事件架构不包含"role"属性：

    
    
    xpack.security.audit.logfile.events.ignore_filters:
      example2:
        roles: ["admin", "ops_admin_*"]

同样，具有多个角色的用户的任何事件(其中一些与正则表达式不匹配)将与此策略不匹配。

为了完整起见，尽管实际用例应该是稀疏的，但过滤器可以使用空字符串 ("") 或空列表 ([]) 匹配事件的缺失属性。例如，以下策略将匹配没有"索引"属性("anonymous_access_denied"、"authentication_success"和其他类型的事件)以及_next_index的事件。

    
    
    xpack.security.audit.logfile.events.ignore_filters:
      example3:
        indices: ["next", ""]

[« Logfile audit output](audit-log-output.md) [Auditing search queries
»](auditing-search-queries.md)
