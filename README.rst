Описание
========
Представляет собой базу знаний по решению различных проблема, где решение представлено в виде графа (дерева). Решение состоит из набора вопросов и вариантов ответа. Постороенно так, что пользователь отвечает на вопросы, выбирая один из вариантов, и продвигается по графу, достигая со временем решения. Интерфейс реализован в виде telegram бота. Графы решения можно готовит в стороннем пакете graphiz или программе freemind, загружать в папку `graph`.

Решаемые проблемы
=================
ПО над которым я работаю устанавливается в закрытой сети, без доступа к интернету. Иногда с ним случаются проблемы, обычно в момент отпуска основного администратора, когда обслуживание передано не очень опытному специалисту. В такие моменты нет времени на изучение документации, интернет доступен только с личного телефона, просмотравать на котором не удобно. Тут может помочь легкое решение с использование telegram, оно требует мало трафика, в понятной форме дает советы по решению проблемы. 

RUN
===
You can use the bot to organize the knowledge base.
For it need:
    1. Develop a solution graph for the problem and describe it in dot.
    2. Place dot file in path `graph`.
    3. Add section in `config.ini`.
    4. Run (restart) bot.

Now you can use program `graph_check.py` for check bot. I made a demonstration project - fishing,
you can see it in `graph`. Demo project deploying in Heroku, URL=http://polar-coast-24118.herokuapp.com/bot
Please look more documentation in `doc/`

If it is interesting for you - please help me. Now need javascript for site: small box for bot dialog.
