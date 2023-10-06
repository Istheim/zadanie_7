import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='data_pay', lookup_expr='gte', label='Минимальная дата оплаты')
    max_date = django_filters.DateFilter(field_name='data_pay', lookup_expr='lte', label='Максимальная дата оплаты')
    course = django_filters.CharFilter(field_name='pay_course__title', lookup_expr='icontains', label='Курс')
    lesson = django_filters.CharFilter(field_name='pay_lesson__title', lookup_expr='icontains', label='Урок')
    payment_method = django_filters.CharFilter(field_name='payment_method', label='Способ оплаты')

    class Meta:
        model = Payment
        fields = []
