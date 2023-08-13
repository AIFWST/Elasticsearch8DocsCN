

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« JWT authentication](jwt-auth-realm.md) [Enabling anonymous access
»](anonymous-access.md)

## 与其他身份验证系统集成

如果您使用的身份验证系统不受 Elasticsearch 安全功能的现成支持，则可以创建一个自定义领域来与之交互以验证用户。您可以将自定义领域实现为 SPIloaded 安全扩展，作为普通 elasticsearch 插件的一部分。

### 实现自定义领域

<https://github.com/elastic/elasticsearch/tree/8.9/x-pack/qa/security-example-spi-extension> 中提供了说明自定义域的结构和实现的示例代码。您可以使用此代码作为创建自己的领域的起点。

要创建自定义领域，您需要：

1. 扩展"org.elasticsearch.xpack.security.authc.Realm"以与您的身份验证系统通信以验证用户。  2. 在将用于创建自定义领域的类中实现"org.elasticsearch.xpack.security.authc.Realm.Factory"接口。  3. 扩展"org.elasticsearch.xpack.security.authc.DefaultAuthenticationFailureHandler"以处理使用自定义域时的身份验证失败。

要将自定义领域打包为插件，请执行以下操作：

1. 为您的领域实现一个扩展类，用于扩展"org.elasticsearch.xpack.core.security.SecurityExtension"。在那里，您需要覆盖以下一个或多个方法：@Override public Map<String， Factory> getRealms() { ... }

"getRealms"方法用于提供类型名称到将用于创建领域的"工厂"的映射。

    
        @Override
    public AuthenticationFailureHandler getAuthenticationFailureHandler() {
        ...
    }

"getAuthenticationFailureHandler"方法用于选择性地提供自定义的"AuthenticationFailureHandler"，它将控制Elasticsearch安全功能在某些身份验证失败事件中的响应方式。

    
        @Override
    public List<String> getSettingsFilter() {
        ...
    }

"Plugin#getSettingsFilter"方法返回应从设置 API 中筛选的设置名称列表，因为它们可能包含敏感凭据。请注意，此方法不是"SecurityExtension"接口的一部分，它是elasticsearch插件主类的一部分。

2. 为插件创建一个构建配置文件;Gradle是我们推荐的。  3. 为扩展创建一个"META-INF/services/org.elasticsearch.xpack.core.security.SecurityExtension"描述符文件，该文件包含"org.elasticsearch.xpack.core.security.SecurityExtension"实现的完全限定类名 4.将所有内容捆绑在一个 zip 文件中。

### 使用自定义领域对用户进行身份验证

要使用自定义领域：

1. 在群集中的每个节点上安装领域扩展。您可以使用"install"子命令运行"bin/elasticsearch-plugin"，并指定指向包含扩展名的zip文件的URL。例如：bin/elasticsearch-plugin install file:///<path>/my-realm-1.0.zip

2. 将适当领域类型的领域配置添加到 'xpack.security.authc.realms' 命名空间下的 'elasticsearch.yml' 中。您必须在与扩展定义的类型匹配的命名空间中定义领域。您可以设置的选项取决于自定义领域公开的设置。至少，您必须显式设置 'order' 属性来控制在身份验证期间查询领域的顺序。您还必须确保每个已配置的领域都有不同的"顺序"设置。如果两个或多个领域具有相同的"顺序"，节点将无法启动。

在 'elasticsearch.yml' 中配置领域时，只有您指定的领域用于身份验证。如果还想使用"本机"或"文件"域，则必须将它们包含在域链中。

3. 重新启动弹性搜索。

[« JWT authentication](jwt-auth-realm.md) [Enabling anonymous access
»](anonymous-access.md)
