"""test_app.py"""
from streamlit.testing.v1 import AppTest



def test_type_a_message():
    """Type a message as a user"""
    at = AppTest.from_file("app.py").run()
    testmessage = 'bonjour'
    at.chat_input[0].set_value(testmessage)
    at.chat_input[0].run() 
    assert at.chat_message[-1].markdown[0].value == f"Echo: {testmessage}"