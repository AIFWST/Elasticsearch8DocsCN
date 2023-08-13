

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Security files](security-files.md) [Updating node security certificates
»](update-node-certs.md)

## FIPS140-2

联邦信息处理标准 (FIPS) 出版物 140-2 (FIPSPUB 140-2) 标题为"加密模块的安全要求"，是用于批准加密模块的美国政府计算机安全标准。Elasticsearch 提供符合 FIPS 140-2 的模式，因此可以在配置的 FIPS140-2 JVM 中运行。

与 Elasticsearch 捆绑在一起的 JVM 未针对 FIPS 140-2 进行配置。必须使用经过 FIPS 140-2 认证的 Java 安全提供程序配置外部 JDK。有关受支持的 JVM 配置，请参阅 Elasticsearch JVM 支持列表。

为 FIPS 140-2 配置 JVM 后，您可以在 FIPS140-2 模式下运行 Elasticsearch，方法是在 'elasticsearch.yml' 中将 'xpack.security.fips_mode.enabled' 设置为 'true'。

对于 Elasticsearch，符合 FIPS 140-2 的依据是：

* 使用 FIPS 批准/NIST 推荐的加密算法。  将这些加密算法的实现委托给NIST验证的加密模块(可通过JVM中使用的Java安全提供程序获得)。  * 允许以符合 FIPS 140-2 的方式配置 Elasticsearch，如下所述。

### 升级注意事项

Elasticsearch 8.9.0 需要 Java 17 或更高版本。目前还没有一个 FIPS 认证的 Java 17 安全模块，您可以在 FIPS 140-2 模式下运行 Elasticsearch 8.9.0 时使用。如果您在 FIPS 140-2 模式下运行，则需要向安全组织请求例外以升级到 Elasticsearch 8.9.0，或者继续使用 Elasticsearch 7.x，直到 Java 17 通过认证。或者，考虑在FedRAMP认证的GovCloud区域中使用Elasticsearch Service。

如果您计划将现有集群升级到可在 aFIPS 140-2 配置的 JVM 中运行的版本，我们建议您首先在现有 JVM 中执行滚动升级到新版本，并执行所有必要的配置更改，以准备在 FIPS 140-2 模式下运行。然后，您可以执行节点的滚动重新启动，在 FIPS 140-2 JVM 中启动每个节点。在重新启动期间，Elasticsearch：

* 将安全设置升级到最新的兼容格式。FIPS 140-2 JVM 无法加载以前的格式版本。如果密钥库不受密码保护，那么必须手动设置密码。请参阅 Elasticsearch 密钥库。  * 将自行生成的试用许可证升级到最新的 FIPS 140-2 兼容格式。

如果您的预订已支持 FIPS 140-2 模式，则可以选择执行滚动升级，同时在 FIPS 140-2 JVM 中运行每个升级的节点。在这种情况下，您还需要手动重新生成"elasticsearch.keystore"，并将所有安全设置迁移到其中，以及下面概述的必要配置更改，然后再启动每个节点。

### 为 FIPS140-2 配置 Elasticsearch

除了设置"xpack.security.fips_mode.enabled"之外，还需要相应地配置许多与安全相关的设置，以便合规并能够在配置FIPS 140-2的JVM中成功运行Elasticsearch。

#### ElasticsearchKeystore

FIPS 140-2(通过 NIST 特别出版物 800-132)规定加密密钥应至少具有 112 位的有效强度。因此，存储节点安全设置的 Elasticsearch 密钥库需要使用满足此要求的密码进行密码保护。这意味着密码长度需要为 14 个字节，相当于 14 个字符的 ASCII 编码密码或 7 个字符的 UTF-8 编码密码。您可以使用 theelasticsearch-keystore passwd 子命令来更改或设置现有密钥库的密码。请注意，当密钥库受密码保护时，每次 Elasticsearch 启动时都必须提供密码。

####TLS

FIPS 140-2 不允许使用 SSLv2 和 SSLv3，因此"SSLv2Hello"和"SSLv3"不能用于"ssl.supported_protocols"。

TLS 密码的使用主要由相关的加密模块(JVM 使用的 FIPS 批准的安全提供程序)控制。默认情况下在 Elasticsearch 中配置的所有密码都符合 FIPS 140-2，因此可以在 FIPS 140-2 JVM 中使用。参见"ssl.cipher_suites"。

#### TLS 密钥库和密钥

密钥库可用于许多常规 TLS 设置，以便方便地存储密钥和信任材料。"JKS"和"PKCS#12"密钥库都不能在 FIPS 140-2 配置的 JVM 中使用。避免使用这些类型的密钥库。您的 FIPS 140-2 提供程序可以提供可以使用的合规密钥库实现，或者您可以使用 PEM 编码文件。要使用 PEM 编码的密钥材料，您可以使用相关的"\*.key"和"*.certificate"配置选项，对于信任材料，您可以使用"*.certificate_authorities"。

FIPS 140-2 合规性要求用于 TLS 的公钥长度必须与 TLS 中使用的对称密钥算法的强度相对应。根据您选择使用的"ssl.cipher_suites"值，TLS 密钥必须具有相应的长度，如下表所示：

**表 80.可比的关键优势**

对称密钥算法

|

RSA 密钥长度

|

ECC 密钥长度 ---|---|--- '3DES'

|

2048

|

224-255 "AES-128"

|

3072

|

256-383 "AES-256"

|

15630

|

512+ #### 存储的密码哈希编辑

虽然 Elasticsearch 提供了许多用于在磁盘上安全散列凭据的算法，但只有基于"PBKDF2"的算法系列符合 FIPS 140-2 的存储密码散列。但是，由于"PBKDF2"本质上是一个密钥派生函数，因此您的 JVM 安全提供程序可能会强制执行 112 位密钥强度要求。尽管 FIPS 140-2 不强制要求用户密码标准，但此要求可能会影响 Elasticsearch 中的密码哈希。为了遵守此要求，同时允许您使用满足安全策略的密码，Elasticsearch offerspbkdf2_stretch这是在 FIPS 140-2 环境中运行 Elasticsearch 时建议的哈希算法。"pbkdf2_stretch"在将用户密码传递给"PBKDF2"实现之前，对用户密码执行一轮SHA-512。

如果您具有外部策略和工具，可以确保保留、本机和文件域的所有用户密码超过 14 字节，则仍然可以使用普通的"pbkdf2"选项之一而不是"pbkdf2_stretch"。

您必须将"xpack.security.authc.password_hashing.algorithm"设置设置为可用的"pbkdf_stretch_*"值之一。启用 FIPS-140 模式后，"xpack.security.authc.password_hashing.算法"的默认值为"pbkdf2_stretch"。请参阅用户缓存和密码哈希算法。

密码散列配置更改不具有追溯性，因此保留、本机和文件域的现有用户的存储散列凭据不会在磁盘上更新。为确保符合 FIPS 140-2，请使用适用于文件领域的 elasticsearch-user CLI 工具以及适用于本机和保留领域的创建用户和更改密码 API 重新创建用户或更改其密码。其他类型的领域不受影响，不需要任何更改。

#### 缓存密码哈希

建议将"SSHA256"(加盐的"SHA256")用于缓存哈希。尽管"PBKDF2"符合FIPS-140-2，但它在设计上很慢，因此通常不适合作为缓存哈希算法。缓存的凭据永远不会存储在磁盘上，加盐的"sha256"为内存凭据哈希提供了足够安全级别，而不会造成令人望而却步的性能开销。您可以_使用"PBKDF2"，但是您应该首先仔细评估性能影响。根据您的部署，"PBKDF2"的开销可能会抵消使用缓存的大部分性能提升。

将所有"cache.hash_algo"设置设置为"ssha256"或保留未定义，因为"ssha256"是所有"cache.hash_algo"设置的默认值。请参阅用户缓存和密码哈希算法。

用户缓存将在节点重新启动时清空，因此任何使用不兼容算法的现有哈希都将被丢弃，并使用您选择的算法创建新哈希。

###Limitations

由于 FIPS 140-2 合规性强制实施的限制，在 FIPS 140-2 模式下运行时，少数功能不可用。列表如下：

* Azure Classic Discovery Plugin * 'elasticsearch-certutil' 工具。但是，"elasticsearch-certutil"可以很好地用于非 FIPS 140-2 配置的 JVM(将"ES_JAVA_HOME"环境变量指向不同的 Java 安装)，以便生成以后可以在 FIPS 140-2 配置的 JVM 中使用的密钥和证书。  * SQL CLI 客户机无法使用 FIPS 140-2 配置的 JVM 运行，同时使用 TLS 进行传输安全或 PKI 进行客户机认证。

[« Security files](security-files.md) [Updating node security certificates
»](update-node-certs.md)
