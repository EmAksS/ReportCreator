USER = [
    {
        'name': 'Логин',
        'key_name': 'username',
        'is_required': True,
        'placeholder': 'Ваш логин пользователя',
        'type': 'TEXT',
        'validation_regex': '^[a-zA-Z0-9_-]{4,16}$',
        'related_item': "User",
        'related_info': None,
        'secure_text': False,
        'error_text': "Имя пользователя должно быть уникальным, не должно содержать пробелов и быть от 4 до 16 символов.",
    },
    {
        'name': 'Пароль',
        'key_name': 'password',
        'is_required': True,
        'placeholder': 'Ваш пароль',
        'type': 'TEXT',
        # минимум 8 символов, минимум одна цифра
        'validation_regex': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$',
        'related_item': "User",
        'related_info': None,
        'secure_text': True,
        'error_text': "Пароль должен быть длиннее 8 символов и содержать хотя бы одну цифру и заглавную букву.",
    },
    {
        'name': 'Фамилия',
        'key_name': 'last_name',
        'is_required': True,
        'placeholder': 'Ваша фамилия',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*$',
        'related_item': "User",
        'related_info': None,
        'secure_text': False,
        'error_text': None,
    },
    {
        'name': 'Имя',
        'key_name': 'first_name',
        'is_required': True,
        'placeholder': 'Ваше имя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*$',
        'related_item': "User",
        'related_info': None,
        'secure_text': False,
        'error_text': None,
    },
    {
        'name': 'Отчество',
        'key_name': 'surname',
        'is_required': False,
        'placeholder': 'Ваше отчество',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]*$',
        'related_item': "User",
        'related_info': None,
        'secure_text': False,
        'error_text': None,
    },
]

EXECUTOR = [
    {
        'name': 'Краткое название компании',
        'key_name': 'company_name',
        'is_required': True,
        'placeholder': 'Название компании с сокращёнными аббревиатурами',
        'type': 'TEXT',
        'validation_regex': '^[a-zA-Z0-9_\"\'\-«»а-яА-Я\s\.\,]{0,64}$',
        'related_item': "Executor",
        'related_info': None,
        'secure_text': False,
        'error_text': "Длина названия не должна превышать 64 символа, а также не содержать особых символов."
    },
    {
        'name': 'Полное название компании',
        'key_name': 'company_fullName',
        'is_required': False,
        'placeholder': 'Название компании с расшифровкой аббревиатур',
        'type': 'TEXT',
        'validation_regex': '^[a-zA-Z0-9_\"\'\-«»а-яА-Я\s\.\,]{0,256}$',
        'related_item': "Executor",
        'related_info': None,
        'secure_text': False,
        'error_text': "Длина названия не должна превышать 256 символов, а также не содержать особых символов."
    },
    {
        'name': 'Логин суперпользователя',
        'key_name': 'username',
        'is_required': True,
        'placeholder': 'Введите логин суперпользователя',
        'type': 'TEXT',
        'validation_regex': '^[a-zA-Z0-9_-]{4,16}$',
        'related_item': "Executor",
        'related_info': None,
        'secure_text': False,
    },
    {
        'name': 'Пароль',
        'key_name': 'password',
        'is_required': True,
        'placeholder': 'Введите пароль',
        'type': 'TEXT',
        # минимум 8 символов, минимум одна цифра
        'validation_regex': '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$',
        'related_item': "Executor",
        'related_info': None,
        'secure_text': True,
    },
    {
        'name': 'Фамилия',
        'key_name': 'last_name',
        'is_required': True,
        'placeholder': 'Ваша фамилия',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*$',
        'related_item': "Executor",
        'related_info': None,
        'secure_text': False,
    },
    {
        'name': 'Имя',
        'key_name': 'first_name',
        'is_required': True,
        'placeholder': 'Ваше имя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*$',
        'related_item': "Executor",
        'related_info': None,
        'secure_text': False,
    },
    {
        'name': 'Отчество',
        'key_name': 'surname',
        'is_required': False,
        'placeholder': 'Ваше отчество',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]*$',
        'related_item': "Executor",
        'related_info': None,
        'secure_text': False,
    },
]

CONTRACTOR = [
    {
        'name': 'Краткое название компании',
        'key_name': 'company_name',
        'is_required': True,
        'placeholder': 'Название компании с сокращёнными аббревиатурами',
        'type': 'TEXT',
        'validation_regex': '^[a-zA-Z0-9_\"\'\-«»а-яА-Я\s\.\,]{0,64}$',
        'related_item': "Contractor",
        'related_info': None,
        'secure_text': False,
        'error_text': "Длина названия не должна превышать 64 символа, а также не содержать особых символов."
    },
    {
        'name': 'Полное название компании',
        'key_name': 'company_fullName',
        'is_required': True,
        'placeholder': 'Название компании с расшифровкой аббревиатур',
        'type': 'TEXT',
        'validation_regex': '^[a-zA-Z0-9_\"\'\-«»а-яА-Я\s\.\,]{0,256}$',
        'related_item': "Contractor",
        'related_info': None,
        'secure_text': False,
        'error_text': "Длина названия не должна превышать 256 символов, а также не содержать особых символов."
    },
    {
        'name': 'Город расположения заказчика',
        'key_name': 'contractor_city',
        'is_required': True,
        'placeholder': 'Название компании с сокращёнными аббревиатурами',
        'type': 'TEXT',
        'validation_regex': '^[a-zA-Z0-9_.,а-яА-Я]{0,64}$',
        'related_item': "Contractor",
        'related_info': None,
        'secure_text': False,
        'error_text': "Длина названия не должна превышать 64 символа, а также не содержать особых символов."
    },
]

TEMPLATE = [
    {
        'name': 'Название шаблона',
        'key_name': 'template_name',
        'is_required': True,
        'placeholder': 'Введите название шаблона документа',
        'type': 'TEXT',
        # Любая кириллица и латиница с использованием цифр и нижнего подчёркивания, но не должно начинаться и заканчиваться с _
        'validation_regex': '^([(a-zA-Z0-9)|(а-яА-Я)]_*)*[^_]$',
        'related_item': "Template",
        'related_info': None,
        'secure_text': False,
        'error_text': "Название документа должно содержать только кириллицу, латиницу, цифры. Также допускается в названии нижнее подчёркивание `_`, но оно должно начинаться и заканчиваться им."
    },
    {
        'name': 'Файл шаблона',
        'key_name': 'template_file',
        'is_required': True,
        'placeholder': 'Отправьте файл шаблона в формате `.docx`',
        'type': 'FILE',
        'validation_regex': '',
        'related_item': "Template",
        'secure_text': False,
        'error_text': ""
    },
    {
        'name': 'Тип документа',
        'key_name': 'template_type',
        'is_required': True,
        'placeholder': 'Выберите тип создаваемого документа',
        'type': 'COMBOBOX',
        'validation_regex': None,
        'related_item': "Template",
        'related_info': {
            'url': "document/types/",
            'show_field': "name",
            'save_field': "code",
        },
        'secure_text': False,
        'error_text': ""
    },
    {
        'name': 'Юридическое лицо исполнителя',
        'key_name': 'related_executor_person',
        'is_required': True,
        'placeholder': 'Юридическое лицо исполнителя договора',
        'type': 'COMBOBOX',
        'validation_regex': None,
        'related_item': "Template",
        'related_info': {
            'url': "persons/executor/list/",
            'show_field': "initials",
            'save_field': "id",
        },
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Юридическое лицо заказчика',
        'key_name': 'related_contractor_person',
        'is_required': True,
        'placeholder': 'Юридическое лицо заказчика по договору',
        'type': 'COMBOBOX',
        'validation_regex': None,
        'related_item': "Template",
        'related_info': {
            'url': "persons/contractor/list/",
            'show_field': "initials",
            'save_field': "id",
        },
        'secure_text': False,
        'error_text': None
    },
]

EXECUTOR_PERSON = [
    {
        'name': 'Фамилия юрлица',
        'key_name': 'last_name',
        'is_required': True,
        'placeholder': 'Фамилия юридического лица исполнителя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
        'related_item': "ExecutorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Имя юрлица',
        'key_name': 'first_name',
        'is_required': True,
        'placeholder': 'Имя юридического лица исполнителя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
        'related_item': "ExecutorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Отчество юрлица',
        'key_name': 'surname',
        'is_required': False,
        'placeholder': 'Отчество юридического лица исполнителя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]*$',
        'related_item': "ExecutorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Должность юрлица',
        'key_name': 'post',
        'is_required': False,
        'placeholder': 'Должность юридического лица исполнителя в компании',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]*{0,64}$',
        'related_item': "ExecutorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
]

CONTRACTOR_PERSON = [
    {
        'name': 'Фамилия юрлица',
        'key_name': 'last_name',
        'is_required': True,
        'placeholder': 'Фамилия юридического лица исполнителя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
        'related_item': "ContractorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Имя юрлица',
        'key_name': 'first_name',
        'is_required': True,
        'placeholder': 'Имя юридического лица исполнителя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
        'related_item': "ContractorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Отчество юрлица',
        'key_name': 'surname',
        'is_required': False,
        'placeholder': 'Отчество юридического лица исполнителя',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]*$',
        'related_item': "ContractorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Должность юрлица',
        'key_name': 'post',
        'is_required': False,
        'placeholder': 'Должность юридического лица исполнителя в компании',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]*{0,64}$',
        'related_item': "ContractorPerson",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Компания юридического лица заказчика',
        'key_name': 'company',
        'is_required': True,
        'placeholder': 'Выберите компанию в которой находится юридическое лицо заказчика',
        'type': 'COMBOBOX',
        'validation_regex': None,
        'related_item': "ContractorPerson",
        'related_info': {
            'url': "company/contractors/",
            'show_field': "company_name",
            'save_field': "id",
        },
        'secure_text': False,
        'error_text': None
    },
]

FIELD = [
    {
        'name': 'Русское название поля',
        'key_name': 'name',
        'is_required': True,
        'placeholder': 'Введите русское название поля',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
        'related_item': "Field",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Ключевое название поля',
        'key_name': 'key_name',
        'is_required': True,
        'placeholder': 'Введите ключевое название поля',
        'type': 'TEXT',
        'validation_regex': '^\w{0,64}$',
        'related_item': "Field",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно быть уникальным, содержать только латиницу, а также не более 64 символов"
    },
    {
        'name': 'Необходимое поле?',
        'key_name': 'is_required',
        'is_required': True,
        'placeholder': 'Это необходимое поле?',
        'type': 'BOOL',
        'validation_regex': None,
        'related_item': "Field",
        'related_info': None,
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Предложение записи для пользователя',
        'key_name': 'placeholder',
        'is_required': False,
        'placeholder': 'Укажите текст, который указывается в предложении.',
        'type': 'TEXT',
        'validation_regex': '^([(a-zA-Z0-9)|(а-яА-Я)]_*)*[^_]$',
        'related_item': "Field",
        'related_info': None,
        'secure_text': False,
        'error_text': "Текст должен состоять из кириллицы или латиницы."
    },
    {
        'name': 'Тип поля',
        'key_name': 'type',
        'is_required': True,
        'placeholder': 'Выберите тип поля из списка',
        'type': 'COMBOBOX',
        'validation_regex': None,
        'related_item': "Field",
        'related_info': {
            # ! Не выводить COMBOBOX, так как их создание невозможно!
            'url': "url_для_вывода_всех_FIELD_TYPES",
            'show_field': "value",
            'save_field': "id",
        },
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Регулярное выражение для проверки',
        'key_name': 'validation_regex',
        'is_required': False,
        'placeholder': 'Значение должно проверяться, укажите регулярное тут регулярное выражение.',
        'type': 'TEXT',
        'validation_regex': None,
        'related_item': "Field",
        'related_info': None, 
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Текст при ошибке валидации',
        'key_name': 'error_text',
        'is_required': False,
        'placeholder': 'Текст ошибки при несоответствии `validation_regex`.',
        'type': 'TEXT',
        'validation_regex': '^([(a-zA-Z0-9)|(а-яА-Я)]_*)*[^_]$',
        'related_item': "Field",
        'related_info': None, 
        'secure_text': False,
        'error_text': "Неправильный формат текста."
    },
]

DOCUMENT_FIELD = [
    {
        'name': 'Связанный шаблон',
        'key_name': 'related_template',
        'is_required': True,
        'placeholder': 'Выберите шаблон для создания поля.',
        'type': 'COMBOBOX',
        'validation_regex': None,
        'related_item': "DocumentField",
        'related_info': {
            'url': "url_для_вывода_всех_шаблонов_компании",
            'show_field': "name",
            'save_field': "id",
        },
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Русское название поля',
        'key_name': 'name',
        'is_required': True,
        'placeholder': 'Введите русское название поля',
        'type': 'TEXT',
        'validation_regex': '^[а-яА-Я]+(-[а-яА-Я]+)*{0,64}$',
        'related_item': "DocumentField",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно содержать только кириллицу, а также не более 64 символов"
    },
    {
        'name': 'Ключевое название поля',
        'key_name': 'key_name',
        'is_required': True,
        'placeholder': 'Введите ключевое название поля',
        'type': 'TEXT',
        'validation_regex': '^\w{0,64}$',
        'related_item': "DocumentField",
        'related_info': None,
        'secure_text': False,
        'error_text': "Значение должно быть уникальным, содержать только латиницу, а также не более 64 символов"
    },
    {
        'name': 'Необходимое поле?',
        'key_name': 'is_required',
        'is_required': True,
        'placeholder': 'Это необходимое поле?',
        'type': 'BOOL',
        'validation_regex': None,
        'related_item': "DocumentField",
        'related_info': None,
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Предложение записи для пользователя',
        'key_name': 'placeholder',
        'is_required': False,
        'placeholder': 'Укажите текст, который указывается в предложении.',
        'type': 'TEXT',
        'validation_regex': '^([(a-zA-Z0-9)|(а-яА-Я)]_*)*[^_]$',
        'related_item': "DocumentField",
        'related_info': None,
        'secure_text': False,
        'error_text': "Текст должен состоять из кириллицы или латиницы."
    },
    {
        'name': 'Тип поля',
        'key_name': 'type',
        'is_required': True,
        'placeholder': 'Выберите тип поля из списка',
        'type': 'COMBOBOX',
        'validation_regex': None,
        'related_item': "DocumentField",
        'related_info': {
            # ! Не выводить COMBOBOX, так как их создание невозможно!
            'url': "url_для_вывода_всех_FIELD_TYPES",
            'show_field': "value",
            'save_field': "id",
        },
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Регулярное выражение для проверки',
        'key_name': 'validation_regex',
        'is_required': False,
        'placeholder': 'Значение должно проверяться, укажите регулярное тут регулярное выражение.',
        'type': 'TEXT',
        'validation_regex': '???',
        'related_item': "DocumentField",
        'related_info': None, 
        'secure_text': False,
        'error_text': None
    },
    {
        'name': 'Текст при ошибке валидации',
        'key_name': 'error_text',
        'is_required': False,
        'placeholder': 'Текст ошибки при несоответствии `validation_regex`.',
        'type': 'TEXT',
        'validation_regex': '^([(a-zA-Z0-9)|(а-яА-Я)]_*)*[^_]$',
        'related_item': "DocumentField",
        'related_info': None, 
        'secure_text': False,
        'error_text': "Неправильный формат текста."
    },
]


ALL_ITEMS = [
    USER,
    EXECUTOR,
    CONTRACTOR, 
    TEMPLATE, 
    EXECUTOR_PERSON, 
    CONTRACTOR_PERSON,
    FIELD,
    DOCUMENT_FIELD,
]

STR_ITEMS = [
    "USER",
    "EXECUTOR",
    "CONTRACTOR", 
    "TEMPLATE", 
    "EXECUTOR_PERSON", 
    "CONTRACTOR_PERSON",
    "FIELD",
    "DOCUMENT_FIELD",
]
