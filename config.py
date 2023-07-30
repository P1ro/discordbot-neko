TOKEN = 'MTEzNTAyMjc5MjQyNTg2NTI5Ng.Gw1voT.S7MDjReB-R-B6soRgfF1RyoiHiuWodDxyQIjL0'
CHANNEL_ID = 955667648845316146
COMMANDS = [
    {
        'command': '!mine',
        'rules': {
            'max_interval': 5,
            'min_interval': 5,
            'depends_on': None,
            'message_to_answer': None,
            'commands_to_avoid': None,
            'time_to_avoid': None
        }
    },
    {
        'command': '!fish',
        'rules': {
            'max_interval': 5,
            'min_interval': 5,
            'depends_on': '!mine',
            'message_to_answer': None,
            'commands_to_avoid': None,
            'time_to_avoid': None
        }
    },
    {
        'command': '!use vida',
        'rules': {
            'max_interval': None,
            'min_interval': None,
            'depends_on': None,
            'message_to_answer': 'Te has salvado',
            'commands_to_avoid': None,
            'time_to_avoid': None
        }
    },
    {
        'command': '!work',
        'rules': {
            'max_interval': 35 * 60,
            'min_interval': 30 * 60,
            'depends_on': None,
            'message_to_answer': None,
            'commands_to_avoid': [
                    '!mine',
                    '!fish',
                ],
            'time_to_avoid': 180
        }
    },
]