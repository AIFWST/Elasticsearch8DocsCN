

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« FIPS 140-2](fips-140-compliance.md) [Update certificates with the same CA
»](update-node-certs-same.md)

## 更新节点安全证书

如果当前节点证书即将过期，或者安全漏洞破坏了证书链的信任，则可能需要更新 TLS 证书。使用 SSL证书 API 检查证书何时到期。

如果您有权访问用于签署现有节点证书的原始证书颁发机构 (CA) 密钥和证书(并且您仍然可以信任您的 CA)，则可以使用该 CA 对新证书进行签名。

如果您必须信任组织中的新 CA，或者需要自己生成新 CA，则需要使用此新 CA 对新节点证书进行签名，并指示节点信任新 CA。在这种情况下，您将使用新 CA 签署节点证书，并指示节点信任此证书链。

根据即将过期的证书，您可能需要更新传输层和/或 HTTP 层的证书。

无论情况如何，默认情况下，Elasticsearch 都会以五秒的间隔监控 SSL 资源的更新。您只需将新证书和密钥文件(或密钥库)复制到 Elasticsearch 配置目录中，您的节点就会检测到更改并重新加载密钥和证书。

由于 Elasticsearch 不会重新加载 'elasticsearch.yml' 配置，因此如果要利用自动证书和密钥重新加载，则必须使用相同的文件名。

如果您需要更新"elasticsearch.yml"配置或更改存储在安全设置中的密钥或密钥库的密码，则必须完成滚动重新启动。Elasticsearch 不会自动重新加载存储在安全设置中的密码更改。

**首选滚动重启**

虽然可以对安全证书执行就地更新，但在群集上使用滚动重启更安全。就地更新可避免滚动重启的一些复杂情况，但会产生以下风险：

* 如果使用 PEM 文件，则证书和密钥位于单独的文件中。您必须_同时_更新这两个文件，否则节点可能会遇到无法建立新连接的临时时期。  * 更新证书和密钥不会自动强制刷新现有连接。这意味着，即使您犯了错误，节点也可能看起来像在运行，但只是因为它仍然具有现有连接。节点可能无法与其他节点连接，使其无法从网络中断或节点重启中恢复。

[« FIPS 140-2](fips-140-compliance.md) [Update certificates with the same CA
»](update-node-certs-same.md)
