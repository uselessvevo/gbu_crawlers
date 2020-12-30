from scrapy_xlsx import XlsxItemExporter

LANDS_TRANS = {
    'zemelnye-uchastki': 'Земельные участки',
    'zemlya': 'Земля'
}

BUILDINGS_TRANS = {
    'ofis': 'Офис',
    'bazy': 'Базы',
    'sklad': 'Склад',
    'ferma': 'Ферма',
    'proizvodstvo/': 'Производство',
    'torgovye-pomeshheniya': 'Торговое помещение',
    'svobodnoe-naznachenie': 'Свободное назначение',
    'gotovyjj-biznes': 'Готовый бизнес'
}

HEADERS_TRANS = {
    'num_id_start': '№ п/п/ (№ скан)',
    'title': 'Заголовок',
    'address': 'Адресное описание',
    'area': 'Площадь с указанием ед. изм (кв.м /сот./га)',
    'price': 'Цена (01.1, тыс. руб.',
    'price_m2': 'Цена (01.1, тыс. руб. за кв. метр',
    'text': 'Текст объявления',
    'contacts': 'Контакт (телефон)',
    'seller_fullname': 'ФИО',
    'url': 'Ссылка на объявление',
}


class CustomExcelExporter(XlsxItemExporter):

    def __init__(self, file, **kwargs):
        super().__init__(file, join_multivalued=',', **kwargs)

    def serialize_field(self, field, name, value):
        name = HEADERS_TRANS.get(name, name)
        serializer = field.get('serializer', self._default_serializer)
        return serializer(value)
