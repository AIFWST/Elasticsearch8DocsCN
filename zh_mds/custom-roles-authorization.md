

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Configuring authorization delegation](configuring-authorization-
delegation.md) [Enable audit logging »](enable-audit-logging.md)

## 自定义角色和授权

如果您需要从开箱即用不支持的系统中检索用户角色，或者如果 Elasticsearch 安全功能提供的授权系统不能满足您的需求，则可以实施 SPI 加载的安全扩展来自定义角色检索和/或授权系统。SPI加载的安全扩展是普通elasticsearch插件的一部分。

### 实现自定义角色提供程序

创建自定义角色提供程序：

1. 实现接口 'BiConsumer<Set<String>， ActionListener<Set<RoleDescriptor>>>'。也就是说，实现由一个方法组成，该方法采用一组字符串(这是要解析的角色名称)和一个 ActionListener，在该方法上传递一组解析的角色描述符作为响应。  2. 自定义角色提供程序实现必须特别注意不要阻止任何 I/O 操作。实现负责确保异步行为和非阻塞调用，由于提供了"ActionListener"，当角色已解析且响应准备就绪时，可以在其上发送响应，这一事实使这变得更加容易。

要将自定义角色提供程序打包为插件，请执行以下操作：

1. 为您的角色提供程序实现一个扩展类，该扩展类实现"org.elasticsearch.xpack.core.security.SecurityExtension"。在那里，您需要覆盖以下一个或多个方法：@Override public List<BiConsumer<Set<String>、ActionListener<Set<RoleDescriptor>>>>getRolesProviders(Settings settings， ResourceWatcherService resourceWatcherService) { ... }

"getRolesProviders"方法用于提供自定义角色提供程序的列表，如果保留角色或本机角色存储无法解析角色名称，则这些提供程序将用于解析角色名称。应按照调用自定义角色提供程序以解析角色的顺序返回列表。例如，如果"getRolesProviders"返回角色提供程序的两个实例，并且它们都能够解析角色"A"，则用于角色"A"的已解析角色描述符将由列表中的第一个角色提供程序解析。

### 实现授权引擎

要创建授权引擎，您需要：

1. 在具有所需授权行为的类中实现"org.elasticsearch.xpack.core.security.authz.AuthorizationEngine"接口。  2. 在包含授权请求所需信息的类中实现"org.elasticsearch.xpack.core.security.authz.Authorization.AuthorizationInfo"接口。

要将授权引擎打包为插件，请执行以下操作：

1. 为您的授权引擎实现一个扩展类，用于扩展"org.elasticsearch.xpack.core.security.SecurityExtension"。在那里，您需要覆盖以下方法：@Override公共授权引擎获取授权引擎(设置设置){ ... }

"getAuthorizationEngine"方法用于提供授权引擎实现。

GitHub 上的弹性搜索存储库中提供了说明自定义授权引擎的结构和实现的示例代码。您可以使用此代码作为创建自己的授权引擎的起点。

### 实现一个弹性搜索插件

为了为您的自定义角色提供程序或授权引擎注册安全扩展，您还需要实现一个包含扩展的 elasticsearch 插件：

1. 实现一个扩展 'org.elasticsearch.plugins.Plugin' 的插件类 2.为插件创建构建配置文件;Gradle是我们推荐的。  3. 创建一个"plugin-descriptor.properties"文件，如插件作者帮助中所述。  4. 为扩展创建一个"META-INF/services/org.elasticsearch.xpack.core.security.SecurityExtension"描述符文件，该文件包含"org.elasticsearch.xpack.core.security.SecurityExtension"实现的完全限定类名 5.将所有内容捆绑在一个 zip 文件中。

### 使用安全扩展插件

若要使用安全扩展插件，请执行以下操作：

1. 在集群中的每个节点上安装带有扩展的插件。您可以使用"install"子命令运行"bin/elasticsearch-plugin"，并指定指向包含扩展名的zip文件的URL。例如：bin/elasticsearch-plugin install file:///<path>/my-extension-plugin-1.0.zip

2. 将扩展中实现的任何配置参数添加到"elasticsearch.yml"文件中。这些设置没有命名空间，您可以在构造扩展时访问任何设置，尽管建议对扩展使用命名空间约定，以使"elasticsearch.yml"配置易于理解。

例如，如果您有一个自定义角色提供程序，用于解析通过读取 AWS 上的 S3 存储桶中的 blob 来解析角色，则可以在"elasticsearch.yml"中指定设置，例如：

    
        custom_roles_provider.s3_roles_provider.bucket: roles
    custom_roles_provider.s3_roles_provider.region: us-east-1
    custom_roles_provider.s3_roles_provider.secret_key: xxx
    custom_roles_provider.s3_roles_provider.access_key: xxx

这些设置作为参数传递给"SecurityExtension"接口中的方法。

3. 重新启动弹性搜索。

[« Configuring authorization delegation](configuring-authorization-
delegation.md) [Enable audit logging »](enable-audit-logging.md)
