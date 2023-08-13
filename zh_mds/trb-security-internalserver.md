

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Common SAML issues](trb-security-saml.md) [Setup-passwords command fails
due to connection failure »](trb-security-setup.md)

## 内部服务器错误 inKibana

**Symptoms:**

* 在 5.1.1 中，出现"未处理的承诺拒绝警告"，Kibana 显示内部服务器错误。

**Resolution:**

如果在 Elasticsearch 中启用了安全插件，但在 Kibana 中禁用了安全插件，则仍必须在"kibana.yml"中设置"elasticsearch.username"和"elasticsearch.password"。否则，Kibana 无法连接到 Elasticsearch。

[« Common SAML issues](trb-security-saml.md) [Setup-passwords command fails
due to connection failure »](trb-security-setup.md)
