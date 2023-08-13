

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Repositories metering APIs](repositories-metering-
apis.md)

[« Get repositories metering information](get-repositories-metering-api.md)
[Rollup APIs »](rollup-apis.md)

## 清除存储库计量存档

删除群集中存在的存档存储库计量信息。

###Request

"删除/_nodes/<node_id>/_repositories_metering/<max_version_to_clear>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

您可以使用此 API 清除集群中的存档存储库计量信息。

### 路径参数

`<node_id>`

     (Optional, string) Comma-separated list of node IDs or names used to limit returned information. 
`<max_version_to_clear>`

     (long) Specifies the maximum [archive_version](get-repositories-metering-api.html#get-repositories-metering-api-response-body "Response body") to be cleared from the archive. 

此处介绍了所有节点选择性选项。

### 响应正文

返回已删除的存档存储库计量信息。

`_nodes`

    

(对象)包含有关请求选择的节点数的统计信息。

"_nodes"的属性

`total`

     (integer) Total number of nodes selected by the request. 
`successful`

     (integer) Number of nodes that responded successfully to the request. 
`failed`

     (integer) Number of nodes that rejected the request or failed to respond. If this value is not `0`, a reason for the rejection or failure is included in the response. 

`cluster_name`

     (string) Name of the cluster. Based on the [Cluster name setting](important-settings.html#cluster-name "Cluster name setting") setting. 
`nodes`

    

(对象)包含请求选择的节点的存储库计量信息。

"节点"的属性

`<node_id>`

    

(阵列)节点的存储库计量信息数组。

"node_id"中对象的属性

`repository_name`

     (string) Repository name. 
`repository_type`

     (string) Repository type. 
`repository_location`

    

(对象)表示存储库中的唯一位置。

存储库类型"Azure"的"repository_location"属性

`base_path`

     (string) The path within the container where the repository stores data. 
`container`

     (string) Container name. 

存储库类型"GCP"的"repository_location"属性

`base_path`

     (string) The path within the bucket where the repository stores data. 
`bucket`

     (string) Bucket name. 

存储库类型"S3"的"repository_location"属性

`base_path`

     (string) The path within the bucket where the repository stores data. 
`bucket`

     (string) Bucket name. 

`repository_ephemeral_id`

     (string) An identifier that changes every time the repository is updated. 
`repository_started_at`

     (long) Time the repository was created or updated. Recorded in milliseconds since the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time). 
`repository_stopped_at`

     (Optional, long) Time the repository was deleted or updated. Recorded in milliseconds since the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time). 
`archived`

     (Boolean) A flag that tells whether or not this object has been archived. When a repository is closed or updated the repository metering information is archived and kept for a certain period of time. This allows retrieving the repository metering information of previous repository instantiations. 
`cluster_version`

     (Optional, long) The cluster state version when this object was archived, this field can be used as a logical timestamp to delete all the archived metrics up to an observed version. This field is only present for archived repository metering information objects. The main purpose of this field is to avoid possible race conditions during repository metering information deletions, i.e. deleting archived repositories metering information that we haven't observed yet. 
`request_counts`

    

(对象)具有对存储库执行的请求数(按请求类型分组)的对象。

存储库类型"Azure"的"request_counts"属性

`GetBlobProperties`

     (long) Number of [Get Blob Properties](https://docs.microsoft.com/en-us/rest/api/storageservices/get-blob-properties) requests. 
`GetBlob`

     (long) Number of [Get Blob](https://docs.microsoft.com/en-us/rest/api/storageservices/get-blob) requests. 
`ListBlobs`

     (long) Number of [List Blobs](https://docs.microsoft.com/en-us/rest/api/storageservices/list-blobs) requests. 
`PutBlob`

     (long) Number of [Put Blob](https://docs.microsoft.com/en-us/rest/api/storageservices/put-blob) requests. 
`PutBlock`

     (long) Number of [Put Block](https://docs.microsoft.com/en-us/rest/api/storageservices/put-block). 
`PutBlockList`

     (long) Number of [Put Block List](https://docs.microsoft.com/en-us/rest/api/storageservices/put-block-list) requests. 

Azure 存储定价。

存储库类型"GCP"的"request_counts"属性

`GetObject`

     (long) Number of [get object](https://cloud.google.com/storage/docs/json_api/v1/objects/get) requests. 
`ListObjects`

     (long) Number of [list objects](https://cloud.google.com/storage/docs/json_api/v1/objects/list) requests. 
`InsertObject`

     (long) Number of [insert object](https://cloud.google.com/storage/docs/json_api/v1/objects/insert) requests, including [simple](https://cloud.google.com/storage/docs/uploading-objects), [multipart](https://cloud.google.com/storage/docs/json_api/v1/how-tos/multipart-upload) and [resumable](https://cloud.google.com/storage/docs/resumable-uploads) uploads. Resumable uploads can perform multiple http requests to insert a single object but they are considered as a single request since they are [billed](https://cloud.google.com/storage/docs/resumable-uploads#introduction) as an individual operation. 

谷歌云存储定价。

存储库类型"S3"的"request_counts"属性

`GetObject`

     (long) Number of [GetObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html) requests. 
`ListObjects`

     (long) Number of [ListObjects](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjects.html) requests. 
`PutObject`

     (long) Number of [PutObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html) requests. 
`PutMultipartObject`

     (long) Number of [Multipart](https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html) requests, including [CreateMultipartUpload](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateMultipartUpload.html), [UploadPart](https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html) and [CompleteMultipartUpload](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CompleteMultipartUpload.html) requests. 

亚马逊云科技简单存储服务定价。

[« Get repositories metering information](get-repositories-metering-api.md)
[Rollup APIs »](rollup-apis.md)
