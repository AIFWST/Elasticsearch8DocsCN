[What is Elasticsearch?](./elasticsearch-intro.md)

[Data in: documents and indices](./documents-indices.md)

[Information out: search and analyze](./search-analyze.md)

[Scalability and resilience](./scalability.md)

[What’s new in 8.9](./release-highlights.md)

[Set up Elasticsearch](./setup.md)

[Installing Elasticsearch](./install-elasticsearch.md)

[Install Elasticsearch from archive on Linux or MacOS](./targz.md)

[Install Elasticsearch with .zip on Windows](./zip-windows.md)

[Install Elasticsearch with Debian Package](./deb.md)

[Install Elasticsearch with RPM](./rpm.md)

[Install Elasticsearch with Docker](./docker.md)

[Run Elasticsearch locally](./run-elasticsearch-locally.md)

[Configuring Elasticsearch](./settings.md)

[Important Elasticsearch configuration](./important-settings.md)

[Secure settings](./secure-settings.md)

[Auditing settings](./auditing-settings.md)

[Circuit breaker settings](./circuit-breaker.md)

[Cluster-level shard allocation and routing settings](./modules-cluster.md)

[Miscellaneous cluster settings](./misc-cluster-settings.md)

[Cross-cluster replication settings](./ccr-settings.md)

[Discovery and cluster formation settings](./modules-discovery-settings.md)

[Field data cache settings](./modules-fielddata.md)

[Health Diagnostic settings](./health-diagnostic-settings.md)

[Index lifecycle management settings](./ilm-settings.md)

[Index management settings](./index-management-settings.md)

[Index recovery settings](./recovery.md)

[Indexing buffer settings](./indexing-buffer.md)

[License settings](./license-settings.md)

[Local gateway settings](./modules-gateway.md)

[Logging](./logging.md)

[Machine learning settings](./ml-settings.md)

[Monitoring settings](./monitoring-settings.md)

[Node](./modules-node.md)

[Networking](./modules-network.md)

[Node query cache settings](./query-cache.md)

[Search settings](./search-settings.md)

[Security settings](./security-settings.md)

[Shard request cache settings](./shard-request-cache.md)

[Snapshot and restore settings](./snapshot-settings.md)

[Transforms settings](./transform-settings.md)

[Thread pools](./modules-threadpool.md)

[Watcher settings](./notification-settings.md)

[Advanced configuration](./advanced-configuration.md)

[Important system configuration](./system-config.md)

[Configuring system settings](./setting-system-settings.md)

[Disable swapping](./setup-configuration-memory.md)

[File Descriptors](./file-descriptors.md)

[Virtual memory](./vm-max-map-count.md)

[Number of threads](./max-number-of-threads.md)

[DNS cache settings](./networkaddress-cache-ttl.md)

[Ensure JNA temporary directory permits executables](./executable-jna-tmpdir.md)

[TCP retransmission timeout](./system-config-tcpretries.md)

[Bootstrap Checks](./bootstrap-checks.md)

[Heap size check](./_heap_size_check.md)

[File descriptor check](./_file_descriptor_check.md)

[Memory lock check](./_memory_lock_check.md)

[Maximum number of threads check](./max-number-threads-check.md)

[Max file size check](./_max_file_size_check.md)

[Maximum size virtual memory check](./max-size-virtual-memory-check.md)

[Maximum map count check](./_maximum_map_count_check.md)

[Client JVM check](./_client_jvm_check.md)

[Use serial collector check](./_use_serial_collector_check.md)

[System call filter check](./_system_call_filter_check.md)

[OnError and OnOutOfMemoryError checks](./_onerror_and_onoutofmemoryerror_checks.md)

[Early-access check](./_early_access_check.md)

[G1GC check](./_g1gc_check.md)

[All permission check](./_all_permission_check.md)

[Discovery configuration check](./_discovery_configuration_check.md)

[Bootstrap Checks for X-Pack](./bootstrap-checks-xpack.md)

[Starting Elasticsearch](./starting-elasticsearch.md)

[Stopping Elasticsearch](./stopping-elasticsearch.md)

[Discovery and cluster formation](./modules-discovery.md)

[Discovery](./discovery-hosts-providers.md)

[Quorum-based decision making](./modules-discovery-quorums.md)

[Voting configurations](./modules-discovery-voting.md)

[Bootstrapping a cluster](./modules-discovery-bootstrap-cluster.md)

[Publishing the cluster state](./cluster-state-publishing.md)

[Cluster fault detection](./cluster-fault-detection.md)

[Add and remove nodes in your cluster](./add-elasticsearch-nodes.md)

[Full-cluster restart and rolling restart](./restart-cluster.md)

[Remote clusters](./remote-clusters.md)

[Configure remote clusters with security](./remote-clusters-security.md)

[Connect to remote clusters](./remote-clusters-connect.md)

[Configure roles and users for remote clusters](./remote-clusters-privileges.md)

[Remote cluster settings](./remote-clusters-settings.md)

[Plugins](./modules-plugins.md)

[Upgrade Elasticsearch](./setup-upgrade.md)

[Archived settings](./archived-settings.md)

[Reading indices from older Elasticsearch versions](./archive-indices.md)

[Index modules](./index-modules.md)

[Analysis](./index-modules-analysis.md)

[Index Shard Allocation](./index-modules-allocation.md)

[Index-level shard allocation filtering](./shard-allocation-filtering.md)

[Delaying allocation when a node leaves](./delayed-allocation.md)

[Index recovery prioritization](./recovery-prioritization.md)

[Total shards per node](./allocation-total-shards.md)

[Index-level data tier allocation filtering](./data-tier-shard-filtering.md)

[Index blocks](./index-modules-blocks.md)

[Mapper](./index-modules-mapper.md)

[Merge](./index-modules-merge.md)

[Similarity module](./index-modules-similarity.md)

[Slow Log](./index-modules-slowlog.md)

[Store](./index-modules-store.md)

[Preloading data into the file system cache](./preload-data-to-file-system-cache.md)

[Translog](./index-modules-translog.md)

[History retention](./index-modules-history-retention.md)

[Index Sorting](./index-modules-index-sorting.md)

[Use index sorting to speed up conjunctions](./index-modules-index-sorting-conjunctions.md)

[Indexing pressure](./index-modules-indexing-pressure.md)

[Mapping](./mapping.md)

[Dynamic mapping](./dynamic-mapping.md)

[Dynamic field mapping](./dynamic-field-mapping.md)

[Dynamic templates](./dynamic-templates.md)

[Explicit mapping](./explicit-mapping.md)

[Runtime fields](./runtime.md)

[Map a runtime field](./runtime-mapping-fields.md)

[Define runtime fields in a search request](./runtime-search-request.md)

[Override field values at query time](./runtime-override-values.md)

[Retrieve a runtime field](./runtime-retrieving-fields.md)

[Index a runtime field](./runtime-indexed.md)

[Explore your data with runtime fields](./runtime-examples.md)

[Field data types](./mapping-types.md)

[Aggregate metric](./aggregate-metric-double.md)

[Alias](./field-alias.md)

[Arrays](./array.md)

[Binary](./binary.md)

[Boolean](./boolean.md)

[Completion](./completion.md)

[Date](./date.md)

[Date nanoseconds](./date_nanos.md)

[Dense vector](./dense-vector.md)

[Flattened](./flattened.md)

[Geopoint](./geo-point.md)

[Geoshape](./geo-shape.md)

[Histogram](./histogram.md)

[IP](./ip.md)

[Join](./parent-join.md)

[Keyword](./keyword.md)

[Nested](./nested.md)

[Numeric](./number.md)

[Object](./object.md)

[Percolator](./percolator.md)

[Point](./point.md)

[Range](./range.md)

[Rank feature](./rank-feature.md)

[Rank features](./rank-features.md)

[Search-as-you-type](./search-as-you-type.md)

[Shape](./shape.md)

[Text](./text.md)

[Token count](./token-count.md)

[Unsigned long](./unsigned-long.md)

[Version](./version.md)

[Metadata fields](./mapping-fields.md)

[_doc_count field](./mapping-doc-count-field.md)

[_field_names field](./mapping-field-names-field.md)

[_ignored field](./mapping-ignored-field.md)

[_id field](./mapping-id-field.md)

[_index field](./mapping-index-field.md)

[_meta field](./mapping-meta-field.md)

[_routing field](./mapping-routing-field.md)

[_source field](./mapping-source-field.md)

[_tier field](./mapping-tier-field.md)

[Mapping parameters](./mapping-params.md)

[analyzer](./analyzer.md)

[coerce](./coerce.md)

[copy_to](./copy-to.md)

[doc_values](./doc-values.md)

[dynamic](./dynamic.md)

[eager_global_ordinals](./eager-global-ordinals.md)

[enabled](./enabled.md)

[format](./mapping-date-format.md)

[ignore_above](./ignore-above.md)

[ignore_malformed](./ignore-malformed.md)

[index](./mapping-index.md)

[index_options](./index-options.md)

[index_phrases](./index-phrases.md)

[index_prefixes](./index-prefixes.md)

[meta](./mapping-field-meta.md)

[fields](./multi-fields.md)

[normalizer](./normalizer.md)

[norms](./norms.md)

[null_value](./null-value.md)

[position_increment_gap](./position-increment-gap.md)

[properties](./properties.md)

[search_analyzer](./search-analyzer.md)

[similarity](./similarity.md)

[store](./mapping-store.md)

[subobjects](./subobjects.md)

[term_vector](./term-vector.md)

[Mapping limit settings](./mapping-settings-limit.md)

[Removal of mapping types](./removal-of-types.md)

[Text analysis](./analysis.md)

[Overview](./analysis-overview.md)

[Concepts](./analysis-concepts.md)

[Anatomy of an analyzer](./analyzer-anatomy.md)

[Index and search analysis](./analysis-index-search-time.md)

[Stemming](./stemming.md)

[Token graphs](./token-graphs.md)

[Configure text analysis](./configure-text-analysis.md)

[Test an analyzer](./test-analyzer.md)

[Configuring built-in analyzers](./configuring-analyzers.md)

[Create a custom analyzer](./analysis-custom-analyzer.md)

[Specify an analyzer](./specify-analyzer.md)

[Built-in analyzer reference](./analysis-analyzers.md)

[Fingerprint](./analysis-fingerprint-analyzer.md)

[Keyword](./analysis-keyword-analyzer.md)

[Language](./analysis-lang-analyzer.md)

[Pattern](./analysis-pattern-analyzer.md)

[Simple](./analysis-simple-analyzer.md)

[Standard](./analysis-standard-analyzer.md)

[Stop](./analysis-stop-analyzer.md)

[Whitespace](./analysis-whitespace-analyzer.md)

[Tokenizer reference](./analysis-tokenizers.md)

[Character group](./analysis-chargroup-tokenizer.md)

[Classic](./analysis-classic-tokenizer.md)

[Edge n-gram](./analysis-edgengram-tokenizer.md)

[Keyword](./analysis-keyword-tokenizer.md)

[Letter](./analysis-letter-tokenizer.md)

[Lowercase](./analysis-lowercase-tokenizer.md)

[N-gram](./analysis-ngram-tokenizer.md)

[Path hierarchy](./analysis-pathhierarchy-tokenizer.md)

[Pattern](./analysis-pattern-tokenizer.md)

[Simple pattern](./analysis-simplepattern-tokenizer.md)

[Simple pattern split](./analysis-simplepatternsplit-tokenizer.md)

[Standard](./analysis-standard-tokenizer.md)

[Thai](./analysis-thai-tokenizer.md)

[UAX URL email](./analysis-uaxurlemail-tokenizer.md)

[Whitespace](./analysis-whitespace-tokenizer.md)

[Token filter reference](./analysis-tokenfilters.md)

[Apostrophe](./analysis-apostrophe-tokenfilter.md)

[ASCII folding](./analysis-asciifolding-tokenfilter.md)

[CJK bigram](./analysis-cjk-bigram-tokenfilter.md)

[CJK width](./analysis-cjk-width-tokenfilter.md)

[Classic](./analysis-classic-tokenfilter.md)

[Common grams](./analysis-common-grams-tokenfilter.md)

[Conditional](./analysis-condition-tokenfilter.md)

[Decimal digit](./analysis-decimal-digit-tokenfilter.md)

[Delimited payload](./analysis-delimited-payload-tokenfilter.md)

[Dictionary decompounder](./analysis-dict-decomp-tokenfilter.md)

[Edge n-gram](./analysis-edgengram-tokenfilter.md)

[Elision](./analysis-elision-tokenfilter.md)

[Fingerprint](./analysis-fingerprint-tokenfilter.md)

[Flatten graph](./analysis-flatten-graph-tokenfilter.md)

[Hunspell](./analysis-hunspell-tokenfilter.md)

[Hyphenation decompounder](./analysis-hyp-decomp-tokenfilter.md)

[Keep types](./analysis-keep-types-tokenfilter.md)

[Keep words](./analysis-keep-words-tokenfilter.md)

[Keyword marker](./analysis-keyword-marker-tokenfilter.md)

[Keyword repeat](./analysis-keyword-repeat-tokenfilter.md)

[KStem](./analysis-kstem-tokenfilter.md)

[Length](./analysis-length-tokenfilter.md)

[Limit token count](./analysis-limit-token-count-tokenfilter.md)

[Lowercase](./analysis-lowercase-tokenfilter.md)

[MinHash](./analysis-minhash-tokenfilter.md)

[Multiplexer](./analysis-multiplexer-tokenfilter.md)

[N-gram](./analysis-ngram-tokenfilter.md)

[Normalization](./analysis-normalization-tokenfilter.md)

[Pattern capture](./analysis-pattern-capture-tokenfilter.md)

[Pattern replace](./analysis-pattern_replace-tokenfilter.md)

[Phonetic](./analysis-phonetic-tokenfilter.md)

[Porter stem](./analysis-porterstem-tokenfilter.md)

[Predicate script](./analysis-predicatefilter-tokenfilter.md)

[Remove duplicates](./analysis-remove-duplicates-tokenfilter.md)

[Reverse](./analysis-reverse-tokenfilter.md)

[Shingle](./analysis-shingle-tokenfilter.md)

[Snowball](./analysis-snowball-tokenfilter.md)

[Stemmer](./analysis-stemmer-tokenfilter.md)

[Stemmer override](./analysis-stemmer-override-tokenfilter.md)

[Stop](./analysis-stop-tokenfilter.md)

[Synonym](./analysis-synonym-tokenfilter.md)

[Synonym graph](./analysis-synonym-graph-tokenfilter.md)

[Trim](./analysis-trim-tokenfilter.md)

[Truncate](./analysis-truncate-tokenfilter.md)

[Unique](./analysis-unique-tokenfilter.md)

[Uppercase](./analysis-uppercase-tokenfilter.md)

[Word delimiter](./analysis-word-delimiter-tokenfilter.md)

[Word delimiter graph](./analysis-word-delimiter-graph-tokenfilter.md)

[Character filters reference](./analysis-charfilters.md)

[HTML strip](./analysis-htmlstrip-charfilter.md)

[Mapping](./analysis-mapping-charfilter.md)

[Pattern replace](./analysis-pattern-replace-charfilter.md)

[Normalizers](./analysis-normalizers.md)

[Index templates](./index-templates.md)

[Simulate multi-component templates](./simulate-multi-component-templates.md)

[Config ignore_missing_component_templates](./ignore_missing_component_templates.md)

[Usage example](./_usage_example.md)

[Data streams](./data-streams.md)

[Set up a data stream](./set-up-a-data-stream.md)

[Use a data stream](./use-a-data-stream.md)

[Modify a data stream](./modify-data-streams.md)

[Time series data stream (TSDS)](./tsds.md)

[Set up a TSDS](./set-up-tsds.md)

[Time series index settings](./tsds-index-settings.md)

[Downsampling a time series data stream](./downsampling.md)

[Run downsampling with ILM](./downsampling-ilm.md)

[Run downsampling manually](./downsampling-manual.md)

[Ingest pipelines](./ingest.md)

[Example: Parse logs](./common-log-format-example.md)

[Enrich your data](./ingest-enriching-data.md)

[Set up an enrich processor](./enrich-setup.md)

[Example: Enrich your data based on geolocation](./geo-match-enrich-policy-type.md)

[Example: Enrich your data based on exact values](./match-enrich-policy-type.md)

[Example: Enrich your data by matching a value to a range](./range-enrich-policy-type.md)

[Processor reference](./processors.md)

[Append](./append-processor.md)

[Attachment](./attachment.md)

[Bytes](./bytes-processor.md)

[Circle](./ingest-circle-processor.md)

[Community ID](./community-id-processor.md)

[Convert](./convert-processor.md)

[CSV](./csv-processor.md)

[Date](./date-processor.md)

[Date index name](./date-index-name-processor.md)

[Dissect](./dissect-processor.md)

[Dot expander](./dot-expand-processor.md)

[Drop](./drop-processor.md)

[Enrich](./enrich-processor.md)

[Fail](./fail-processor.md)

[Fingerprint](./fingerprint-processor.md)

[Foreach](./foreach-processor.md)

[Geo-grid](./ingest-geo-grid-processor.md)

[GeoIP](./geoip-processor.md)

[Grok](./grok-processor.md)

[Gsub](./gsub-processor.md)

[HTML strip](./htmlstrip-processor.md)

[Inference](./inference-processor.md)

[Join](./join-processor.md)

[JSON](./json-processor.md)

[KV](./kv-processor.md)

[Lowercase](./lowercase-processor.md)

[Network direction](./network-direction-processor.md)

[Pipeline](./pipeline-processor.md)

[Redact](./redact-processor.md)

[Registered domain](./registered-domain-processor.md)

[Remove](./remove-processor.md)

[Rename](./rename-processor.md)

[Reroute](./reroute-processor.md)

[Script](./script-processor.md)

[Set](./set-processor.md)

[Set security user](./ingest-node-set-security-user-processor.md)

[Sort](./sort-processor.md)

[Split](./split-processor.md)

[Trim](./trim-processor.md)

[Uppercase](./uppercase-processor.md)

[URL decode](./urldecode-processor.md)

[URI parts](./uri-parts-processor.md)

[User agent](./user-agent-processor.md)

[Aliases](./aliases.md)

[Search your data](./search-your-data.md)

[Collapse search results](./collapse-search-results.md)

[Filter search results](./filter-search-results.md)

[Highlighting](./highlighting.md)

[Long-running searches](./async-search-intro.md)

[Near real-time search](./near-real-time.md)

[Paginate search results](./paginate-search-results.md)

[Retrieve inner hits](./inner-hits.md)

[Retrieve selected fields](./search-fields.md)

[Search across clusters](./modules-cross-cluster-search.md)

[Search multiple data streams and indices](./search-multiple-indices.md)

[Search shard routing](./search-shard-routing.md)

[Search templates](./search-template.md)

[Search template examples with Mustache](./search-template-with-mustache-examples.md)

[Sort search results](./sort-search-results.md)

[kNN search](./knn-search.md)

[Semantic search](./semantic-search.md)

[Semantic search with ELSER](./semantic-search-elser.md)

[Query DSL](./query-dsl.md)

[Query and filter context](./query-filter-context.md)

[Compound queries](./compound-queries.md)

[Boolean](./query-dsl-bool-query.md)

[Boosting](./query-dsl-boosting-query.md)

[Constant score](./query-dsl-constant-score-query.md)

[Disjunction max](./query-dsl-dis-max-query.md)

[Function score](./query-dsl-function-score-query.md)

[Full text queries](./full-text-queries.md)

[Intervals](./query-dsl-intervals-query.md)

[Match](./query-dsl-match-query.md)

[Match boolean prefix](./query-dsl-match-bool-prefix-query.md)

[Match phrase](./query-dsl-match-query-phrase.md)

[Match phrase prefix](./query-dsl-match-query-phrase-prefix.md)

[Combined fields](./query-dsl-combined-fields-query.md)

[Multi-match](./query-dsl-multi-match-query.md)

[Query string](./query-dsl-query-string-query.md)

[Simple query string](./query-dsl-simple-query-string-query.md)

[Geo queries](./geo-queries.md)

[Geo-bounding box](./query-dsl-geo-bounding-box-query.md)

[Geo-distance](./query-dsl-geo-distance-query.md)

[Geo-grid](./query-dsl-geo-grid-query.md)

[Geo-polygon](./query-dsl-geo-polygon-query.md)

[Geoshape](./query-dsl-geo-shape-query.md)

[Shape queries](./shape-queries.md)

[Shape](./query-dsl-shape-query.md)

[Joining queries](./joining-queries.md)

[Nested](./query-dsl-nested-query.md)

[Has child](./query-dsl-has-child-query.md)

[Has parent](./query-dsl-has-parent-query.md)

[Parent ID](./query-dsl-parent-id-query.md)

[Match all](./query-dsl-match-all-query.md)

[Span queries](./span-queries.md)

[Span containing](./query-dsl-span-containing-query.md)

[Span field masking](./query-dsl-span-field-masking-query.md)

[Span first](./query-dsl-span-first-query.md)

[Span multi-term](./query-dsl-span-multi-term-query.md)

[Span near](./query-dsl-span-near-query.md)

[Span not](./query-dsl-span-not-query.md)

[Span or](./query-dsl-span-or-query.md)

[Span term](./query-dsl-span-term-query.md)

[Span within](./query-dsl-span-within-query.md)

[Specialized queries](./specialized-queries.md)

[Distance feature](./query-dsl-distance-feature-query.md)

[More like this](./query-dsl-mlt-query.md)

[Percolate](./query-dsl-percolate-query.md)

[Rank feature](./query-dsl-rank-feature-query.md)

[Script](./query-dsl-script-query.md)

[Script score](./query-dsl-script-score-query.md)

[Wrapper](./query-dsl-wrapper-query.md)

[Pinned Query](./query-dsl-pinned-query.md)

[Term-level queries](./term-level-queries.md)

[Exists](./query-dsl-exists-query.md)

[Fuzzy](./query-dsl-fuzzy-query.md)

[IDs](./query-dsl-ids-query.md)

[Prefix](./query-dsl-prefix-query.md)

[Range](./query-dsl-range-query.md)

[Regexp](./query-dsl-regexp-query.md)

[Term](./query-dsl-term-query.md)

[Terms](./query-dsl-terms-query.md)

[Terms set](./query-dsl-terms-set-query.md)

[Wildcard](./query-dsl-wildcard-query.md)

[Text expansion](./query-dsl-text-expansion-query.md)

[minimum_should_match parameter](./query-dsl-minimum-should-match.md)

[rewrite parameter](./query-dsl-multi-term-rewrite.md)

[Regular expression syntax](./regexp-syntax.md)

[Aggregations](./search-aggregations.md)

[Bucket aggregations](./search-aggregations-bucket.md)

[Adjacency matrix](./search-aggregations-bucket-adjacency-matrix-aggregation.md)

[Auto-interval date histogram](./search-aggregations-bucket-autodatehistogram-aggregation.md)

[Categorize text](./search-aggregations-bucket-categorize-text-aggregation.md)

[Children](./search-aggregations-bucket-children-aggregation.md)

[Composite](./search-aggregations-bucket-composite-aggregation.md)

[Date histogram](./search-aggregations-bucket-datehistogram-aggregation.md)

[Date range](./search-aggregations-bucket-daterange-aggregation.md)

[Diversified sampler](./search-aggregations-bucket-diversified-sampler-aggregation.md)

[Filter](./search-aggregations-bucket-filter-aggregation.md)

[Filters](./search-aggregations-bucket-filters-aggregation.md)

[Frequent item sets](./search-aggregations-bucket-frequent-item-sets-aggregation.md)

[Geo-distance](./search-aggregations-bucket-geodistance-aggregation.md)

[Geohash grid](./search-aggregations-bucket-geohashgrid-aggregation.md)

[Geohex grid](./search-aggregations-bucket-geohexgrid-aggregation.md)

[Geotile grid](./search-aggregations-bucket-geotilegrid-aggregation.md)

[Global](./search-aggregations-bucket-global-aggregation.md)

[Histogram](./search-aggregations-bucket-histogram-aggregation.md)

[IP prefix](./search-aggregations-bucket-ipprefix-aggregation.md)

[IP range](./search-aggregations-bucket-iprange-aggregation.md)

[Missing](./search-aggregations-bucket-missing-aggregation.md)

[Multi Terms](./search-aggregations-bucket-multi-terms-aggregation.md)

[Nested](./search-aggregations-bucket-nested-aggregation.md)

[Parent](./search-aggregations-bucket-parent-aggregation.md)

[Random sampler](./search-aggregations-random-sampler-aggregation.md)

[Range](./search-aggregations-bucket-range-aggregation.md)

[Rare terms](./search-aggregations-bucket-rare-terms-aggregation.md)

[Reverse nested](./search-aggregations-bucket-reverse-nested-aggregation.md)

[Sampler](./search-aggregations-bucket-sampler-aggregation.md)

[Significant terms](./search-aggregations-bucket-significantterms-aggregation.md)

[Significant text](./search-aggregations-bucket-significanttext-aggregation.md)

[Terms](./search-aggregations-bucket-terms-aggregation.md)

[Time series](./search-aggregations-bucket-time-series-aggregation.md)

[Variable width histogram](./search-aggregations-bucket-variablewidthhistogram-aggregation.md)

[Subtleties of bucketing range fields](./search-aggregations-bucket-range-field-note.md)

[Metrics aggregations](./search-aggregations-metrics.md)

[Avg](./search-aggregations-metrics-avg-aggregation.md)

[Boxplot](./search-aggregations-metrics-boxplot-aggregation.md)

[Cardinality](./search-aggregations-metrics-cardinality-aggregation.md)

[Extended stats](./search-aggregations-metrics-extendedstats-aggregation.md)

[Geo-bounds](./search-aggregations-metrics-geobounds-aggregation.md)

[Geo-centroid](./search-aggregations-metrics-geocentroid-aggregation.md)

[Geo-line](./search-aggregations-metrics-geo-line.md)

[Cartesian-bounds](./search-aggregations-metrics-cartesian-bounds-aggregation.md)

[Cartesian-centroid](./search-aggregations-metrics-cartesian-centroid-aggregation.md)

[Matrix stats](./search-aggregations-matrix-stats-aggregation.md)

[Max](./search-aggregations-metrics-max-aggregation.md)

[Median absolute deviation](./search-aggregations-metrics-median-absolute-deviation-aggregation.md)

[Min](./search-aggregations-metrics-min-aggregation.md)

[Percentile ranks](./search-aggregations-metrics-percentile-rank-aggregation.md)

[Percentiles](./search-aggregations-metrics-percentile-aggregation.md)

[Rate](./search-aggregations-metrics-rate-aggregation.md)

[Scripted metric](./search-aggregations-metrics-scripted-metric-aggregation.md)

[Stats](./search-aggregations-metrics-stats-aggregation.md)

[String stats](./search-aggregations-metrics-string-stats-aggregation.md)

[Sum](./search-aggregations-metrics-sum-aggregation.md)

[T-test](./search-aggregations-metrics-ttest-aggregation.md)

[Top hits](./search-aggregations-metrics-top-hits-aggregation.md)

[Top metrics](./search-aggregations-metrics-top-metrics.md)

[Value count](./search-aggregations-metrics-valuecount-aggregation.md)

[Weighted avg](./search-aggregations-metrics-weight-avg-aggregation.md)

[Pipeline aggregations](./search-aggregations-pipeline.md)

[Average bucket](./search-aggregations-pipeline-avg-bucket-aggregation.md)

[Bucket script](./search-aggregations-pipeline-bucket-script-aggregation.md)

[Bucket count K-S test](./search-aggregations-bucket-count-ks-test-aggregation.md)

[Bucket correlation](./search-aggregations-bucket-correlation-aggregation.md)

[Bucket selector](./search-aggregations-pipeline-bucket-selector-aggregation.md)

[Bucket sort](./search-aggregations-pipeline-bucket-sort-aggregation.md)

[Change point](./search-aggregations-change-point-aggregation.md)

[Cumulative cardinality](./search-aggregations-pipeline-cumulative-cardinality-aggregation.md)

[Cumulative sum](./search-aggregations-pipeline-cumulative-sum-aggregation.md)

[Derivative](./search-aggregations-pipeline-derivative-aggregation.md)

[Extended stats bucket](./search-aggregations-pipeline-extended-stats-bucket-aggregation.md)

[Inference bucket](./search-aggregations-pipeline-inference-bucket-aggregation.md)

[Max bucket](./search-aggregations-pipeline-max-bucket-aggregation.md)

[Min bucket](./search-aggregations-pipeline-min-bucket-aggregation.md)

[Moving function](./search-aggregations-pipeline-movfn-aggregation.md)

[Moving percentiles](./search-aggregations-pipeline-moving-percentiles-aggregation.md)

[Normalize](./search-aggregations-pipeline-normalize-aggregation.md)

[Percentiles bucket](./search-aggregations-pipeline-percentiles-bucket-aggregation.md)

[Serial differencing](./search-aggregations-pipeline-serialdiff-aggregation.md)

[Stats bucket](./search-aggregations-pipeline-stats-bucket-aggregation.md)

[Sum bucket](./search-aggregations-pipeline-sum-bucket-aggregation.md)

[Geospatial analysis](./geospatial-analysis.md)

[EQL](./eql.md)

[Syntax reference](./eql-syntax.md)

[Function reference](./eql-function-ref.md)

[Pipe reference](./eql-pipe-ref.md)

[Example: Detect threats with EQL](./eql-ex-threat-detection.md)

[SQL](./xpack-sql.md)

[Overview](./sql-overview.md)

[Getting Started with SQL](./sql-getting-started.md)

[Conventions and Terminology](./sql-concepts.md)

[Mapping concepts across SQL and Elasticsearch](./_mapping_concepts_across_sql_and_elasticsearch.md)

[Security](./sql-security.md)

[SQL REST API](./sql-rest.md)

[Overview](./sql-rest-overview.md)

[Response Data Formats](./sql-rest-format.md)

[Paginating through a large response](./sql-pagination.md)

[Filtering using Elasticsearch Query DSL](./sql-rest-filtering.md)

[Columnar results](./sql-rest-columnar.md)

[Passing parameters to a query](./sql-rest-params.md)

[Use runtime fields](./sql-runtime-fields.md)

[Run an async SQL search](./sql-async.md)

[SQL Translate API](./sql-translate.md)

[SQL CLI](./sql-cli.md)

[SQL JDBC](./sql-jdbc.md)

[API usage](./_api_usage.md)

[SQL ODBC](./sql-odbc.md)

[Driver installation](./sql-odbc-installation.md)

[Configuration](./sql-odbc-setup.md)

[SQL Client Applications](./sql-client-apps.md)

[DBeaver](./sql-client-apps-dbeaver.md)

[DbVisualizer](./sql-client-apps-dbvis.md)

[Microsoft Excel](./sql-client-apps-excel.md)

[Microsoft Power BI Desktop](./sql-client-apps-powerbi.md)

[Microsoft PowerShell](./sql-client-apps-ps1.md)

[MicroStrategy Desktop](./sql-client-apps-microstrat.md)

[Qlik Sense Desktop](./sql-client-apps-qlik.md)

[SQuirreL SQL](./sql-client-apps-squirrel.md)

[SQL Workbench/J](./sql-client-apps-workbench.md)

[Tableau Desktop](./sql-client-apps-tableau-desktop.md)

[Tableau Server](./sql-client-apps-tableau-server.md)

[SQL Language](./sql-spec.md)

[Lexical Structure](./sql-lexical-structure.md)

[SQL Commands](./sql-commands.md)

[DESCRIBE TABLE](./sql-syntax-describe-table.md)

[SELECT](./sql-syntax-select.md)

[SHOW CATALOGS](./sql-syntax-show-catalogs.md)

[SHOW COLUMNS](./sql-syntax-show-columns.md)

[SHOW FUNCTIONS](./sql-syntax-show-functions.md)

[SHOW TABLES](./sql-syntax-show-tables.md)

[Data Types](./sql-data-types.md)

[Index patterns](./sql-index-patterns.md)

[Frozen Indices](./sql-index-frozen.md)

[Functions and Operators](./sql-functions.md)

[Comparison Operators](./sql-operators.md)

[Logical Operators](./sql-operators-logical.md)

[Math Operators](./sql-operators-math.md)

[Cast Operators](./sql-operators-cast.md)

[LIKE and RLIKE Operators](./sql-like-rlike-operators.md)

[Aggregate Functions](./sql-functions-aggs.md)

[Grouping Functions](./sql-functions-grouping.md)

[Date/Time and Interval Functions and Operators](./sql-functions-datetime.md)

[Full-Text Search Functions](./sql-functions-search.md)

[Mathematical Functions](./sql-functions-math.md)

[String Functions](./sql-functions-string.md)

[Type Conversion Functions](./sql-functions-type-conversion.md)

[Geo Functions](./sql-functions-geo.md)

[Conditional Functions And Expressions](./sql-functions-conditional.md)

[System Functions](./sql-functions-system.md)

[Reserved keywords](./sql-syntax-reserved.md)

[SQL Limitations](./sql-limitations.md)

[Scripting](./modules-scripting.md)

[Painless scripting language](./modules-scripting-painless.md)

[How to write scripts](./modules-scripting-using.md)

[Scripts, caching, and search speed](./scripts-and-search-speed.md)

[Dissecting data](./dissect.md)

[Grokking grok](./grok.md)

[Access fields in a document](./script-fields-api.md)

[Common scripting use cases](./common-script-uses.md)

[Field extraction](./scripting-field-extraction.md)

[Accessing document fields and special variables](./modules-scripting-fields.md)

[Scripting and security](./modules-scripting-security.md)

[Lucene expressions language](./modules-scripting-expression.md)

[Advanced scripts using script engines](./modules-scripting-engine.md)

[Data management](./data-management.md)

[ILM: Manage the index lifecycle](./index-lifecycle-management.md)

[Tutorial: Customize built-in policies](./example-using-index-lifecycle-policy.md)

[Tutorial: Automate rollover](./getting-started-index-lifecycle-management.md)

[Index management in Kibana](./index-mgmt.md)

[Overview](./overview-index-lifecycle-management.md)

[Concepts](./ilm-concepts.md)

[Index lifecycle](./ilm-index-lifecycle.md)

[Rollover](./index-rollover.md)

[Policy updates](./update-lifecycle-policy.md)

[Index lifecycle actions](./ilm-actions.md)

[Allocate](./ilm-allocate.md)

[Delete](./ilm-delete.md)

[Force merge](./ilm-forcemerge.md)

[Migrate](./ilm-migrate.md)

[Read only](./ilm-readonly.md)

[Rollover](./ilm-rollover.md)

[Downsample](./ilm-downsample.md)

[Searchable snapshot](./ilm-searchable-snapshot.md)

[Set priority](./ilm-set-priority.md)

[Shrink](./ilm-shrink.md)

[Unfollow](./ilm-unfollow.md)

[Wait for snapshot](./ilm-wait-for-snapshot.md)

[Configure a lifecycle policy](./set-up-lifecycle-policy.md)

[Migrate index allocation filters to node roles](./migrate-index-allocation-filters.md)

[Troubleshooting index lifecycle management errors](./index-lifecycle-error-handling.md)

[Start and stop index lifecycle management](./start-stop-ilm.md)

[Manage existing indices](./ilm-with-existing-indices.md)

[Skip rollover](./skipping-rollover.md)

[Restore a managed data stream or index](./index-lifecycle-and-snapshots.md)

[Data tiers](./data-tiers.md)

[Autoscaling](./xpack-autoscaling.md)

[Autoscaling deciders](./autoscaling-deciders.md)

[Reactive storage decider](./autoscaling-reactive-storage-decider.md)

[Proactive storage decider](./autoscaling-proactive-storage-decider.md)

[Frozen shards decider](./autoscaling-frozen-shards-decider.md)

[Frozen storage decider](./autoscaling-frozen-storage-decider.md)

[Frozen existence decider](./autoscaling-frozen-existence-decider.md)

[Machine learning decider](./autoscaling-machine-learning-decider.md)

[Fixed decider](./autoscaling-fixed-decider.md)

[Monitor a cluster](./monitor-elasticsearch-cluster.md)

[Overview](./monitoring-overview.md)

[How it works](./how-monitoring-works.md)

[Monitoring in a production environment](./monitoring-production.md)

[Collecting monitoring data with Elastic Agent](./configuring-elastic-agent.md)

[Collecting monitoring data with Metricbeat](./configuring-metricbeat.md)

[Collecting log data with Filebeat](./configuring-filebeat.md)

[Configuring data streams/indices for monitoring](./config-monitoring-indices.md)

[Configuring data streams created by Elastic Agent](./config-monitoring-data-streams-elastic-agent.md)

[Configuring data streams created by Metricbeat 8](./config-monitoring-data-streams-metricbeat-8.md)

[Configuring indices created by Metricbeat 7 or internal collection](./config-monitoring-indices-metricbeat-7-internal-collection.md)

[Legacy collection methods](./collecting-monitoring-data.md)

[Collectors](./es-monitoring-collectors.md)

[Exporters](./es-monitoring-exporters.md)

[Local exporters](./local-exporter.md)

[HTTP exporters](./http-exporter.md)

[Pausing data collection](./pause-export.md)

[Roll up or transform your data](./data-rollup-transform.md)

[Rolling up historical data](./xpack-rollup.md)

[Overview](./rollup-overview.md)

[API quick reference](./rollup-api-quickref.md)

[Getting started](./rollup-getting-started.md)

[Understanding groups](./rollup-understanding-groups.md)

[Rollup aggregation limitations](./rollup-agg-limitations.md)

[Rollup search limitations](./rollup-search-limitations.md)

[Transforming data](./transforms.md)

[Overview](./transform-overview.md)

[Setup](./transform-setup.md)

[When to use transforms](./transform-usage.md)

[Generating alerts for transforms](./transform-alerts.md)

[Transforms at scale](./transform-scale.md)

[How checkpoints work](./transform-checkpoints.md)

[API quick reference](./transform-api-quickref.md)

[Tutorial: Transforming the eCommerce sample data](./ecommerce-transforms.md)

[Examples](./transform-examples.md)

[Painless examples](./transform-painless-examples.md)

[Limitations](./transform-limitations.md)

[Set up a cluster for high availability](./high-availability.md)

[Designing for resilience](./high-availability-cluster-design.md)

[Resilience in small clusters](./high-availability-cluster-small-clusters.md)

[Resilience in larger clusters](./high-availability-cluster-design-large-clusters.md)

[Cross-cluster replication](./xpack-ccr.md)

[Set up cross-cluster replication](./ccr-getting-started-tutorial.md)

[Manage cross-cluster replication](./ccr-managing.md)

[Manage auto-follow patterns](./ccr-auto-follow.md)

[Upgrading clusters](./ccr-upgrading.md)

[Uni-directional disaster recovery](./ccr-disaster-recovery-uni-directional-tutorial.md)

[Bi-directional disaster recovery](./ccr-disaster-recovery-bi-directional-tutorial.md)

[Snapshot and restore](./snapshot-restore.md)

[Register a repository](./snapshots-register-repository.md)

[Azure repository](./repository-azure.md)

[Google Cloud Storage repository](./repository-gcs.md)

[S3 repository](./repository-s3.md)

[Shared file system repository](./snapshots-filesystem-repository.md)

[Read-only URL repository](./snapshots-read-only-repository.md)

[Source-only repository](./snapshots-source-only-repository.md)

[Create a snapshot](./snapshots-take-snapshot.md)

[Restore a snapshot](./snapshots-restore-snapshot.md)

[Searchable snapshots](./searchable-snapshots.md)

[Secure the Elastic Stack](./secure-cluster.md)

[Elasticsearch security principles](./es-security-principles.md)

[Start the Elastic Stack with security enabled automatically](./configuring-stack-security.md)

[Manually configure security](./manually-configure-security.md)

[Set up minimal security](./security-minimal-setup.md)

[Set up basic security](./security-basic-setup.md)

[Set up basic security plus HTTPS](./security-basic-setup-https.md)

[Setting passwords for native and built-in users](./change-passwords-native-users.md)

[Enabling cipher suites for stronger encryption](./ciphers.md)

[Supported SSL/TLS versions by JDK version](./jdk-tls-versions.md)

[Security files](./security-files.md)

[FIPS 140-2](./fips-140-compliance.md)

[Updating node security certificates](./update-node-certs.md)

[With the same CA](./update-node-certs-same.md)

[With a different CA](./update-node-certs-different.md)

[User authentication](./setting-up-authentication.md)

[Built-in users](./built-in-users.md)

[Service accounts](./service-accounts.md)

[Internal users](./internal-users.md)

[Token-based authentication services](./token-authentication-services.md)

[User profiles](./user-profile.md)

[Realms](./realms.md)

[Realm chains](./realm-chains.md)

[Security domains](./security-domain.md)

[Active Directory user authentication](./active-directory-realm.md)

[File-based user authentication](./file-realm.md)

[LDAP user authentication](./ldap-realm.md)

[Native user authentication](./native-realm.md)

[OpenID Connect authentication](./oidc-realm.md)

[PKI user authentication](./pki-realm.md)

[SAML authentication](./saml-realm.md)

[Kerberos authentication](./kerberos-realm.md)

[JWT authentication](./jwt-auth-realm.md)

[Integrating with other authentication systems](./custom-realms.md)

[Enabling anonymous access](./anonymous-access.md)

[Looking up users without authentication](./user-lookup.md)

[Controlling the user cache](./controlling-user-cache.md)

[Configuring SAML single-sign-on on the Elastic Stack](./saml-guide-stack.md)

[Configuring single sign-on to the Elastic Stack using OpenID Connect](./oidc-guide.md)

[User authorization](./authorization.md)

[Built-in roles](./built-in-roles.md)

[Defining roles](./defining-roles.md)

[Role restriction](./role-restriction.md)

[Security privileges](./security-privileges.md)

[Document level security](./document-level-security.md)

[Field level security](./field-level-security.md)

[Granting privileges for data streams and aliases](./securing-aliases.md)

[Mapping users and groups to roles](./mapping-roles.md)

[Setting up field and document level security](./field-and-document-access-control.md)

[Submitting requests on behalf of other users](./run-as-privilege.md)

[Configuring authorization delegation](./configuring-authorization-delegation.md)

[Customizing roles and authorization](./custom-roles-authorization.md)

[Enable audit logging](./enable-audit-logging.md)

[Audit events](./audit-event-types.md)

[Logfile audit output](./audit-log-output.md)

[Logfile audit events ignore policies](./audit-log-ignore-policy.md)

[Auditing search queries](./auditing-search-queries.md)

[Restricting connections with IP filtering](./ip-filtering.md)

[Securing clients and integrations](./security-clients-integrations.md)

[HTTP/REST clients and security](./http-clients.md)

[ES-Hadoop and Security](./hadoop.md)

[Monitoring and security](./secure-monitoring.md)

[Operator privileges](./operator-privileges.md)

[Configure operator privileges](./configure-operator-privileges.md)

[Operator-only functionality](./operator-only-functionality.md)

[Operator privileges for snapshot and restore](./operator-only-snapshot-and-restore.md)

[Troubleshooting](./security-troubleshooting.md)

[Some settings are not returned via the nodes settings API](./security-trb-settings.md)

[Authorization exceptions](./security-trb-roles.md)

[Users command fails due to extra arguments](./security-trb-extraargs.md)

[Users are frequently locked out of Active Directory](./trouble-shoot-active-directory.md)

[Certificate verification fails for curl on Mac](./trb-security-maccurl.md)

[SSLHandshakeException causes connections to fail](./trb-security-sslhandshake.md)

[Common SSL/TLS exceptions](./trb-security-ssl.md)

[Common Kerberos exceptions](./trb-security-kerberos.md)

[Common SAML issues](./trb-security-saml.md)

[Internal Server Error in Kibana](./trb-security-internalserver.md)

[Setup-passwords command fails due to connection failure](./trb-security-setup.md)

[Failures due to relocation of the configuration files](./trb-security-path.md)

[Limitations](./security-limitations.md)

[Watcher](./xpack-alerting.md)

[Getting started with Watcher](./watcher-getting-started.md)

[How Watcher works](./how-watcher-works.md)

[Encrypting sensitive data in Watcher](./encrypting-data.md)

[Inputs](./input.md)

[Simple input](./input-simple.md)

[Search input](./input-search.md)

[HTTP input](./input-http.md)

[Chain input](./input-chain.md)

[Triggers](./trigger.md)

[Schedule trigger](./trigger-schedule.md)

[Conditions](./condition.md)

[Always condition](./condition-always.md)

[Never condition](./condition-never.md)

[Compare condition](./condition-compare.md)

[Array compare condition](./condition-array-compare.md)

[Script condition](./condition-script.md)

[Actions](./actions.md)

[Running an action for each element in an array](./action-foreach.md)

[Adding conditions to actions](./action-conditions.md)

[Email action](./actions-email.md)

[Webhook action](./actions-webhook.md)

[Index action](./actions-index.md)

[Logging action](./actions-logging.md)

[Slack action](./actions-slack.md)

[PagerDuty action](./actions-pagerduty.md)

[Jira action](./actions-jira.md)

[Transforms](./transform.md)

[Search payload transform](./transform-search.md)

[Script payload transform](./transform-script.md)

[Chain payload transform](./transform-chain.md)

[Managing watches](./managing-watches.md)

[Example watches](./example-watches.md)

[Watching the status of an Elasticsearch cluster](./watch-cluster-status.md)

[Limitations](./watcher-limitations.md)

[Command line tools](./commands.md)

[elasticsearch-certgen](./certgen.md)

[elasticsearch-certutil](./certutil.md)

[elasticsearch-create-enrollment-token](./create-enrollment-token.md)

[elasticsearch-croneval](./elasticsearch-croneval.md)

[elasticsearch-keystore](./elasticsearch-keystore.md)

[elasticsearch-node](./node-tool.md)

[elasticsearch-reconfigure-node](./reconfigure-node.md)

[elasticsearch-reset-password](./reset-password.md)

[elasticsearch-saml-metadata](./saml-metadata.md)

[elasticsearch-service-tokens](./service-tokens-command.md)

[elasticsearch-setup-passwords](./setup-passwords.md)

[elasticsearch-shard](./shard-tool.md)

[elasticsearch-syskeygen](./syskeygen.md)

[elasticsearch-users](./users-command.md)

[How to](./how-to.md)

[General recommendations](./general-recommendations.md)

[Recipes](./recipes.md)

[Mixing exact search with stemming](./mixing-exact-search-with-stemming.md)

[Getting consistent scoring](./consistent-scoring.md)

[Incorporating static relevance signals into the score](./static-scoring-signals.md)

[Tune for indexing speed](./tune-for-indexing-speed.md)

[Tune for search speed](./tune-for-search-speed.md)

[Tune approximate kNN search](./tune-knn-search.md)

[Tune for disk usage](./tune-for-disk-usage.md)

[Size your shards](./size-your-shards.md)

[Use Elasticsearch for time series data](./use-elasticsearch-for-time-series-data.md)

[Troubleshooting](./troubleshooting.md)

[Fix common cluster issues](./fix-common-cluster-issues.md)

[Watermark errors](./fix-watermark-errors.md)

[Circuit breaker errors](./circuit-breaker-errors.md)

[High CPU usage](./high-cpu-usage.md)

[High JVM memory pressure](./high-jvm-memory-pressure.md)

[Red or yellow cluster status](./red-yellow-cluster-status.md)

[Rejected requests](./rejected-requests.md)

[Task queue backlog](./task-queue-backlog.md)

[Mapping explosion](./mapping-explosion.md)

[Hot spotting](./hotspotting.md)

[Diagnose unassigned shards](./diagnose-unassigned-shards.md)

[Add a missing tier to the system](./add-tier.md)

[Allow Elasticsearch to allocate the data in the system](./allow-all-cluster-allocation.md)

[Allow Elasticsearch to allocate the index](./allow-all-index-allocation.md)

[Indices mix index allocation filters with data tiers node roles to move through data tiers](./troubleshoot-migrate-to-tiers.md)

[Not enough nodes to allocate all shard replicas](./increase-tier-capacity.md)

[Total number of shards for an index on a single node exceeded](./increase-shard-limit.md)

[Total number of shards per node has been reached](./increase-cluster-shard-limit.md)

[Troubleshooting corruption](./corruption-troubleshooting.md)

[Fix data nodes out of disk](./fix-data-node-out-of-disk.md)

[Increase the disk capacity of data nodes](./increase-capacity-data-node.md)

[Decrease the disk usage of data nodes](./decrease-disk-usage-data-node.md)

[Fix master nodes out of disk](./fix-master-node-out-of-disk.md)

[Fix other role nodes out of disk](./fix-other-node-out-of-disk.md)

[Start index lifecycle management](./start-ilm.md)

[Start Snapshot Lifecycle Management](./start-slm.md)

[Restore from snapshot](./restore-from-snapshot.md)

[Multiple deployments writing to the same snapshot repository](./add-repository.md)

[Addressing repeated snapshot policy failures](./repeated-snapshot-failures.md)

[Troubleshooting discovery](./discovery-troubleshooting.md)

[Troubleshooting monitoring](./monitoring-troubleshooting.md)

[Troubleshooting transforms](./transform-troubleshooting.md)

[Troubleshooting Watcher](./watcher-troubleshooting.md)

[Troubleshooting searches](./troubleshooting-searches.md)

[Troubleshooting shards capacity health issues](./troubleshooting-shards-capacity-issues.md)

[REST APIs](./rest-apis.md)

[API conventions](./api-conventions.md)

[Common options](./common-options.md)

[REST API compatibility](./rest-api-compatibility.md)

[Autoscaling APIs](./autoscaling-apis.md)

[Create or update autoscaling policy](./autoscaling-put-autoscaling-policy.md)

[Get autoscaling capacity](./autoscaling-get-autoscaling-capacity.md)

[Delete autoscaling policy](./autoscaling-delete-autoscaling-policy.md)

[Get autoscaling policy](./autoscaling-get-autoscaling-policy.md)

[Behavioral Analytics APIs](./behavioral-analytics-apis.md)

[Put Analytics Collection](./put-analytics-collection.md)

[Delete Analytics Collection](./delete-analytics-collection.md)

[List Analytics Collections](./list-analytics-collection.md)

[Post Analytics Collection Event](./post-analytics-collection-event.md)

[Compact and aligned text (CAT) APIs](./cat.md)

[cat aliases](./cat-alias.md)

[cat allocation](./cat-allocation.md)

[cat anomaly detectors](./cat-anomaly-detectors.md)

[cat component templates](./cat-component-templates.md)

[cat count](./cat-count.md)

[cat data frame analytics](./cat-dfanalytics.md)

[cat datafeeds](./cat-datafeeds.md)

[cat fielddata](./cat-fielddata.md)

[cat health](./cat-health.md)

[cat indices](./cat-indices.md)

[cat master](./cat-master.md)

[cat nodeattrs](./cat-nodeattrs.md)

[cat nodes](./cat-nodes.md)

[cat pending tasks](./cat-pending-tasks.md)

[cat plugins](./cat-plugins.md)

[cat recovery](./cat-recovery.md)

[cat repositories](./cat-repositories.md)

[cat segments](./cat-segments.md)

[cat shards](./cat-shards.md)

[cat snapshots](./cat-snapshots.md)

[cat task management](./cat-tasks.md)

[cat templates](./cat-templates.md)

[cat thread pool](./cat-thread-pool.md)

[cat trained model](./cat-trained-model.md)

[cat transforms](./cat-transforms.md)

[Cluster APIs](./cluster.md)

[Cluster allocation explain](./cluster-allocation-explain.md)

[Cluster get settings](./cluster-get-settings.md)

[Cluster health](./cluster-health.md)

[Health](./health-api.md)

[Cluster reroute](./cluster-reroute.md)

[Cluster state](./cluster-state.md)

[Cluster stats](./cluster-stats.md)

[Cluster update settings](./cluster-update-settings.md)

[Nodes feature usage](./cluster-nodes-usage.md)

[Nodes hot threads](./cluster-nodes-hot-threads.md)

[Nodes info](./cluster-nodes-info.md)

[Prevalidate node removal](./prevalidate-node-removal-api.md)

[Nodes reload secure settings](./cluster-nodes-reload-secure-settings.md)

[Nodes stats](./cluster-nodes-stats.md)

[Cluster Info](./cluster-info.md)

[Pending cluster tasks](./cluster-pending.md)

[Remote cluster info](./cluster-remote-info.md)

[Task management](./tasks.md)

[Voting configuration exclusions](./voting-config-exclusions.md)

[Create or update desired nodes](./update-desired-nodes.md)

[Get desired nodes](./get-desired-nodes.md)

[Delete desired nodes](./delete-desired-nodes.md)

[Get desired balance](./get-desired-balance.md)

[Delete/reset desired balance](./delete-desired-balance.md)

[Cross-cluster replication APIs](./ccr-apis.md)

[Get CCR stats](./ccr-get-stats.md)

[Create follower](./ccr-put-follow.md)

[Pause follower](./ccr-post-pause-follow.md)

[Resume follower](./ccr-post-resume-follow.md)

[Unfollow](./ccr-post-unfollow.md)

[Forget follower](./ccr-post-forget-follower.md)

[Get follower stats](./ccr-get-follow-stats.md)

[Get follower info](./ccr-get-follow-info.md)

[Create auto-follow pattern](./ccr-put-auto-follow-pattern.md)

[Delete auto-follow pattern](./ccr-delete-auto-follow-pattern.md)

[Get auto-follow pattern](./ccr-get-auto-follow-pattern.md)

[Pause auto-follow pattern](./ccr-pause-auto-follow-pattern.md)

[Resume auto-follow pattern](./ccr-resume-auto-follow-pattern.md)

[Data stream APIs](./data-stream-apis.md)

[Create data stream](./indices-create-data-stream.md)

[Delete data stream](./indices-delete-data-stream.md)

[Get data stream](./indices-get-data-stream.md)

[Migrate to data stream](./indices-migrate-to-data-stream.md)

[Data stream stats](./data-stream-stats-api.md)

[Promote data stream](./promote-data-stream-api.md)

[Modify data streams](./modify-data-streams-api.md)

[Downsample](./indices-downsample-data-stream.md)

[Document APIs](./docs.md)

[Reading and Writing documents](./docs-replication.md)

[Index](./docs-index_.md)

[Get](./docs-get.md)

[Delete](./docs-delete.md)

[Delete by query](./docs-delete-by-query.md)

[Update](./docs-update.md)

[Update by query](./docs-update-by-query.md)

[Multi get](./docs-multi-get.md)

[Bulk](./docs-bulk.md)

[Reindex](./docs-reindex.md)

[Term vectors](./docs-termvectors.md)

[Multi term vectors](./docs-multi-termvectors.md)

[?refresh](./docs-refresh.md)

[Optimistic concurrency control](./optimistic-concurrency-control.md)

[Enrich APIs](./enrich-apis.md)

[Create enrich policy](./put-enrich-policy-api.md)

[Delete enrich policy](./delete-enrich-policy-api.md)

[Get enrich policy](./get-enrich-policy-api.md)

[Execute enrich policy](./execute-enrich-policy-api.md)

[Enrich stats](./enrich-stats-api.md)

[EQL APIs](./eql-apis.md)

[Delete async EQL search](./delete-async-eql-search-api.md)

[EQL search](./eql-search-api.md)

[Get async EQL search](./get-async-eql-search-api.md)

[Get async EQL search status](./get-async-eql-status-api.md)

[Features APIs](./features-apis.md)

[Get features](./get-features-api.md)

[Reset features](./reset-features-api.md)

[Fleet APIs](./fleet-apis.md)

[Get global checkpoints](./get-global-checkpoints.md)

[Fleet search](./fleet-search.md)

[Fleet search](./fleet-multi-search.md)

[Find structure API](./find-structure.md)

[Graph explore API](./graph-explore-api.md)

[Index APIs](./indices.md)

[Alias exists](./indices-alias-exists.md)

[Aliases](./indices-aliases.md)

[Analyze](./indices-analyze.md)

[Analyze index disk usage](./indices-disk-usage.md)

[Clear cache](./indices-clearcache.md)

[Clone index](./indices-clone-index.md)

[Close index](./indices-close.md)

[Create index](./indices-create-index.md)

[Create or update alias](./indices-add-alias.md)

[Create or update component template](./indices-component-template.md)

[Create or update index template](./indices-put-template.md)

[Create or update index template (legacy)](./indices-templates-v1.md)

[Delete component template](./indices-delete-component-template.md)

[Delete dangling index](./dangling-index-delete.md)

[Delete alias](./indices-delete-alias.md)

[Delete index](./indices-delete-index.md)

[Delete index template](./indices-delete-template.md)

[Delete index template (legacy)](./indices-delete-template-v1.md)

[Exists](./indices-exists.md)

[Field usage stats](./field-usage-stats.md)

[Flush](./indices-flush.md)

[Force merge](./indices-forcemerge.md)

[Get alias](./indices-get-alias.md)

[Get component template](./getting-component-templates.md)

[Get field mapping](./indices-get-field-mapping.md)

[Get index](./indices-get-index.md)

[Get index settings](./indices-get-settings.md)

[Get index template](./indices-get-template.md)

[Get index template (legacy)](./indices-get-template-v1.md)

[Get mapping](./indices-get-mapping.md)

[Import dangling index](./dangling-index-import.md)

[Index recovery](./indices-recovery.md)

[Index segments](./indices-segments.md)

[Index shard stores](./indices-shards-stores.md)

[Index stats](./indices-stats.md)

[Index template exists (legacy)](./indices-template-exists-v1.md)

[List dangling indices](./dangling-indices-list.md)

[Open index](./indices-open-close.md)

[Refresh](./indices-refresh.md)

[Resolve index](./indices-resolve-index-api.md)

[Rollover](./indices-rollover-index.md)

[Shrink index](./indices-shrink-index.md)

[Simulate index](./indices-simulate-index.md)

[Simulate template](./indices-simulate-template.md)

[Split index](./indices-split-index.md)

[Unfreeze index](./unfreeze-index-api.md)

[Update index settings](./indices-update-settings.md)

[Update mapping](./indices-put-mapping.md)

[Index lifecycle management APIs](./index-lifecycle-management-api.md)

[Create or update lifecycle policy](./ilm-put-lifecycle.md)

[Get policy](./ilm-get-lifecycle.md)

[Delete policy](./ilm-delete-lifecycle.md)

[Move to step](./ilm-move-to-step.md)

[Remove policy](./ilm-remove-policy.md)

[Retry policy](./ilm-retry-policy.md)

[Get index lifecycle management status](./ilm-get-status.md)

[Explain lifecycle](./ilm-explain-lifecycle.md)

[Start index lifecycle management](./ilm-start.md)

[Stop index lifecycle management](./ilm-stop.md)

[Migrate indices, ILM policies, and legacy, composable and component templates to data tiers routing](./ilm-migrate-to-data-tiers.md)

[Ingest APIs](./ingest-apis.md)

[Create or update pipeline](./put-pipeline-api.md)

[Delete pipeline](./delete-pipeline-api.md)

[GeoIP stats](./geoip-stats-api.md)

[Get pipeline](./get-pipeline-api.md)

[Simulate pipeline](./simulate-pipeline-api.md)

[Info API](./info-api.md)

[Licensing APIs](./licensing-apis.md)

[Delete license](./delete-license.md)

[Get license](./get-license.md)

[Get trial status](./get-trial-status.md)

[Start trial](./start-trial.md)

[Get basic status](./get-basic-status.md)

[Start basic](./start-basic.md)

[Update license](./update-license.md)

[Logstash APIs](./logstash-apis.md)

[Create or update Logstash pipeline](./logstash-api-put-pipeline.md)

[Delete Logstash pipeline](./logstash-api-delete-pipeline.md)

[Get Logstash pipeline](./logstash-api-get-pipeline.md)

[Machine learning APIs](./ml-apis.md)

[Get machine learning info](./get-ml-info.md)

[Get machine learning memory stats](./get-ml-memory.md)

[Set upgrade mode](./ml-set-upgrade-mode.md)

[Machine learning anomaly detection APIs](./ml-ad-apis.md)

[Add events to calendar](./ml-post-calendar-event.md)

[Add jobs to calendar](./ml-put-calendar-job.md)

[Close jobs](./ml-close-job.md)

[Create jobs](./ml-put-job.md)

[Create calendars](./ml-put-calendar.md)

[Create datafeeds](./ml-put-datafeed.md)

[Create filters](./ml-put-filter.md)

[Delete calendars](./ml-delete-calendar.md)

[Delete datafeeds](./ml-delete-datafeed.md)

[Delete events from calendar](./ml-delete-calendar-event.md)

[Delete filters](./ml-delete-filter.md)

[Delete forecasts](./ml-delete-forecast.md)

[Delete jobs](./ml-delete-job.md)

[Delete jobs from calendar](./ml-delete-calendar-job.md)

[Delete model snapshots](./ml-delete-snapshot.md)

[Delete expired data](./ml-delete-expired-data.md)

[Estimate model memory](./ml-estimate-model-memory.md)

[Flush jobs](./ml-flush-job.md)

[Forecast jobs](./ml-forecast.md)

[Get buckets](./ml-get-bucket.md)

[Get calendars](./ml-get-calendar.md)

[Get categories](./ml-get-category.md)

[Get datafeeds](./ml-get-datafeed.md)

[Get datafeed statistics](./ml-get-datafeed-stats.md)

[Get influencers](./ml-get-influencer.md)

[Get jobs](./ml-get-job.md)

[Get job statistics](./ml-get-job-stats.md)

[Get model snapshots](./ml-get-snapshot.md)

[Get model snapshot upgrade statistics](./ml-get-job-model-snapshot-upgrade-stats.md)

[Get overall buckets](./ml-get-overall-buckets.md)

[Get scheduled events](./ml-get-calendar-event.md)

[Get filters](./ml-get-filter.md)

[Get records](./ml-get-record.md)

[Open jobs](./ml-open-job.md)

[Post data to jobs](./ml-post-data.md)

[Preview datafeeds](./ml-preview-datafeed.md)

[Reset jobs](./ml-reset-job.md)

[Revert model snapshots](./ml-revert-snapshot.md)

[Start datafeeds](./ml-start-datafeed.md)

[Stop datafeeds](./ml-stop-datafeed.md)

[Update datafeeds](./ml-update-datafeed.md)

[Update filters](./ml-update-filter.md)

[Update jobs](./ml-update-job.md)

[Update model snapshots](./ml-update-snapshot.md)

[Upgrade model snapshots](./ml-upgrade-job-model-snapshot.md)

[Machine learning data frame analytics APIs](./ml-df-analytics-apis.md)

[Create data frame analytics jobs](./put-dfanalytics.md)

[Delete data frame analytics jobs](./delete-dfanalytics.md)

[Evaluate data frame analytics](./evaluate-dfanalytics.md)

[Explain data frame analytics](./explain-dfanalytics.md)

[Get data frame analytics jobs](./get-dfanalytics.md)

[Get data frame analytics jobs stats](./get-dfanalytics-stats.md)

[Preview data frame analytics](./preview-dfanalytics.md)

[Start data frame analytics jobs](./start-dfanalytics.md)

[Stop data frame analytics jobs](./stop-dfanalytics.md)

[Update data frame analytics jobs](./update-dfanalytics.md)

[Machine learning trained model APIs](./ml-df-trained-models-apis.md)

[Clear trained model deployment cache](./clear-trained-model-deployment-cache.md)

[Create or update trained model aliases](./put-trained-models-aliases.md)

[Create part of a trained model](./put-trained-model-definition-part.md)

[Create trained models](./put-trained-models.md)

[Create trained model vocabulary](./put-trained-model-vocabulary.md)

[Delete trained model aliases](./delete-trained-models-aliases.md)

[Delete trained models](./delete-trained-models.md)

[Get trained models](./get-trained-models.md)

[Get trained models stats](./get-trained-models-stats.md)

[Infer trained model](./infer-trained-model.md)

[Start trained model deployment](./start-trained-model-deployment.md)

[Stop trained model deployment](./stop-trained-model-deployment.md)

[Update trained model deployment](./update-trained-model-deployment.md)

[Migration APIs](./migration-api.md)

[Deprecation info](./migration-api-deprecation.md)

[Feature migration](./feature-migration-api.md)

[Node lifecycle APIs](./node-lifecycle-api.md)

[Put shutdown API](./put-shutdown.md)

[Get shutdown API](./get-shutdown.md)

[Delete shutdown API](./delete-shutdown.md)

[Reload search analyzers API](./indices-reload-analyzers.md)

[Repositories metering APIs](./repositories-metering-apis.md)

[Get repositories metering information](./get-repositories-metering-api.md)

[Clear repositories metering archive](./clear-repositories-metering-archive-api.md)

[Rollup APIs](./rollup-apis.md)

[Create rollup jobs](./rollup-put-job.md)

[Delete rollup jobs](./rollup-delete-job.md)

[Get job](./rollup-get-job.md)

[Get rollup caps](./rollup-get-rollup-caps.md)

[Get rollup index caps](./rollup-get-rollup-index-caps.md)

[Rollup search](./rollup-search.md)

[Start rollup jobs](./rollup-start-job.md)

[Stop rollup jobs](./rollup-stop-job.md)

[Script APIs](./script-apis.md)

[Create or update stored script](./create-stored-script-api.md)

[Delete stored script](./delete-stored-script-api.md)

[Get script contexts](./get-script-contexts-api.md)

[Get script languages](./get-script-languages-api.md)

[Get stored script](./get-stored-script-api.md)

[Search APIs](./search.md)

[Search](./search-search.md)

[Async search](./async-search.md)

[Point in time](./point-in-time-api.md)

[kNN search](./knn-search-api.md)

[Reciprocal rank fusion](./rrf.md)

[Scroll](./scroll-api.md)

[Clear scroll](./clear-scroll-api.md)

[Search template](./search-template-api.md)

[Multi search template](./multi-search-template.md)

[Render search template](./render-search-template-api.md)

[Search shards](./search-shards.md)

[Suggesters](./search-suggesters.md)

[Multi search](./search-multi-search.md)

[Count](./search-count.md)

[Validate](./search-validate.md)

[Terms enum](./search-terms-enum.md)

[Explain](./search-explain.md)

[Profile](./search-profile.md)

[Field capabilities](./search-field-caps.md)

[Ranking evaluation](./search-rank-eval.md)

[Vector tile search](./search-vector-tile-api.md)

[Search Application APIs](./search-application-apis.md)

[Put Search Application](./put-search-application.md)

[Get Search Application](./get-search-application.md)

[List Search Applications](./list-search-applications.md)

[Delete Search Application](./delete-search-application.md)

[Search Application Search](./search-application-search.md)

[Render Search Application Query](./search-application-render-query.md)

[Searchable snapshots APIs](./searchable-snapshots-apis.md)

[Mount snapshot](./searchable-snapshots-api-mount-snapshot.md)

[Cache stats](./searchable-snapshots-api-cache-stats.md)

[Searchable snapshot statistics](./searchable-snapshots-api-stats.md)

[Clear cache](./searchable-snapshots-api-clear-cache.md)

[Security APIs](./security-api.md)

[Authenticate](./security-api-authenticate.md)

[Change passwords](./security-api-change-password.md)

[Clear cache](./security-api-clear-cache.md)

[Clear roles cache](./security-api-clear-role-cache.md)

[Clear privileges cache](./security-api-clear-privilege-cache.md)

[Clear API key cache](./security-api-clear-api-key-cache.md)

[Clear service account token caches](./security-api-clear-service-token-caches.md)

[Create API keys](./security-api-create-api-key.md)

[Create or update application privileges](./security-api-put-privileges.md)

[Create or update role mappings](./security-api-put-role-mapping.md)

[Create or update roles](./security-api-put-role.md)

[Create or update users](./security-api-put-user.md)

[Create service account tokens](./security-api-create-service-token.md)

[Delegate PKI authentication](./security-api-delegate-pki-authentication.md)

[Delete application privileges](./security-api-delete-privilege.md)

[Delete role mappings](./security-api-delete-role-mapping.md)

[Delete roles](./security-api-delete-role.md)

[Delete service account token](./security-api-delete-service-token.md)

[Delete users](./security-api-delete-user.md)

[Disable users](./security-api-disable-user.md)

[Enable users](./security-api-enable-user.md)

[Enroll Kibana](./security-api-kibana-enrollment.md)

[Enroll node](./security-api-node-enrollment.md)

[Get API key information](./security-api-get-api-key.md)

[Get application privileges](./security-api-get-privileges.md)

[Get builtin privileges](./security-api-get-builtin-privileges.md)

[Get role mappings](./security-api-get-role-mapping.md)

[Get roles](./security-api-get-role.md)

[Get service accounts](./security-api-get-service-accounts.md)

[Get service account credentials](./security-api-get-service-credentials.md)

[Get token](./security-api-get-token.md)

[Get user privileges](./security-api-get-user-privileges.md)

[Get users](./security-api-get-user.md)

[Grant API keys](./security-api-grant-api-key.md)

[Has privileges](./security-api-has-privileges.md)

[Invalidate API key](./security-api-invalidate-api-key.md)

[Invalidate token](./security-api-invalidate-token.md)

[OpenID Connect prepare authentication](./security-api-oidc-prepare-authentication.md)

[OpenID Connect authenticate](./security-api-oidc-authenticate.md)

[OpenID Connect logout](./security-api-oidc-logout.md)

[Query API key information](./security-api-query-api-key.md)

[Update API key](./security-api-update-api-key.md)

[Bulk update API keys](./security-api-bulk-update-api-keys.md)

[SAML prepare authentication](./security-api-saml-prepare-authentication.md)

[SAML authenticate](./security-api-saml-authenticate.md)

[SAML logout](./security-api-saml-logout.md)

[SAML invalidate](./security-api-saml-invalidate.md)

[SAML complete logout](./security-api-saml-complete-logout.md)

[SAML service provider metadata](./security-api-saml-sp-metadata.md)

[SSL certificate](./security-api-ssl.md)

[Activate user profile](./security-api-activate-user-profile.md)

[Disable user profile](./security-api-disable-user-profile.md)

[Enable user profile](./security-api-enable-user-profile.md)

[Get user profiles](./security-api-get-user-profile.md)

[Suggest user profile](./security-api-suggest-user-profile.md)

[Update user profile data](./security-api-update-user-profile-data.md)

[Has privileges user profile](./security-api-has-privileges-user-profile.md)

[Snapshot and restore APIs](./snapshot-restore-apis.md)

[Create or update snapshot repository](./put-snapshot-repo-api.md)

[Verify snapshot repository](./verify-snapshot-repo-api.md)

[Repository analysis](./repo-analysis-api.md)

[Get snapshot repository](./get-snapshot-repo-api.md)

[Delete snapshot repository](./delete-snapshot-repo-api.md)

[Clean up snapshot repository](./clean-up-snapshot-repo-api.md)

[Clone snapshot](./clone-snapshot-api.md)

[Create snapshot](./create-snapshot-api.md)

[Get snapshot](./get-snapshot-api.md)

[Get snapshot status](./get-snapshot-status-api.md)

[Restore snapshot](./restore-snapshot-api.md)

[Delete snapshot](./delete-snapshot-api.md)

[Snapshot lifecycle management APIs](./snapshot-lifecycle-management-api.md)

[Create or update policy](./slm-api-put-policy.md)

[Get policy](./slm-api-get-policy.md)

[Delete policy](./slm-api-delete-policy.md)

[Execute snapshot lifecycle policy](./slm-api-execute-lifecycle.md)

[Execute snapshot retention policy](./slm-api-execute-retention.md)

[Get snapshot lifecycle management status](./slm-api-get-status.md)

[Get snapshot lifecycle stats](./slm-api-get-stats.md)

[Start snapshot lifecycle management](./slm-api-start.md)

[Stop snapshot lifecycle management](./slm-api-stop.md)

[SQL APIs](./sql-apis.md)

[Clear SQL cursor](./clear-sql-cursor-api.md)

[Delete async SQL search](./delete-async-sql-search-api.md)

[Get async SQL search](./get-async-sql-search-api.md)

[Get async SQL search status](./get-async-sql-search-status-api.md)

[SQL search](./sql-search-api.md)

[SQL translate](./sql-translate-api.md)

[Transform APIs](./transform-apis.md)

[Create transform](./put-transform.md)

[Delete transform](./delete-transform.md)

[Get transforms](./get-transform.md)

[Get transform statistics](./get-transform-stats.md)

[Preview transform](./preview-transform.md)

[Reset transform](./reset-transform.md)

[Schedule now transform](./schedule-now-transform.md)

[Start transform](./start-transform.md)

[Stop transforms](./stop-transform.md)

[Update transform](./update-transform.md)

[Upgrade transforms](./upgrade-transforms.md)

[Usage API](./usage-api.md)

[Watcher APIs](./watcher-api.md)

[Ack watch](./watcher-api-ack-watch.md)

[Activate watch](./watcher-api-activate-watch.md)

[Deactivate watch](./watcher-api-deactivate-watch.md)

[Delete watch](./watcher-api-delete-watch.md)

[Execute watch](./watcher-api-execute-watch.md)

[Get watch](./watcher-api-get-watch.md)

[Get Watcher stats](./watcher-api-stats.md)

[Query watches](./watcher-api-query-watches.md)

[Create or update watch](./watcher-api-put-watch.md)

[Update Watcher settings](./watcher-api-update-settings.md)

[Get Watcher settings](./watcher-api-get-settings.md)

[Start watch service](./watcher-api-start.md)

[Stop watch service](./watcher-api-stop.md)

[Definitions](./api-definitions.md)

[Role mapping resources](./role-mapping-resources.md)

[Migration guide](./breaking-changes.md)

[8.9](./migrating-8.9.md)

[8.8](./migrating-8.8.md)

[8.7](./migrating-8.7.md)

[8.6](./migrating-8.6.md)

[8.5](./migrating-8.5.md)

[8.4](./migrating-8.4.md)

[8.3](./migrating-8.3.md)

[8.2](./migrating-8.2.md)

[8.1](./migrating-8.1.md)

[8.0](./migrating-8.0.md)

[Java time migration guide](./migrate-to-java-time.md)

[Transient settings migration guide](./transient-settings-migration-guide.md)

[Release notes](./es-release-notes.md)

[Elasticsearch version 8.9.0](./release-notes-8.9.0.md)

[Elasticsearch version 8.8.2](./release-notes-8.8.2.md)

[Elasticsearch version 8.8.1](./release-notes-8.8.1.md)

[Elasticsearch version 8.8.0](./release-notes-8.8.0.md)

[Elasticsearch version 8.7.1](./release-notes-8.7.1.md)

[Elasticsearch version 8.7.0](./release-notes-8.7.0.md)

[Elasticsearch version 8.6.2](./release-notes-8.6.2.md)

[Elasticsearch version 8.6.1](./release-notes-8.6.1.md)

[Elasticsearch version 8.6.0](./release-notes-8.6.0.md)

[Elasticsearch version 8.5.3](./release-notes-8.5.3.md)

[Elasticsearch version 8.5.2](./release-notes-8.5.2.md)

[Elasticsearch version 8.5.1](./release-notes-8.5.1.md)

[Elasticsearch version 8.5.0](./release-notes-8.5.0.md)

[Elasticsearch version 8.4.3](./release-notes-8.4.3.md)

[Elasticsearch version 8.4.2](./release-notes-8.4.2.md)

[Elasticsearch version 8.4.1](./release-notes-8.4.1.md)

[Elasticsearch version 8.4.0](./release-notes-8.4.0.md)

[Elasticsearch version 8.3.3](./release-notes-8.3.3.md)

[Elasticsearch version 8.3.2](./release-notes-8.3.2.md)

[Elasticsearch version 8.3.1](./release-notes-8.3.1.md)

[Elasticsearch version 8.3.0](./release-notes-8.3.0.md)

[Elasticsearch version 8.2.3](./release-notes-8.2.3.md)

[Elasticsearch version 8.2.2](./release-notes-8.2.2.md)

[Elasticsearch version 8.2.1](./release-notes-8.2.1.md)

[Elasticsearch version 8.2.0](./release-notes-8.2.0.md)

[Elasticsearch version 8.1.3](./release-notes-8.1.3.md)

[Elasticsearch version 8.1.2](./release-notes-8.1.2.md)

[Elasticsearch version 8.1.1](./release-notes-8.1.1.md)

[Elasticsearch version 8.1.0](./release-notes-8.1.0.md)

[Elasticsearch version 8.0.1](./release-notes-8.0.1.md)

[Elasticsearch version 8.0.0](./release-notes-8.0.0.md)

[Elasticsearch version 8.0.0-rc2](./release-notes-8.0.0-rc2.md)

[Elasticsearch version 8.0.0-rc1](./release-notes-8.0.0-rc1.md)

[Elasticsearch version 8.0.0-beta1](./release-notes-8.0.0-beta1.md)

[Elasticsearch version 8.0.0-alpha2](./release-notes-8.0.0-alpha2.md)

[Elasticsearch version 8.0.0-alpha1](./release-notes-8.0.0-alpha1.md)

[Dependencies and versions](./dependencies-versions.md)