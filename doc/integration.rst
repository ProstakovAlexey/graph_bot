Integration
===========
For integration you program must make:
    1. Send SSL request in format. token - give from bot father (for test can use `test_token`), `user_id` - himself.
    2. Read bot answer:           -
           - status can use for you program logic (now use for testing);
           - text - need show for users.
    3. Wait user answer, and send it in bot.
    4. Go to in 2.

Formats
-------
Robot use json POST request. If you use python, can look `tests.py`. **Request format**::


    Content-Type": "text/json; charset=utf-8
    {
     'token': 'test_token',
     'user_id': '123-123',
     'user_name': 'Tester',
     'text': '/end'
    }

Descriptions:
    - `token` - security token, was write in file `tokens.txt`;
    - `user_id` - unic id, possibel UUID;
    - `user_name` - user name, nounic, exapmle Alex or Sara;
    - `text` - users text.

**Response format**::

    {
     'status': '0',
     'text': 'Answer'
    }


Descriptions:
    - status - code (now use only for test);
    - text - bot answer text.


