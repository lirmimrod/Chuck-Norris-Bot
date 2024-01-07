from abc import abstractmethod
import requests
import uuid
from conf import AZURE_KEY


class Translator:

    def translate(self, text_to_translate: str, desired_language: str) -> str:
        request = requests.post(self.get_url(),
                                params=self.get_request_params(self.get_language_for_api(desired_language)),
                                headers=self.get_request_headers(), json=self.get_body(text_to_translate))
        response = request.json()
        result = self.pars_response(response)
        return result

    @abstractmethod
    def pars_response(self, response: list) -> str:
        pass

    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def get_request_params(self, lang_for_api: str):
        pass

    @abstractmethod
    def get_request_headers(self):
        pass

    @abstractmethod
    def get_body(self, text_to_translate: str):
        pass

    @abstractmethod
    def get_language_for_api(self, desired_language: str) -> str:
        pass


class AzureTranslator(Translator):

    def pars_response(self, response: list) -> str:
        first_translation = response[0]['translations'][0]
        text_content = first_translation['text']
        return text_content

    def get_body(self, text_to_translate: str):
        return [{'text': text_to_translate}]

    def get_key(self) -> str:
        return AZURE_KEY

    def get_url(self) -> str:
        return "https://api.cognitive.microsofttranslator.com" + '/translate'

    def get_request_params(self, lang_for_api: str):
        return {
            "api-version": "3.0",
            "from": "en",
            "to": lang_for_api
        }

    def get_request_headers(self):
        return {
            "Ocp-Apim-Subscription-Key": self.get_key(),
            "Content-type": "application/json",
            "Ocp-Apim-Subscription-Region": "francecentral",
            "X-ClientTraceId": str(uuid.uuid4())
        }

    def get_language_for_api(self, desired_language: str) -> str:
        language_map = self.get_languages_dictionary()
        for key, val in language_map.items():
            if key == "translation":
                for key_short_name, map_name_val in val.items():
                    if map_name_val['name'].lower() == desired_language.lower():
                        return key_short_name
        return ' '

    @staticmethod
    def get_languages_dictionary():
        endpoint = 'https://api.cognitive.microsofttranslator.com/languages?api-version=3.0'
        response = requests.get(endpoint)

        if response.status_code == 200:
            # Parse the JSON response
            languages_data = response.json()
        else:
            print(f'Error: HTTP {response.status_code} - {response.text}')
        return languages_data
