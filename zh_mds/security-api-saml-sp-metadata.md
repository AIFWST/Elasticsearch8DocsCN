

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« SAML complete logout API](security-api-saml-complete-logout.md) [SSL
certificate API »](security-api-ssl.md)

## SAML 服务提供程序元数据API

为 SAML 2.0 服务提供商生成 SAML 元数据。

###Request

'GET /_security/saml/metadata/<realm_name>'

###Description

SAML 2.0 规范为服务提供商提供了一种使用元数据文件描述其功能和配置的机制。此 API 根据 Elasticsearch 中 SAMLrealm 的配置生成服务提供程序元数据。

### 路径参数

`<realm_name>`

     (Required, string) The name of the SAML realm in Elasticsearch. 

### 响应正文

`metadata`

     (string) An XML string that contains a SAML Service Provider's metadata for the realm. 

###Examples

以下示例为 SAML 领域"saml1"生成服务提供程序元数据：

    
    
    GET /_security/saml/metadata/saml1

API 以 XML 字符串形式返回以下包含 SAML 元数据的响应：

    
    
    {
        "metadata" : "<?xml version=\"1.0\" encoding=\"UTF-8\"?><md:EntityDescriptor xmlns:md=\"urn:oasis:names:tc:SAML:2.0:metadata\" entityID=\"https://kibana.org\"><md:SPSSODescriptor AuthnRequestsSigned=\"false\" WantAssertionsSigned=\"true\" protocolSupportEnumeration=\"urn:oasis:names:tc:SAML:2.0:protocol\"><md:SingleLogoutService Binding=\"urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect\" Location=\"https://kibana.org/logout\"/><md:AssertionConsumerService Binding=\"urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST\" Location=\"https://kibana.org/api/security/saml/callback\" index=\"1\" isDefault=\"true\"/></md:SPSSODescriptor></md:EntityDescriptor>"
    }

[« SAML complete logout API](security-api-saml-complete-logout.md) [SSL
certificate API »](security-api-ssl.md)
