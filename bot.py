from abc import abstractmethod
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from translators import Translator, AzureTranslator
from jokes_servise import get_the_jock_number_i
from conf import TELEGRAM_TOKEN


class Bot:
    def __init__(self, translator: Translator, language):
        self.translator = translator
        self.language = language

    @abstractmethod
    def start_bot(self):
        pass

    @abstractmethod
    def handle_response(self, text: str) -> str:
        pass

    @abstractmethod
    def get_token(self) -> str:
        pass

    @abstractmethod
    def get_bot_username(self) -> str:
        pass


class TelegramBot(Bot):

    def __init__(self, translator: Translator, language):
        super().__init__(translator, language)

    def get_bot_username(self) -> str:
        return '@ChunkNurrisbot'

    def get_token(self) -> str:
        return TELEGRAM_TOKEN

    def start_bot(self):
        app = Application.builder().token(self.get_token()).build()
        # Commands
        app.add_handler(CommandHandler('start', self.start_command))
        # Messages
        app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        app.run_polling(poll_interval=3)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text

        print(f'User({update.message.chat.id}) in {message_type}: "{text}"')
        response: str = self.handle_response(text)
        print('Bot:', response)
        await update.message.reply_text(response)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hello! welcome to Chunk Nurris bot!')

    def handle_response(self, text: str) -> str:
        processed: str = text.lower()
        result = "I do not understand what you wrote.."

        if 'set language' in processed:
            result = self.handle_set_language_request(processed)

        elif processed.isdigit():
            result = self.handle_digit(processed)

        return self.translator.translate(result, self.language)

    def handle_digit(self, processed):
        if 101 >= int(processed) > 0:
            joke = get_the_jock_number_i(int(processed))
            response = self.translator.translate(joke, self.language)
            return response
        else:
            return "Please choose number between 1 - 101 !"

    def handle_set_language_request(self, processed):
        parts = processed.split()
        if len(parts) >= 3:
            language = parts[-1]
            self.language = language
            short_lang = self.translator.get_language_for_api(language)
            if short_lang == ' ':
                return self.translator.translate(
                    "I cant find that language, Please choose another language", language)
            self.language = language
            respond = self.translator.translate("No Problem", self.language)
            return respond
        else:
            return self.translator.translate("Please type a desired language", self.language)


if __name__ == '__main__':
    TelegramBot(AzureTranslator(), "English").start_bot()
