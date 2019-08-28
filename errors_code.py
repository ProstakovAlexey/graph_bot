ERRORS = {
    1: {
        'ru': 'История переписки удалена, можно начать сначала, по команде /start',
        'en': 'History is reset. You can start again by command /start'
    },
    2: {
        'ru': 'Вы ввели не правильный номер. Нужно вводить номер от 1 до .... Номера можно посмотреть по команде /list',
        'en': 'You entered the wrong number, you need to enter from 1 to ... Look for number can see /list'
    },

    4: {
        'ru': 'Вы ввели неправильный формат команды, нужно вводить /start {номер}. Пример /start 1',
        'en': 'You entered the start command in the wrong format, good format example /start 1',
    },
    5: {
        'ru': 'Привет %s. Я могу помочь найти решение некоторых проблем, используя заранее подготовленные '
              'графы решений. Чтобы посмотреть список решение введите /list. Для начала работы с решением '
              'введите /start и номер решения, например /start 1. После я буду задавать вопросы и предлагать '
              'варианты ответов, вводите номер нужного. Я запоминаю разговор (пока не перезагружен). Если '
              'нужно прекратить наберите /end и вернетесь к выбору решения.',
        'en': 'Hi %s. I can help to find a solution to some problems using pre-prepared graphs solutions. '
              'You can see all available solutions with the /list command. For starting, you write /start and'
              ' the solution number, for example /start 1. After I ask some questions that will help to sort'
              ' out the problem. I remember our correspondence (if I do not restart) and I can continue from '
              'the previous place. If you want to finish, then write /end.'
    },
    6: {
        'ru': 'Список доступных решений (напишите /start и номер решения):',
        'result': 'List of available algorithms:<br/>'
    },
    7: {
        'ru': 'Привет %s. Я Вас не помню, пожалуйста введите команду /help для знакомства',
        'en': 'Hi %s. I do not remember you, let is get started with the command /help'
    },
    19: {
        'ru': 'Введите что угодно, нажмите ENTER',
        'en': 'Input any thing and press ENTER'
    },
    20: {
        'en': 'ERROR! Node name %s, comment %s have not edge(s). '
              'Any node must hav edge(s), except End, one must lead at least one edge in dot file.',
        'ru': 'Ошибка! Нода %s, комментарий %s не имеет ребра(ер) '
              'Любая нода, кроме End, должна иметь 1 или более ребер. Проверьте dot файл.'
    },
    21: {
        'ru': 'Поздравляю. Алгоритм завершен!',
        'en': 'Congratulations, the algorithm is complete!'
    },
    22: {
        'ru': 'Надо ввести цифру',
        'en': 'Please input only digits'
    }
}


def get_error(code, lang='ru'):
    """
    Return message bu code and lang. Need for internationalization application.
    :param code: message number
    :param lang: user lang
    :return:
    """
    if code not in ERRORS:
        return f"Have not message for error_code = {code}"
    if lang in ERRORS[code]:
        return ERRORS[code][lang]
    if 'en' in ERRORS[code]:
        return ERRORS[code]['en']
    return 'Imposable error'
