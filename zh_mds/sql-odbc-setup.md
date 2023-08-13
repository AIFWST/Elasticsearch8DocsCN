

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL ODBC](sql-odbc.md)

[« Driver installation](sql-odbc-installation.md) [SQL Client Applications
»](sql-client-apps.md)

##Configuration

安装驱动程序后，为了使应用程序能够通过 ODBC 连接到 Elasticsearch，必须向驱动程序提供一组配置参数。根据应用程序的不同，通常有三种方式可以提供这些参数：

* 通过连接字符串;  * 使用用户 DSN 或系统 DSN;  * 通过文件 DSN。

DSN(_data源name_)是ODBC驱动程序连接到数据库所需的参数集的通用名称。

我们将这些参数称为 _connection parameters_ 或 _DSN_(尽管这些参数配置驱动程序功能的其他一些方面;例如日志记录、缓冲区大小......

使用 DSN 是执行驱动程序配置的最广泛使用、最简单和最安全的方法。另一方面，构造连接字符串是最粗糙的方法，因此也是最不常见的方法。

我们将只关注DSN的使用情况。

### 1\.启动 ODBC 数据源管理器

对于 DSN 管理，ODBC 提供了_ODBC数据源Administrator_application，可随时安装在所有最新的桌面 Windows 操作系统上。

* 32 位版本的 Odbcad32.exe 文件位于 '%systemdrive%\Windows\SysWoW64' 文件夹中。  * 64 位版本的 Odbcad32.exe 文件位于 '%systemdrive%\Windows\System32' 文件夹中。

要启动它，请打开搜索菜单 - _Win + S_ \- 并键入"ODBC 数据源(64 位)"或"ODBC 数据源(32 位)"，然后按 _Enter_ ：

**启动 ODBC 数据源管理器**！启动管理员

启动后，您可以通过单击 ODBC 数据源管理器的 _Drivers_ 选项卡并检查已安装驱动程序列表中是否存在_Elasticsearch Driver_来验证驱动程序是否已正确安装。

您还应该看到已安装驱动程序的版本号。

"驱动程序"选项卡"管理员驱动程序

### 2\.配置一个DSN

下一步是配置 DSN。您可以在 管理员应用程序的前三个选项卡上映射的以下选项之间进行选择：

* 用户 DSN

在此选项卡下配置的连接仅对当前登录的用户可用。其中每个 DSN 都由选定的任意名称(通常是主机或群集名称)引用。

组成 DSN 的实际参数集通过驱动程序存储在系统注册表中。因此，用户以后只需向应用程序提供DSN名称，即可连接到配置的Elasticsearch实例。

* 系统DSN

与用户 DSN 类似，不同之处在于在此选项卡下配置的连接可供系统上配置的所有用户使用。

* 文件 DSN

此选项卡包含允许将一组连接参数写入文件而不是注册表的功能。

然后可以在多个系统之间共享此类文件，并且用户需要指定该文件的路径，以便应用程序连接到配置的Elasticsearch实例。

上述所有要点的配置步骤都是相似的。以下是配置系统 DSN 的示例。

##### 2.1 启动 Elasticsearch SQL ODBC 驱动程序 DSNEditor

单击"_System DSN_"选项卡，然后单击"_Add..._"按钮：

**添加新的 DSN**！管理员系统添加

将打开一个新窗口，列出所有可用的已安装驱动程序。单击on_Elasticsearch Driver_ ，突出显示它，然后在 _Finish_ 按钮上：

**启动DSN编辑器**！管理员启动编辑器

此操作将关闭之前打开的第二个窗口并打开一个新窗口，即 Elasticsearch SQL ODBC 驱动程序的 DSN 编辑器：

**Elasticsearch SQL ODBC Driver DSN Editor**！dsn editorbasic

这个新窗口有三个选项卡，每个选项卡负责一组配置参数，如下所示。

##### 2.2 连接参数

此选项卡允许配置以下项目：

*名字

这是DSN将引用的名称。

可用于此字段的字符仅限于注册表项允许的字符集。

示例：_本地主机_

*描述

此字段允许任意文本;通常用于有关已配置连接的简短说明。

示例：与本地 [：：1]：9200._ 的_Clear文本连接

* 云标识

_Cloud ID_是一个字符串，用于简化连接到 Elastic 的云 Elasticsearch 服务时的配置;它是从每个 Elasticsearch 集群的云控制台中获取的，并将连接参数编码到该集群。

置备此字段时，也会置备 _主机名_ 、 _端口_ 和安全设置，并禁用其各自的输入。

* 主机名

此字段需要驱动程序将连接到的 Elasticsearch 实例的 IP 地址或可解析的 DNS 名称。

示例：_：：1_

*港口

Elasticsearch 侦听的端口。

如果留空，将使用默认的 **9200** 端口号。

* 用户名、密码

如果启用了安全性，则这些字段需要包含访问用户的凭据。

至少必须设置"名称_"和"主机名"字段，然后才能保存 DSN。

默认情况下启用连接加密。如果连接到没有加密的 Elasticsearch 节点，则需要更改此设置。

##### 2.3 加密参数

可以选择以下 SSL 选项之一：

*禁用。所有通信均未加密。

驱动程序和 Elasticsearch 实例之间的通信是通过明文连接执行的。

此设置可能会向拦截网络流量的第三方公开访问凭据，因此不建议使用此设置。

*启用。证书未验证。

连接加密已启用，但未验证服务器的证书。

这是当前的默认设置。

此设置允许第三方作为中间人轻松行动，从而拦截所有通信。

*启用。证书已验证;主机名未验证。

连接加密已启用，驱动程序验证服务器的证书是否有效，但它不会验证证书是否在它所针对的服务器上运行。

此设置允许有权访问服务器证书的第三方充当中间人，从而拦截所有通信。

*启用。证书已验证;主机名已验证。

连接加密已启用，驱动程序将验证证书是否有效，以及证书是否部署在证书所针对的服务器上。

*启用。证书身份链已验证。

此设置等效于上一个设置，但会额外检查证书的吊销。这提供了最强大的安全选项，并且是生产部署的推荐设置。

* 证书文件

如果服务器使用的证书不属于 PKI(例如使用自签名证书)，则可以配置驱动程序将用于验证服务器提供的证书的 X.509 证书文件的路径。

驱动程序只会在尝试连接之前读取文件的内容。请参阅2.7 测试连接部分，进一步了解如何检查所提供参数的有效性。

证书文件不能捆绑或密码保护，因为驱动程序不会提示输入密码。

如果使用文件浏览器查找证书 - 通过按 _Browse..._ 按钮 - 默认情况下仅考虑具有 _.pem_ 和_.der_扩展名的文件。从下拉列表中选择_All文件 (*.*)_，如果您的文件以不同的扩展名结尾：

**证书文件浏览器**！dsn 编辑器安全证书

##### 2.4 代理参数

如果连接到 Elasticsearch 节点需要通过代理，则需要配置以下参数：

*类型

连接到代理主机时使用哪种协议。这也要求如何在 2.2 连接参数下指定您希望通过代理连接到的 Elasticsearch 节点：

    * HTTP, SOCKS4A, SOCKS5H: either IP address or host name is accepted; the proxy will resolve the DNS name; 
    * SOCKS4, SOCKS5: Elasticsearch node location needs to be provided as an IP address; 

*港口

代理正在侦听连接的 TCP 端口。

* 用户名

用于向代理进行身份验证的凭据的用户部分。

*密码

代理凭据的密码部分。

**代理参数**！dsn 编辑器代理

##### 2.5 连接参数

可以通过以下参数进一步调整连接配置。

* 请求超时 (s)

对服务器的请求可以花费的最长时间(以秒为单位)。这可以被更大的语句级超时设置覆盖。值 0 表示无超时。

* 最大页面大小(行)

Elasticsearch SQL 服务器应为一页发送驱动程序的最大行数。这对应于 SQL 搜索 API 的"fetch_size"参数。"0"值表示服务器默认值。

* 最大页面长度 (MB)

答案在被驱动程序拒绝为太大之前可以增长到的最大大小(以兆字节为单位)。这是关于一个页面的 HTTP 答案正文，而不是查询可能生成的累积数据量。

* 瓦尔查尔限制

字符串列的最大宽度。如果此设置大于零，驱动程序会将所有字符串类型列播发为具有等于此值的最大字符长度，并将截断任何更长的字符串 toit。字符串类型是文本字段(文本，关键字等)和一些专用字段(IP，GEO等)。请注意，在截断之前不会对值执行任何解释，如果限制设置得太低，则可能导致无效值。对于那些不支持与 Elasticsearch 字段一样大的列长度的应用程序，这是必需的。

*浮动格式

控制当浮点数由驱动程序转换为字符串时，如何打印这些浮点数。此参数的可能值：

    * `scientific`: the exponential notation (ex.: 1.23E01); 
    * `default`: the default notation (ex.: 12.3); 
    * `auto`: the driver will choose one of the above depending on the value to be printed. Note that the number of decimals is dependent on the precision (or ODBC scale) of the value being printed and varies with the different floating point types supported by Elasticsearch SQL. This setting is not effective when the application fetches from the driver the values as numbers and then does the conversion subsequently itself. 

* 数据编码

此值控制要对 REST 内容进行编码的数据格式。可能的值为：

    * `CBOR`: use the Concise Binary Object Representation format. This is the preferred encoding, given its more compact format. 
    * `JSON`: use the JavaScript Object Notation format. This format is more verbose, but easier to read, especially useful if troubleshooting. 

* 数据压缩

此设置控制是否以及何时压缩 REST 内容(以上述格式之一编码)。可能的值为：

    * `on`: enables the compression; 
    * `off`: disables the compression; 
    * `auto`: enables the compression, except for the case when the data flows through a secure connection; since in this case the encryption layer employs its own data compression and there can be security implications when an additional compression is enabled, the setting should be kept to this value. 

* 遵循 HTTP 重定向

驱动程序是否应遵循对服务器的请求的 HTTP 重定向？

* 使用当地时区

此设置控制以下各项的时区：

    * the context in which the query will execute (especially relevant for functions dealing with timestamp components); 
    * the timestamps received from / sent to the server.

如果禁用，将应用 UTC 时区;否则，为本地计算机的设置时区。

* 自动转义 PVA

模式值参数使用"_"和"%"作为特殊字符来构建模式匹配值。然而，一些应用程序使用这些字符作为常规字符，这可能导致Elasticsearch SQL返回比应用程序预期的更多的数据。通过自动转义，驱动程序将检查参数，如果应用程序尚未完成，则将转义这些特殊字符。

* 多值字段宽松

此设置控制在查询多值字段时服务器的行为。如果设置了此字段并且服务器遇到这样的字段，它将在集合中选择一个值 - 不保证该值是什么，但通常是自然升序中的第一个值 - 并将其作为列的值返回。如果未设置，服务器将返回错误。这对应于 SQL 搜索 API 的"field_multi_value_leniency"参数。

* 包括冻结索引

如果此参数为"true"，则服务器将在查询执行中包含冻结的索引。这对应于Elasticsearch SQL的请求参数'index_include_frozen'

* 早期查询执行

如果设置了此配置，则驱动程序将在应用程序提交语句进行准备(即早期)后立即执行该语句，并且在功能上等效于直接执行。仅当查询缺少参数时，才会发生这种情况。早期执行对于那些在实际执行查询之前检查结果的应用程序很有用。Elasticsearch SQL缺乏准备API，因此需要尽早执行才能与这些应用程序进行互操作性。

**连接参数**！dsn 编辑器杂项

##### 2.6 日志记录参数

出于故障排除目的，Elasticsearch SQL ODBC 驱动程序提供了记录应用程序进行的 API 调用的功能;这在管理员应用程序中启用：

**启用应用程序 ODBC API 日志记录**！管理员跟踪

但是，这只会将应用程序进行的 ODBC API 调用记录到the_Driver Manager_中，而不会将_Driver Manager_进行的 ODBC API 调用记录到驱动程序本身中。若要启用驱动程序接收的调用以及内部驱动程序处理事件的日志记录，可以在编辑器的选项卡上启用驱动程序s_Logging_日志记录：

* 启用日志记录？

勾选此项将启用驱动程序的日志记录。启用此选项时，日志记录目录也是必需的(请参阅下一个选项)。但是，即使禁用了日志记录，指定的日志记录目录也将保存在 DSN 中(如果提供)。

* 日志目录

此处指定要将日志文件写入哪个目录。

驱动程序将为生成日志记录消息的连接创建每个连接一个日志文件。

* 日志级别

配置日志的详细程度。

**启用驱动程序日志记录**！dsn 编辑器日志记录

启用身份验证后，将从日志中编辑密码。

调试日志记录可以快速导致创建许多非常大的文件，并产生大量的处理开销。仅在指示时启用，最好仅在获取少量数据时启用。

##### 2.7 测试连接

配置 _Hostname_ 、_Port_(如果不同于隐式默认值)和 SSL 选项后，您可以通过按 _Test Connection_ 按钮来测试提供的参数是否正确。这将指示驱动程序连接到 Elasticsearch 实例并执行简单的 SQL 测试查询。(因此，这将需要一个启用了SQL插件的正在运行的Elasticsearch实例。

**连接测试**！dsn editorconntest

连接测试时，会考虑所有配置的参数，包括日志记录配置。这将允许及早检测潜在的文件/目录访问权限冲突。

有关配置日志记录的替代方法，请参阅备用日志记录配置部分。

### 3\.DSN可用

一切就绪后，按 _Save_ 按钮会将配置存储到所选目标(注册表或文件)中。

在保存DSN配置之前，将验证提供的文件/目录路径在当前系统上是否有效。但是，DSN 编辑器不会以任何方式验证配置的 _主机名_ ：_Port_ 的有效性或可访问性。请参阅 2.7 测试连接以进行详尽检查。

如果一切正确，新创建的DSN的名称将列出为可供使用：

**连接已添加**！管理员系统已添加

### 备用日志记录配置

由于 ODBC API 的规范，驱动程序将仅在调用连接 API 后接收配置的 DSN 参数(包括日志记录参数)(如 _SQLConnect_ 或 _SQLDriverConnect_)。但是，The_Driver Manager_将始终在尝试建立连接之前对驱动程序进行一组 API 调用。要捕获这些调用，需要以另一种方式传递日志记录配置参数。TheElasticsearch SQL ODBC Driver 将为此目的使用环境变量。

配置环境变量是特定于操作系统的，本指南中未详细介绍。变量是应配置系统范围还是特定于用户取决于启用 ODBC 的应用程序的运行方式，以及日志记录是否应仅影响当前用户。

环境变量的定义需要按如下方式完成：

* 名称：_ESODBC_LOG_DIR_ * 值：路径，其中：

[path] 是日志文件将写入的目录的路径;

[level] 是可选的，可以采用以下值之一：_调试_、_信息_、_警告_、_错误_ ;如果未提供，则假定为 _debug_。

**日志记录环境变量**！env varlog

通过环境变量启用日志记录时，驱动程序将为每个进程创建一个日志文件。

两种配置日志记录的方法可以共存，并且都可以使用相同的目标日志记录目录。但是，一条日志记录消息将只记录一次，连接日志记录优先于环境变量日志记录。

[« Driver installation](sql-odbc-installation.md) [SQL Client Applications
»](sql-client-apps.md)
