

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Enabling cipher suites for stronger encryption](ciphers.md) [Security
files »](security-files.md)

## JDK版本支持的SSL/TLS版本

Elasticsearch 依赖于 JDK 的 SSL 和 TLS 实现。

不同的JDK版本支持不同版本的SSL，这可能会影响Elasticsearch的运行方式。

在 JDK 中的缺省 JSSE 提供程序上运行时，此支持适用。配置为使用 FIPS 140-2 安全提供程序的 JVM 可能具有自定义 TLS 实现，该实现可能支持与此列表不同的 TLS 协议版本。

有关 TLS 支持的信息，请查看安全提供程序的发行说明。

`SSLv3`

     SSL v3 is supported on all Elasticsearch [compatible JDKs](install-elasticsearch.html#jvm-version "Java \(JVM\) Version") but is disabled by default. See [Enabling additional SSL/TLS versions on your JDK](jdk-tls-versions.html#jdk-enable-tls-protocol "Enabling additional SSL/TLS versions on your JDK"). 
`TLSv1`

     TLS v1.0 is supported on all Elasticsearch [compatible JDKs](install-elasticsearch.html#jvm-version "Java \(JVM\) Version"). Some newer JDKs, including the JDK bundled with Elasticsearch, disable TLS v1.0 by default. See [Enabling additional SSL/TLS versions on your JDK](jdk-tls-versions.html#jdk-enable-tls-protocol "Enabling additional SSL/TLS versions on your JDK"). 
`TLSv1.1`

     TLS v1.1 is supported on all Elasticsearch [compatible JDKs](install-elasticsearch.html#jvm-version "Java \(JVM\) Version"). Some newer JDKs, including the JDK bundled with Elasticsearch, disable TLS v1.1 by default. See [Enabling additional SSL/TLS versions on your JDK](jdk-tls-versions.html#jdk-enable-tls-protocol "Enabling additional SSL/TLS versions on your JDK"). 
`TLSv1.2`

     TLS v1.2 is supported on all Elasticsearch [compatible JDKs](install-elasticsearch.html#jvm-version "Java \(JVM\) Version"). It is enabled by default on all JDKs that are supported by Elasticsearch, including the bundled JDK. 
`TLSv1.3`

    

TLS v1.3 在 JDK11 及更高版本上受支持，JDK8 构建版本比 8u261 更新(包括 Elasticsearch 支持的每个 JDK8 发行版的最新版本)。TLS v1.3 在与 Elasticsearch 捆绑在一起的 JDK 上默认受支持和启用。

虽然 Elasticsearch 支持在没有 TLS v1.3 的旧版 JDK8 版本上运行，但我们建议升级到包含 TLS v1.3 的 JDK 版本，以获得更好的支持和更新。

### 在 JDK 上启用其他 SSL/TLS 版本

JDK 支持的 SSL/TLS 版本集由作为 JDK 的一部分安装的 javasecurity 属性文件控制。

此配置文件列出了在该 JDK 中禁用的 SSL/TLS 算法。完成以下步骤以从该列表中删除 TLS 版本并在 JDK 中使用它。

1. 找到 JDK 的配置文件。  2. 从该文件复制"jdk.tls.disabledAlgorithms"设置，并将其添加到 Elasticsearch 配置目录中的自定义配置文件中。  3. 在自定义配置文件中，从"jdk.tls.disabledAlgorithms"中删除要使用的 TLS 版本的值。  4. 配置 Elasticsearch 以将自定义系统属性传递给 JDK，以便使用您的自定义配置文件。

#### 找到您的 JDK 的配置文件

对于 Elasticsearch **bundled JDK**，配置文件位于 Elasticsearch 主目录 ('$ES_HOME) 的子目录中：

Linux ： '$ES_HOME/jdk/conf/security/java.security' * Windows： '$ES_HOME/jdk/conf/security/java.security' * macOS：'$ES_HOME/jdk.app/Content/Home/conf/security/java.security'

对于 JDK8**，配置文件位于 Java 安装的 'jre/lib/security' 目录中。如果 '$JAVA_HOME' 指向你用来运行 Elasticsearch 的 JDK 的主目录，那么配置文件将位于：

* '$JAVA_HOME/jre/lib/security/java.security'

对于 JDK11 或更高版本** ，配置文件位于 Java 安装的"conf/security"目录中。如果 '$JAVA_HOME' 指向你用来运行 Elasticsearch 的 JDK 的主目录，那么配置文件将位于：

* '$JAVA_HOME/conf/security/java.security'

#### 复制禁用的算法设置

在 JDK 配置文件中，有一行以 'jdk.tls.disabledAlgorithms=' 开头。此设置控制在 JDK 中_禁用_哪些协议和算法。该设置的值通常跨越多行。

例如，在 OpenJDK 16 中，设置为：

    
    
    jdk.tls.disabledAlgorithms=SSLv3, TLSv1, TLSv1.1, RC4, DES, MD5withRSA, \
        DH keySize < 1024, EC keySize < 224, 3DES_EDE_CBC, anon, NULL

在 Elasticsearch 配置目录中创建一个名为"es.java.security"的新文件。将 'jdk.tls.disabledAlgorithms' 设置从 JDK 的默认配置文件复制到 'es.java.security' 中。您无需复制任何其他设置。

#### 启用所需的 TLS 版本

编辑 Elasticsearch 配置目录中的 'es.java.security' 文件，并修改 'jdk.tls.disabledAlgorithms' 设置，以便不再列出您希望使用的任何 SSL 或 TLS 版本。

例如，要在 OpenJDK 16 上启用 TLSv1.1(它使用前面显示的"jdk.tls.disabledAlgorithms"设置)，"es.java.security"文件将包含以前禁用的 TLS algorithms_except_"TLSv1.1"：

    
    
    jdk.tls.disabledAlgorithms=SSLv3, TLSv1, RC4, DES, MD5withRSA, \
        DH keySize < 1024, EC keySize < 224, 3DES_EDE_CBC, anon, NULL

#### 启用自定义安全配置

要启用自定义安全策略，请在 Elasticsearch 配置目录的 'jvm.options.d' 目录中添加一个文件。

要启用自定义安全策略，请在 Elasticsearch 配置目录的 jvm.options.d 目录中创建一个名为"java.security.options"的文件，其中包含以下内容：

    
    
    -Djava.security.properties=/path/to/your/es.java.security

### 在弹性搜索中启用 TLS 版本

SSL/TLS 版本可以通过"ssl.supported_protocols"设置在 Elasticsearch 中启用和禁用。

Elasticsearch 将仅支持底层 JDK 启用的 TLS 版本。如果将"ssl.supported_procotols"配置为包含 JDK 中未启用的 TLS 版本，则将以静默方式忽略该版本。

同样，在JDK中启用的TLS版本也不会被使用，除非它在Elasticsearch中被配置为"ssl.supported_protocols"之一。

[« Enabling cipher suites for stronger encryption](ciphers.md) [Security
files »](security-files.md)
