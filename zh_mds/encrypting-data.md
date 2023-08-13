

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« How Watcher works](how-watcher-works.md) [Watcher inputs »](input.md)

## 在观察程序中加密敏感数据

监视可能有权访问敏感数据，例如 HTTP 基本身份验证信息或有关 SMTP 电子邮件服务的详细信息。您可以通过生成密钥并在群集中的每个节点上添加一些安全设置来加密此数据。

手表中 HTTP 基本身份验证块中使用的每个"密码"字段(例如在 Webhook、HTTP 输入或使用报告电子邮件附件时)都不会再存储为纯文本。另请注意，无法在 awatch 中将您自己的字段配置为加密。

若要加密观察程序中的敏感数据，请执行以下操作：

1. 使用 elasticsearch-syskeygen 命令创建系统密钥文件。  2. 将"system_key"文件复制到群集中的所有节点。

系统密钥是对称密钥，因此必须在群集中的每个节点上使用相同的密钥。

3. 设置"xpack.watcher.encrypt_sensitive_data"设置：xpack.watcher.encrypt_sensitive_data：真

4. 在集群中每个节点的 Elasticsearch 密钥库中设置"xpack.watcher.encryption_key"设置。

例如，运行以下命令以在每个节点上导入"system_key"文件：

    
        bin/elasticsearch-keystore add-file xpack.watcher.encryption_key <filepath>/system_key

5. 删除群集中每个节点上的"system_key"文件。

现有手表不受这些更改的影响。只有执行这些步骤后创建的监视才会启用加密。

[« How Watcher works](how-watcher-works.md) [Watcher inputs »](input.md)
