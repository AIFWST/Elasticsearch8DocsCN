

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Common Kerberos exceptions](trb-security-kerberos.md) [Internal Server
Error in Kibana »](trb-security-internalserver.md)

## 常见 SAML 问题

下面显示了一些常见的 SAML 问题，并提供了有关如何解决这些问题的提示。

1. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        Cannot find any matching realm for [SamlPrepareAuthenticationRequest{realmName=saml1,
    assertionConsumerServiceURL=https://my.kibana.url/api/security/saml/callback}]

**Resolution:**

为了启动 SAML 身份验证，Kibana 需要从 Elasticsearch 中配置的 SAMLrealm 中知道它应该使用哪个 SAMLrealm。您可以使用'xpack.security.authc.providers.saml。<provider-name>.realm'设置，用于在 Kibana 中显式设置 SAML 领域名称。它必须与在 Elasticsearch 中配置的 SAML 领域的名称匹配。

如果您收到类似上述的错误，则可能意味着'xpack.security.authc.providers.saml的值。<provider-name>Kibana配置中的 .realm' 是错误的。验证它是否与 Elasticsearch 中配置域的名称匹配，即 Elasticsearch 配置中 'xpack.security.authc.realms.saml." 后面的字符串。

2. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        Authentication to realm saml1 failed - Provided SAML response is not valid for realm
    saml/saml1 (Caused by ElasticsearchSecurityException[Conditions
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company....ple.com/]
    do not match required audience
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company.example.com]])

**Resolution:**

我们收到了发往另一个 SAML 服务提供商的 SAML 响应。这通常意味着在"elasticsearch.yml"("sp.entity_id")中配置的 SAML 服务提供商实体 ID 与 SAML IdentityProvider 文档中配置为 SAML 服务提供商实体 ID 的内容不匹配。

要解决此问题，请确保 Elasticsearch 中的 saml 领域和 IdP 都为服务提供商的 SAML 实体 ID 配置了相同的字符串。

在 Elasticsearch 日志中，就在异常消息(上面)之前，还会有一个或多个表单的"INFO"级消息

    
        Audience restriction
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company.example.com/]
    does not match required audience
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company.example.com]
    (difference starts at character [#68] [/] vs [])

此日志消息有助于确定从 IdP 接收的值与在 Elasticsearch 中配置的值之间的差异。仅当两个字符串被视为相似时，系统才会显示括号中描述两个受众标识符之间差异的文本。

这些字符串作为区分大小写的字符串进行比较，而不是作为规范化的 URL，即使这些值类似于 URL。请注意尾部斜杠、端口号等。

3. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        Cannot find metadata for entity [your:entity.id] in [metadata.xml]

**Resolution:**

我们无法在配置的元数据文件中找到 SAML 实体 ID "your：entity.id"的元数据("元数据.xml")。

    1. Ensure that the `metadata.xml` file you are using is indeed the one provided by your SAML Identity Provider. 
    2. Ensure that the `metadata.xml` file contains one <EntityDescriptor> element as follows: `<EntityDescriptor ID="0597c9aa-e69b-46e7-a1c6-636c7b8a8070" entityID="https://saml.example.com/f174199a-a96e-4201-88f1-0d57a610c522/" ...` where the value of the `entityID` attribute is the same as the value of the `idp.entity_id` that you have set in your SAML realm configuration in `elasticsearch.yml`. 
    3. Note that these are also compared as case-sensitive strings and not as canonicalized URLs even when the values are URL-like. 

4. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        unable to authenticate user [<unauthenticated-saml-user>]
    for action [cluster:admin/xpack/security/saml/authenticate]

**Resolution:**

此错误表示 Elasticsearch 无法处理传入的 SAML身份验证消息。由于无法处理消息，Elasticsearch 不知道要进行身份验证的用户是谁<unauthenticated-saml-user>，而是使用""占位符。要诊断 _actual_ 问题，您必须检查 Elasticsearch 日志以获取更多详细信息。

5. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        Authentication to realm <saml-realm-name> failed - SAML Attribute [<AttributeName0>] for
    [xpack.security.authc.realms.saml.<saml-realm-name>.attributes.principal] not found in saml attributes
    [<AttributeName1>=<AttributeValue1>, <AttributeName2>=<AttributeValue2>, ...] or NameID [ NameID(format)=value ]

**Resolution:**

此错误表示 Elasticsearch 未能在身份提供程序发送的 SAML 响应中找到必要的 SAML属性。在这个例子中，Elasticsearch的配置如下：

    
        xpack.security.authc.realms.saml.<saml-realm-name>.attributes.principal: AttributeName0

此配置意味着 Elasticsearch 希望在 SAML 响应中找到名称为"AttributeName0"的 SAML 属性或具有适当格式的 "NameID"，以便将其映射到"主体"用户属性。"主体"用户属性是必需的，因此如果无法进行此映射，身份验证将失败。

如果您尝试映射"NameID"，请确保预期的"NameID"格式与发送的格式匹配。有关更多详细信息，请参阅特殊属性名称。

如果您尝试映射 SAML 属性，并且该属性不是错误消息中列表的一部分，则可能意味着您拼错了属性名称，或者 IdP 未发送此特定属性。您可以使用列表中的其他属性映射到"主体"，或咨询 IdP 管理员以确定是否可以发送所需的属性。

6. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        Cannot find [{urn:oasis:names:tc:SAML:2.0:metadata}IDPSSODescriptor]/[urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect] in descriptor

**Resolution:**

此错误表示身份提供程序的 SAML 元数据不包含<SingleSignOnService>绑定为 HTTP-Redirect(urn：oasis：names：tc：SAML：2.0：bindings：HTTP-Redirect)的""端点。Elasticsearch 仅支持 SAML 身份验证请求的"HTTP-重定向"绑定(并且不支持"HTTP-POST"绑定)。请咨询您的 IdP 管理员，以启用至少一个<SingleSignOnService>支持"HTTP-重定向"绑定的""并更新您的 IdP SAML 元数据。

7. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        Authentication to realm my-saml-realm failed -
    Provided SAML response is not valid for realm saml/my-saml-realm
    (Caused by ElasticsearchSecurityException[SAML Response is not a 'success' response:
     The SAML IdP did not grant the request. It indicated that the Elastic Stack side sent
     something invalid (urn:oasis:names:tc:SAML:2.0:status:Requester). Specific status code which might
     indicate what the issue is: [urn:oasis:names:tc:SAML:2.0:status:InvalidNameIDPolicy]]
    )

**Resolution:**

这意味着 SAML 身份提供程序无法对用户进行身份验证，并向服务提供商(弹性堆栈)发送了 SAML 响应，指示此失败。该消息将传达 SAML 身份提供程序是否认为问题出在服务提供商(弹性堆栈)或身份提供程序本身，并且下面的特定状态代码非常有用，因为它通常指示潜在问题。特定错误代码的列表在 SAML 2.0 核心规范 - 第 3.2.2.2 节中定义，最常见的错误代码是：

    1. `urn:oasis:names:tc:SAML:2.0:status:AuthnFailed`: The SAML Identity Provider failed to authenticate the user. There is not much to troubleshoot on the Elastic Stack side for this status, the logs of the SAML Identity Provider will hopefully offer much more information. 
    2. `urn:oasis:names:tc:SAML:2.0:status:InvalidNameIDPolicy`: The SAML Identity Provider cannot support releasing a NameID with the requested format. When creating SAML Authentication Requests, Elasticsearch sets the NameIDPolicy element of the Authentication request with the appropriate value. This is controlled by the [`nameid_format`](security-settings.html#ref-saml-settings "SAML realm settings") configuration parameter in `elasticsearch.yml`, which if not set defaults to `urn:oasis:names:tc:SAML:2.0:nameid-format:transient`. This instructs the Identity Provider to return a NameID with that specific format in the SAML Response. If the SAML Identity Provider cannot grant that request, for example because it is configured to release a NameID format with `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent` format instead, it returns this error indicating an invalid NameID policy. This issue can be resolved by adjusting `nameid_format` to match the format the SAML Identity Provider can return or by setting it to `urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified` so that the Identity Provider is allowed to return any format it wants. 

8. **症状：**

Kibana 中的身份验证失败，并在 Elasticsearch 日志中打印以下错误：

    
        The XML Signature of this SAML message cannot be validated. Please verify that the saml
    realm uses the correct SAMLmetadata file/URL for this Identity Provider

**Resolution:**

这意味着 Elasticsearch 无法验证身份提供程序发送的 SAML 消息的数字签名。Elasticsearch 使用 SAML 元数据中包含的身份提供程序的公钥，以验证 IdP 使用其对应的私钥创建的签名。如果不这样做，可能有多种原因：

    1. As the error message indicates, the most common cause is that the wrong metadata file is used and as such the public key it contains doesn't correspond to the private key the Identity Provider uses. 
    2. The configuration of the Identity Provider has changed or the key has been rotated and the metadata file that Elasticsearch is using has not been updated. 
    3. The SAML Response has been altered in transit and the signature cannot be validated even though the correct key is used. 

如上所述，SAML 中用于数字签名的私钥和公钥以及自签名 X.509 证书与传输层或 http 层上用于 TLS 的密钥和证书无关。上述故障与您的"xpack.ssl"相关配置无关。

9. **症状：**

用户无法使用 Kibana 中的本地用户名和密码登录，因为启用了 SAML。

**Resolution:**

如果您希望用户除了使用 SAML 领域进行单点登录之外，还能够使用本地凭据对 ToKibana 进行身份验证，则必须在 Kibana 中启用"基本""身份验证提供程序"。该过程记录在 SAMLGuide 中

10. **症状：**

没有 SAML 请求 ID 值从 Kibana 传递到 Elasticsearch：

    
        Caused by org.elasticsearch.ElasticsearchSecurityException: SAML content is in-response-to [_A1B2C3D4E5F6G8H9I0] but expected one of []

**解决方法：** 此错误表示 Elasticsearch 收到了与特定 SAML 请求绑定的 SAML响应，但 Kibana 没有明确指定该请求的 ID。这通常意味着 Kibana 找不到之前存储 SAML 请求 ID 的用户会话。

要解决此问题，请确保在 Kibana 配置中，"xpack.security.sameSiteCookies"未设置为"严格"。根据您的配置，您可以依赖默认值或将值显式设置为"无"。

欲了解更多信息，请阅读MDN SameSitecookie

如果您在负载均衡器后面提供多个 Kibana 安装，请确保对所有安装使用相同的安全配置。

**Logging:**

如果上述解决方案无法解决您的问题，请为 SAML 领域启用其他日志记录以进一步进行故障排除。可以通过配置以下持久设置来启用调试日志记录：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.xpack.security.authc.saml": 'debug'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.xpack.security.authc.saml": "debug"
      }
    }

或者，您可以将以下行添加到"ES_PATH_CONF"配置文件的末尾：

    
    
    logger.saml.name = org.elasticsearch.xpack.security.authc.saml
    logger.saml.level = DEBUG

有关详细信息，请参阅配置日志记录级别。

[« Common Kerberos exceptions](trb-security-kerberos.md) [Internal Server
Error in Kibana »](trb-security-internalserver.md)
