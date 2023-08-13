

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md)

[« Lucene expressions language](modules-scripting-expression.md) [Data
management »](data-management.md)

## 使用脚本引擎的高级脚本

"脚本引擎"是实现脚本语言的后端。它也可以用来编写需要使用高级内部脚本的脚本。例如，想要在评分时使用术语频率的脚本。

插件文档提供了有关如何编写插件的更多信息，以便 Elasticsearch 能够正确加载它。要注册"ScriptEngine"，您的插件应该实现"ScriptPlugin"接口并覆盖"getScriptEngine(设置设置)"方法。

以下是使用语言名称"expert_scripts"的自定义"脚本引擎"的示例。它实现了一个名为"pure_df"的单个脚本，该脚本可用作搜索脚本，以覆盖每个文档的分数作为所提供术语的文档频率。

    
    
    private static class MyExpertScriptEngine implements ScriptEngine {
        @Override
        public String getType() {
            return "expert_scripts";
        }
    
        @Override
        public <T> T compile(
            String scriptName,
            String scriptSource,
            ScriptContext<T> context,
            Map<String, String> params
        ) {
            if (context.equals(ScoreScript.CONTEXT) == false) {
                throw new IllegalArgumentException(getType()
                        + " scripts cannot be used for context ["
                        + context.name + "]");
            }
            // we use the script "source" as the script identifier
            if ("pure_df".equals(scriptSource)) {
                ScoreScript.Factory factory = new PureDfFactory();
                return context.factoryClazz.cast(factory);
            }
            throw new IllegalArgumentException("Unknown script name "
                    + scriptSource);
        }
    
        @Override
        public void close() {
            // optionally close resources
        }
    
        @Override
        public Set<ScriptContext<?>> getSupportedContexts() {
            return Set.of(ScoreScript.CONTEXT);
        }
    
        private static class PureDfFactory implements ScoreScript.Factory,
                                                      ScriptFactory {
            @Override
            public boolean isResultDeterministic() {
                // PureDfLeafFactory only uses deterministic APIs, this
                // implies the results are cacheable.
                return true;
            }
    
            @Override
            public LeafFactory newFactory(
                Map<String, Object> params,
                SearchLookup lookup
            ) {
                return new PureDfLeafFactory(params, lookup);
            }
        }
    
        private static class PureDfLeafFactory implements LeafFactory {
            private final Map<String, Object> params;
            private final SearchLookup lookup;
            private final String field;
            private final String term;
    
            private PureDfLeafFactory(
                        Map<String, Object> params, SearchLookup lookup) {
                if (params.containsKey("field") == false) {
                    throw new IllegalArgumentException(
                            "Missing parameter [field]");
                }
                if (params.containsKey("term") == false) {
                    throw new IllegalArgumentException(
                            "Missing parameter [term]");
                }
                this.params = params;
                this.lookup = lookup;
                field = params.get("field").toString();
                term = params.get("term").toString();
            }
    
            @Override
            public boolean needs_score() {
                return false;  // Return true if the script needs the score
            }
    
            @Override
            public ScoreScript newInstance(DocReader docReader)
                    throws IOException {
                DocValuesDocReader dvReader = DocValuesDocReader) docReader);             PostingsEnum postings = dvReader.getLeafReaderContext()                     .reader().postings(new Term(field, term;
                if (postings == null) {
                    /*
                     * the field and/or term don't exist in this segment,
                     * so always return 0
                     */
                    return new ScoreScript(params, lookup, docReader) {
                        @Override
                        public double execute(
                            ExplanationHolder explanation
                        ) {
                            return 0.0d;
                        }
                    };
                }
                return new ScoreScript(params, lookup, docReader) {
                    int currentDocid = -1;
                    @Override
                    public void setDocument(int docid) {
                        /*
                         * advance has undefined behavior calling with
                         * a docid <= its current docid
                         */
                        if (postings.docID() < docid) {
                            try {
                                postings.advance(docid);
                            } catch (IOException e) {
                                throw new UncheckedIOException(e);
                            }
                        }
                        currentDocid = docid;
                    }
                    @Override
                    public double execute(ExplanationHolder explanation) {
                        if (postings.docID() != currentDocid) {
                            /*
                             * advance moved past the current doc, so this
                             * doc has no occurrences of the term
                             */
                            return 0.0d;
                        }
                        try {
                            return postings.freq();
                        } catch (IOException e) {
                            throw new UncheckedIOException(e);
                        }
                    }
                };
            }
        }
    }

您可以通过将其"lang"指定为"expert_scripts"并将脚本的名称指定为脚本源来执行脚本：

    
    
    POST /_search
    {
      "query": {
        "function_score": {
          "query": {
            "match": {
              "body": "foo"
            }
          },
          "functions": [
            {
              "script_score": {
                "script": {
                    "source": "pure_df",
                    "lang" : "expert_scripts",
                    "params": {
                        "field": "body",
                        "term": "foo"
                    }
                }
              }
            }
          ]
        }
      }
    }

[« Lucene expressions language](modules-scripting-expression.md) [Data
management »](data-management.md)
