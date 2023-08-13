

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-reset-password](reset-password.md) [elasticsearch-service-
tokens »](service-tokens-command.md)

## elasticsearch-saml-metadata

'elasticsearch-saml-metadata' 命令可用于生成 SAML 2.0 服务提供商元数据文件。

###Synopsis

    
    
    bin/elasticsearch-saml-metadata
    [--realm <name>]
    [--out <file_path>] [--batch]
    [--attribute <name>] [--service-name <name>]
    [--locale <name>] [--contacts]
    ([--organisation-name <name>] [--organisation-display-name <name>] [--organisation-url <url>])
    ([--signing-bundle <file_path>] | [--signing-cert <file_path>][--signing-key <file_path>])
    [--signing-key-password <password>]
    [-E <KeyValuePair>]
    [-h, --help] ([-s, --silent] | [-v, --verbose])

###Description

SAML 2.0 规范为服务提供商提供了一种机制，可以使用_metadata file_来描述其功能和配置。

'elasticsearch-saml-metadata' 命令会根据 Elasticsearch 中 SAML 领域的配置生成这样的文件。

某些 SAML 身份提供程序允许您在将弹性堆栈配置为服务提供商时自动导入元数据文件。

您可以选择对元数据文件进行数字签名，以便在与身份提供程序共享元数据文件之前确保其完整性和真实性。用于对元数据文件进行签名的密钥不一定与 SAMLmessage 签名的 saml 领域配置中已使用的密钥相同。

如果您的 Elasticsearch 密钥库受密码保护，那么当您运行 'elasticsearch-saml-metadata' 命令时，系统会提示您输入密码。

###Parameters

'--属性 <name>'

     Specifies a SAML attribute that should be included as a `<RequestedAttribute>` element in the metadata. Any attribute configured in the Elasticsearch realm is automatically included and does not need to be specified as a commandline option. 
`--batch`

     Do not prompt for user input. 
`--contacts`

     Specifies that the metadata should include one or more `<ContactPerson>` elements. The user will be prompted to enter the details for each person. 
`-E <KeyValuePair>`

     Configures an Elasticsearch setting. 
`-h, --help`

     Returns all of the command parameters. 
`--locale <name>`

     Specifies the locale to use for metadata elements such as `<ServiceName>`. Defaults to the JVM's default system locale. 
`--organisation-display-name <name`

     Specified the value of the `<OrganizationDisplayName>` element. Only valid if `--organisation-name` is also specified. 
`--organisation-name <name>`

     Specifies that an `<Organization>` element should be included in the metadata and provides the value for the `<OrganizationName>`. If this is specified, then `--organisation-url` must also be specified. 
`--organisation-url <url>`

     Specifies the value of the `<OrganizationURL>` element. This is required if `--organisation-name` is specified. 
`--out <file_path>`

     Specifies a path for the output files. Defaults to `saml-elasticsearch-metadata.xml`
`--service-name <name>`

     Specifies the value for the `<ServiceName>` element in the metadata. Defaults to `elasticsearch`. 
`--signing-bundle <file_path>`

     Specifies the path to an existing key pair (in PKCS#12 format). The private key of that key pair will be used to sign the metadata file. 
`--signing-cert <file_path>`

     Specifies the path to an existing certificate (in PEM format) to be used for signing of the metadata file. You must also specify the `--signing-key` parameter. This parameter cannot be used with the `--signing-bundle` parameter. 
`--signing-key <file_path>`

     Specifies the path to an existing key (in PEM format) to be used for signing of the metadata file. You must also specify the `--signing-cert` parameter. This parameter cannot be used with the `--signing-bundle` parameter. 
`--signing-key-password <password>`

     Specifies the password for the signing key. It can be used with either the `--signing-key` or the `--signing-bundle` parameters. 
`--realm <name>`

     Specifies the name of the realm for which the metadata should be generated. This parameter is required if there is more than 1 `saml` realm in your Elasticsearch configuration. 
`-s, --silent`

     Shows minimal output. 
`-v, --verbose`

     Shows verbose output. 

###Examples

以下命令为"saml1"领域生成默认元数据文件：

    
    
    bin/elasticsearch-saml-metadata --realm saml1

该文件将被写入"saml-elasticsearch-metadata.xml"。系统可能会提示您为领域使用的任何属性提供"友好名称"值。

以下命令为"saml2"领域生成一个元数据文件，其中 <ServiceName>'' 为 'kibana-finance'，区域设置为 'en-GB' 并包含 '' 元素<ContactPerson>和一个 '<Organization>' 元素：

    
    
    bin/elasticsearch-saml-metadata --realm saml2 \
        --service-name kibana-finance \
        --locale en-GB \
        --contacts \
        --organisation-name "Mega Corp. Finance Team" \
        --organisation-url "http://mega.example.com/finance/"

[« elasticsearch-reset-password](reset-password.md) [elasticsearch-service-
tokens »](service-tokens-command.md)
