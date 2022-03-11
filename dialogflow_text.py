# Модуль для работы с погодой
from google.cloud import dialogflow
import os


# Если нужно привязать Dialogflow, то потребуется залогиниться через сервис аккаунт
# Скачиваете свой файл json с сайта googlecloud, указываем путь до файла
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'access/google_access.json'
# ID проекта, к которому будем обращаться
PROJECT_ID = 'small-talk-hlcf'
# ID сессии, можно указать любой, формат str
SESSION_ID = 'eva'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, SESSION_ID)


# Принимает запрос для dialogflow
# Возвращает текст ответа и событие
def dialog_flow_answer(text):
    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.display_name
