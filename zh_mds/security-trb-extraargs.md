

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Authorization exceptions](security-trb-roles.md) [Users are frequently
locked out of Active Directory »](trouble-shoot-active-directory.md)

## 用户命令由于额外的参数而失败

**Symptoms:**

* 'elasticsearch-users' 命令失败，并显示以下消息："错误：提供了额外的参数 [...] "。

**Resolution:**

当"弹性搜索用户"工具解析输入并发现意外参数时，会发生此错误。当某些参数中使用特殊字符时，可能会发生这种情况。例如，在 Windows 系统上，"，"字符被视为参数分隔符;换句话说，'-r role1，role2'被翻译成'-r role1 role2'，而'elasticsearch-users'工具只识别'role1'作为预期参数。这里的解决方案是引用参数："-r "role1，role2"'。

有关此命令的更多信息，请参阅 'elasticsearch-users' 命令。

[« Authorization exceptions](security-trb-roles.md) [Users are frequently
locked out of Active Directory »](trouble-shoot-active-directory.md)
