

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL ODBC](sql-odbc.md)

[« SQL ODBC](sql-odbc.md) [Configuration »](sql-odbc-setup.md)

## 驱动安装

Elasticsearch SQL ODBC 驱动程序可以使用 MSI 包安装在Microsoft Windows 上。安装过程很简单，由标准的 MSI 向导步骤组成。

### 安装先决条件

推荐的安装平台是 Windows 10 64 位或 Windows Server2016 64 位。

在安装 Elasticsearch SQL ODBC 驱动程序之前，您需要满足以下先决条件;

.NET Framework 4.x 完整、最新 - <https://dotnet.microsoft.com/download/dotnet-framework> * Visual Studio 2017 或更高版本的 Microsoft Visual C++ Redistributable - <https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist>

    * The 64 bit driver requires the x64 redistributable 
    * The 32 bit driver requires the x86 or the x64 redistributable (the latter also installs the components needed for the 32 bit driver) 

* 执行安装的用户的提升权限(管理员)。

如果未能满足任何先决条件，安装程序将显示错误消息并中止安装。

无法使用 MSI 进行内联升级。为了升级，您首先必须卸载旧驱动程序，然后安装新驱动程序。

安装 MSI 时，Windows Defender SmartScreen 可能会警告运行无法识别的应用。如果 MSI 是从 Elastic 的网站下载的，则可以通过允许安装继续("仍然运行")来确认该消息是安全的。

### 版本兼容性

您的驱动程序必须与您的 Elasticsearch 服务器版本兼容。

驱动程序版本不能比 Elasticsearch 服务器版本更新。例如，7.10.0 服务器与 8.9.0 驱动程序不兼容。

弹性搜索服务器版本 |兼容的驱动程序版本 |示例 ---|---|--- 8.0.0–8.9.0

|

* 相同版本 * 任何早期的 8.x 版本 * 7.7.0 之后的任何 7.x 版本。

|

8.9.0 服务器与 8.9.0 及更早版本的 8.x 驱动程序兼容。8.9.0 服务器还与 7.7.0 及更高版本的 7.x 驱动程序兼容。   7.7.1-7.17

|

* 相同版本 * 早期的 7.x 版本，回到 7.7.0。

|

7.10.0 服务器与 7.7.0-7.10.0 驱动程序兼容。   7.7.0 及更早版本

|

* 版本相同。

|

7.6.1 服务器仅与 7.6.1 驱动程序兼容。   ### 下载".msi"软件包编辑

从以下网址下载 Elasticsearch SQL ODBC Driver 8.9.0 的".msi"包：https：//www.elastic.co/downloads/odbc-client

有两个版本的安装程序可用：

* **32 位驱动程序 (x86)**，用于 Microsoft Office 2016 应用程序套件;特别是Microsoft Excel和Microsoft Access以及其他基于32位的程序。  * **64 位驱动程序 (x64)** 建议与所有其他应用程序一起使用。

用户应考虑下载并安装 32 位和 64 位驱动程序，以便在系统上安装的应用程序之间实现最大兼容性。

### 使用图形用户界面 (GUI) 进行安装

双击下载的".msi"软件包以启动 GUI 向导，该向导将指导您完成安装过程。

您将首先看到一个欢迎屏幕：

!安装程序欢迎屏幕

单击"**下一步**"将显示最终用户许可协议。您需要接受许可协议才能继续安装。

!安装程序 EULA 屏幕

以下屏幕允许您自定义 Elasticsearch ODBC 驱动程序文件的安装路径。

默认安装路径的格式为：**%ProgramFiles%\Elastic\ODBCDriver\8.9.0**

!安装程序驱动程序路径

您现在可以安装驱动程序了。

您将需要提升的权限(管理员)才能安装。

!安装程序开始

假设安装没有错误，您应该看到进度屏幕，然后是完成屏幕：

!安装程序安装

在完成屏幕上，您可以通过选中对话框复选框来启动"ODBC 数据源管理"屏幕。这将在关闭时自动启动配置屏幕(32 位或 64 位)，您可以在其中配置 DSN。

!安装程序完成

与任何 MSI 安装包一样，可以在"%TEMP%"目录中找到安装过程的日志文件，其中随机生成的名称遵循"MSI<random>"格式。日志'。

如果您在安装过程中遇到错误，我们建议您打开问题<https://github.com/elastic/elasticsearch-sql-odbc/issues>，附加您的安装日志文件并提供其他详细信息，以便我们进行调查。

### 使用命令行安装

下面给出的示例适用于 64 位 MSI 软件包的安装。要使用 32 位 MSI 软件包获得相同的结果，您将改用文件名后缀"windows-x86.msi"

".msi"也可以通过命令行安装。使用与 GUI 相同的默认值的最简单安装是通过首先导航到下载目录，然后运行以下命令来实现的：

    
    
    msiexec.exe /i esodbc-8.9.0-windows-x86_64.msi /qn

默认情况下，"msiexec.exe"不会等待安装过程完成，因为它在Windows子系统中运行。要等待进程完成并确保相应地设置"%ERRORLEVEL%"，建议使用"start /wait"创建一个进程并等待它退出：

    
    
    start /wait msiexec.exe /i esodbc-8.9.0-windows-x86_64.msi /qn

与任何 MSI 安装包一样，可以在"%TEMP%"目录中找到安装过程的日志文件，其中随机生成的名称遵循"MSI<random>"格式。日志'。可以使用"/l"命令行参数提供日志文件的路径

    
    
    start /wait msiexec.exe /i esodbc-8.9.0-windows-x86_64.msi /qn /l install.log

可以使用以下命令查看支持的 Windows 安装程序命令行参数：

    
    
    msiexec.exe /help

...​或通过查阅 Windows Installer SDK Command-LineOptions.aspx)。

#### 命令行选项

GUI 中公开的所有设置也可作为命令行参数(在 Windows 安装程序文档中称为 _properties_)，可以传递给"msiexec.exe"：

`INSTALLDIR`

|

安装目录。默认为'%ProgramFiles%\Elastic\ODBCDriver\8.9.0'。   ---|--- 要传递值，只需使用格式"=""将属性名称和值附加到<PROPERTYNAME><VALUE>安装命令中。例如，要使用与默认目录不同的安装目录：

    
    
    start /wait msiexec.exe /i esodbc-8.9.0-windows-x86_64.msi /qn INSTALLDIR="c:\CustomDirectory"

请参阅 Windows 安装程序 SDK 命令行选项.aspx)，了解与包含引号的值相关的其他规则。

#### 使用添加/删除程序卸载

".msi"软件包处理作为安装的一部分添加的所有目录和文件的卸载。

卸载将删除在安装过程中创建的**所有**内容。

可以通过按Windows键并键入"添加或删除程序"以打开系统设置来卸载已安装的程序。

打开后，在已安装的应用程序列表中找到 Elasticsearch ODBC 驱动程序安装，单击并选择"卸载"：

![uninstall](images/sql/odbc/uninstall.png)

#### 使用命令行卸载

也可以从命令行执行卸载，方法是导航到包含".msi"包的目录并运行：

    
    
    start /wait msiexec.exe /x esodbc-8.9.0-windows-x86_64.msi /qn

与安装过程类似，可以使用"/l"命令行参数传递卸载过程的日志文件的路径

    
    
    start /wait msiexec.exe /x esodbc-8.9.0-windows-x86_64.msi /qn /l uninstall.log

[« SQL ODBC](sql-odbc.md) [Configuration »](sql-odbc-setup.md)
