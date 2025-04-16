# AzureServiceModule/modules/AISearchClient.py

class AISearchService:
    def __init__(self, client, deployment, search_key, search_endpoint, search_index):
        self.client = client
        self.deployment = deployment
        self.search_key = search_key
        self.search_endpoint = search_endpoint
        self.search_index = search_index

    def query(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": "Azure AI Search를 활용해 사용자의 질문에 적합한 공연 기획 문서를 요약해 주세요."},
            {"role": "user", "content": user_input}
        ]

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=0.2,
            max_tokens=800,
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": self.search_endpoint,
                            "index_name": self.search_index,
                            "semantic_configuration": f"{self.search_index}-semantic-configuration",
                            "query_type": "semantic",
                            "in_scope": True,
                            "filter": None,
                            "strictness": 3,
                            "top_n_documents": 5,
                            "authentication": {
                                "type": "api_key",
                                "key": self.search_key
                            }
                        }
                    }
                ]
            }
        )

        return response.choices[0].message.content.strip()
