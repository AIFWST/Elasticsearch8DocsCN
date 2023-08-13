

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Migration
guide](breaking-changes.md)

[« Migrating to 8.4](migrating-8.4.md) [Migrating to 8.2
»](migrating-8.2.md)

## 迁移到 8.3

本节讨论在将应用程序迁移到 Elasticsearch 8.3 时需要注意的更改。

另请参阅_What发行说明中的新增8.9_and。

### 重大变更

Elasticsearch 8.3 中没有重大更改。

###Deprecations

以下功能已在 Elasticsearch 8.3 中弃用，并将在未来的版本中删除。虽然这不会对应用程序产生直接影响，但我们强烈建议您在升级到 8.3 后采取所述步骤来更新代码。

若要了解是否正在使用任何已弃用的功能，请启用弃用日志记录。

#### 群集和节点设置弃用

不推荐在 LDAP 或活动目录 (AD) 域中配置绑定 DN 而不使用相应的绑定密码

**详细信息** 对于 LDAP 或 AD 身份验证领域，在没有绑定密码的情况下设置绑定 DN(通过"xpack.security.authc.realms.ldap.*.bind_dn"领域设置)是配置错误，可能会阻止对节点的成功身份验证。在下一个主要版本中，如果在没有密码的情况下指定绑定 DN，节点将无法启动。

**影响** 如果您为 LDAP 或 AD 身份验证领域配置了绑定 DN，请为 LDAP 或 ActiveDirectory 设置绑定密码。配置没有密码的绑定 DN 会在弃用日志中生成警告。

**注意：** 仅当当前 LDAP 或 AD配置指定了没有密码的绑定 DN 时，此弃用才适用。这种情况不太可能，但可能会影响一小部分用户。

[« Migrating to 8.4](migrating-8.4.md) [Migrating to 8.2
»](migrating-8.2.md)
