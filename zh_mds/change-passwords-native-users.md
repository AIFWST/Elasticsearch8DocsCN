

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Set up basic security for the Elastic Stack plus secured HTTPS
traffic](security-basic-setup-https.md) [Enabling cipher suites for stronger
encryption »](ciphers.md)

## 为本机用户和内置用户设置密码

实现安全性后，您可能需要或想要更改不同用户的密码。您可以使用"弹性搜索-重置密码"工具或更改密码 API 来更改本机用户和内置用户的密码，例如"弹性"或"kibana_system"用户。

例如，以下命令将用户名为"user1"的用户的密码更改为自动生成的值，并将新密码打印到终端：

    
    
    bin/elasticsearch-reset-password -u user1

要为用户显式设置密码，请在预期密码中包含"-i"参数。

    
    
    bin/elasticsearch-reset-password -u user1 -i <password>

如果您在 Kibana 中工作或没有命令行访问权限，则可以使用更改密码 API 来更改用户的密码：

    
    
    POST /_security/user/user1/_password
    {
      "password" : "new-test-password"
    }

[« Set up basic security for the Elastic Stack plus secured HTTPS
traffic](security-basic-setup-https.md) [Enabling cipher suites for stronger
encryption »](ciphers.md)
