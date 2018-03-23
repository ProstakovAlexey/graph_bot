Graph bot
=========








Make new graph scheme
---------------------
Bot work with scheme reading by DOT Language [http://www.graphviz.org/documentation/]. But scheme for bot have some features:
    1. First node must have name **Start**.
    2. Last node must have name **End**.
    3. If node have 2 or more edge, each edge must have name. Bot think, it is question.
    4. After you must check file. Use command ``dot -Tpng test.gv -o test.png``.
    5. Copy file in ``graph``.
    6. Write section in ``config.ini`` and restart bot.

Exapmle scheme you can look in ``for_test/test.gv``


