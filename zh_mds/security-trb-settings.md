

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Troubleshooting security](security-troubleshooting.md) [Authorization
exceptions »](security-trb-roles.md)

## 某些设置不会通过节点设置API 返回

**Symptoms:**

* 使用节点信息 API 检索节点的设置时，缺少某些信息。

**Resolution:**

这是故意的。某些设置被认为是高度敏感的：所有"ssl"设置、ldap"bind_dn"和"bind_password"。因此，我们会筛选这些设置，并且不会通过节点信息 APIrest 终结点公开它们。您还可以使用"xpack.security.hide_settings"设置定义应隐藏的其他敏感设置。例如，此片段隐藏了"ldap1"领域的"url"设置和"ad1"领域的所有设置。

    
    
    xpack.security.hide_settings: xpack.security.authc.realms.ldap1.url,
    xpack.security.authc.realms.ad1.*

[« Troubleshooting security](security-troubleshooting.md) [Authorization
exceptions »](security-trb-roles.md)
