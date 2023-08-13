

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Users command fails due to extra arguments](security-trb-extraargs.md)
[Certificate verification fails for curl on Mac »](trb-security-maccurl.md)

## 用户经常被锁定在活动目录之外

**Symptoms:**

* 某些用户经常被锁定在活动目录之外。

**Resolution:**

检查您的领域配置;领域是连续检查的，一个接一个。如果您的 Active Directory 领域先于其他领域进行检查，并且存在同时出现在 Active Directory 和另一个领域中的用户名，则一个领域的有效登录可能会导致另一个领域的登录尝试失败。

例如，如果"UserA"同时存在于 Active Directory 和文件领域，并且首先检查 Active Directory 领域，然后检查文件，则尝试在文件域中以"UserA"身份进行身份验证将首先尝试针对 Active Directory 进行身份验证并失败，然后再成功针对"文件"域进行身份验证。由于在每个请求上都验证了身份验证，因此在"文件"域中的"UserA"的每个请求上都会检查 Active Directory 领域并失败。在这种情况下，当身份验证请求成功完成时，Active Directory 上的帐户将收到几次失败的登录尝试，并且该帐户可能会暂时被锁定。相应地规划你的领域顺序。

另请注意，通常不需要定义多个 ActiveDirectory 领域来处理域控制器故障。使用 MicrosoftDNS 时，域的 DNS 条目应始终指向可用的域控制器。

[« Users command fails due to extra arguments](security-trb-extraargs.md)
[Certificate verification fails for curl on Mac »](trb-security-maccurl.md)
