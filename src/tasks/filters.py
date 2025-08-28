import django_filters
from .models import Task
from .documents import TaskDocument
from datetime import datetime
import re


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title', label='По названию')
    deadline = django_filters.CharFilter(method='filter_deadline', label='По дедлайну')

    def filter_title(self, queryset, name, value):
        """Фильтр по title через ElasticSearch"""
        es_results = TaskDocument.search().query("match", title=value).execute()
        task_ids = [hit.id for hit in es_results]
        return queryset.filter(id__in=task_ids)

    def filter_deadline(self, queryset, name, value):
        """
        Фильтр по дедлайну с поддержкой операторов (> < >= <= =).
        Автоматически определяет формат даты или datetime.
        """
        if not value:
            return queryset

        match = re.match(r'^\s*(>=|<=|>|<|=)?\s*(.+)$', value)
        if not match:
            return queryset.none()

        operator, date_str = match.groups()
        operator = operator or '='

        lookup_map = {
            '>': 'gt',
            '<': 'lt',
            '>=': 'gte',
            '<=': 'lte',
            '=': 'exact'
        }
        lookup = lookup_map[operator]

        try:
            dt = datetime.fromisoformat(date_str)
            field = 'deadline'
        except ValueError:
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                dt = d
                field = 'deadline__date'
            except ValueError:
                return queryset.none()

        return queryset.filter(**{f'{field}__{lookup}': dt})

    class Meta:
        model = Task
        fields = ['title', 'deadline']
