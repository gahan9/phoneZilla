JET_DEFAULT_THEME = 'green'


JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#354052',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True

JET_CHANGE_FORM_SIBLING_LINKS = True

JET_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultIndexDashboard'

JET_APP_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultAppIndexDashboard'

JET_SIDE_MENU_ITEMS = [
    # {'app_label': 'authtoken', 'items': [
    #     {'name': 'token'},
    # ]},
    # {'app_label': 'auth', 'items': [
    #     {'name': 'user'},
    # ]},
    {'app_label': 'inventory_management', 'items': [
        {'name': 'productrecord'},
        {'name': 'purchaserecord'},
    ]},
    {'app_label': 'sale_record', 'items': [
        {'name': 'customerdetail'},
        {'name': 'salerecord'},
    ]},
]
