#from file.py import function_to_test, Class, value
def test_function_to_test():
    result = function_to_test('some_value')
    assert isinstance(result, Class)
    assert result in value

Фреймворк pytest

# pip install pytest
# pytest test.py

# Для срабатывания одной кнопкой дотаточно настроить в Debug launch.json нажатием на create json file/ module -- pytest
#нейм, тайп, реквест, модуль, 'args': ['test.py']
#далее F5



Случай использования 	                        Flake8 	            PyLint
Установка 	                                    pip install flake8 	pip install pylint
Получить справку 	                            flake8 --help 	    pylint
Проанализировать конкретный файл или модуль 	flake8 <filename> 	pylint <filename>




async def process_messages(messages, do_async):
    for message in messages:
        try:
            user_id = message['user']['id']
            user = db_conn.get('user', 'id=={}'.format(user_id))
            user.messages = user.messages + '\n' + message['text']
            user.save()
            if do_async:
                await db_conn.write_async(
                    'message', 
                    {'text': message['text'], 'user_id': message['user']['id']}
                )
            else:
                db_conn.write(
                    'message',
                    {'text': message['text'], 'user_id': message['user']['id']}
                )
            return 200, 'OK'
        except DatabaseException as exc:
            return 400, str(exc)