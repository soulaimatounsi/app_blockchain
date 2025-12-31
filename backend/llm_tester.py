from mistralai import Mistral

class LLMSecurityTester:
    def __init__(self, api_key, model_name="mistral-small-latest"):
        self.client = Mistral(api_key=api_key)
        self.model_name = model_name

    def analyze_contract(self, contract_code):
        prompt = f"""
You are an expert in Ethereum smart contract security.
Analyze the following Solidity contract and detect vulnerabilities.
Return the answer in JSON format.

Contract:
{contract_code}
"""
        response = self.client.chat.complete(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
