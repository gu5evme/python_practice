from statistics import mean, median
from rich.console import Console
from rich.table import Table

def eval_usage_type(mean_value, median_value) -> str:
    """
    Определяет тип нагрузки

    :param mean_value:
    :param median_value:
    :return:
    """

    if mean_value < (median_value * 0.75):
        return "lowering"
    elif mean_value > (median_value * 1.25):
        return "flapping"
    else:
        return "stable"


def eval_intensity(median_value) -> str:
    """
    Определяет интенсивность использования

    :param median_value:
    :return:
    """

    if 0 < median_value <= 30:
        return "low"
    elif 30 < median_value <= 60:
        return "moderate"
    elif 60 < median_value <= 90:
        return "high"
    elif median_value > 90:
        return "extreme"


def make_decision(usage_type, intensivity) -> str:
    """
    Выдает решение по ресурсу на основе типа нагрузки и интенсивности использования

    :param usage_type:
    :param intensivity:
    :return:
    """

    is_intensity_low_and_usage_type_lowering = True if intensivity == "low" and usage_type == "lowering" else False
    is_intensity_low_and_usage_type_stable = True if intensivity == "low" and usage_type == "stable" else False
    is_intensity_low_and_usage_type_flapping = True if intensivity == "low" and usage_type == "flapping" else False

    is_intensity_moderate_and_usage_type_lowering = True if intensivity == "moderate" and usage_type == "lowering" else False
    is_intensity_moderate_and_usage_type_stable = True if intensivity == "moderate" and usage_type == "stable" else False
    is_intensity_moderate_and_usage_type_flapping = True if intensivity == "moderate" and usage_type == "flapping" else False

    is_intensity_high_and_usage_type_lowering = True if intensivity == "high" and usage_type == "lowering" else False
    is_intensity_high_and_usage_type_stable = True if intensivity == "high" and usage_type == "stable" else False
    is_intensity_high_and_usage_type_flapping = True if intensivity == "high" and usage_type == "flapping" else False

    is_intensity_overload_and_usage_type_lowering = True if intensivity == "extreme" and usage_type == "lowering" else False
    is_intensity_overload_and_usage_type_stable = True if intensivity == "extreme" and usage_type == "stable" else False
    is_intensity_overload_and_usage_type_flapping = True if intensivity == "extreme" and usage_type == "flapping" else False

    if is_intensity_low_and_usage_type_lowering or is_intensity_low_and_usage_type_stable or is_intensity_low_and_usage_type_flapping or is_intensity_moderate_and_usage_type_lowering:
        return "delete resource"
    elif is_intensity_moderate_and_usage_type_stable or is_intensity_moderate_and_usage_type_flapping or is_intensity_high_and_usage_type_lowering or is_intensity_high_and_usage_type_stable:
        return "normal using"
    elif  is_intensity_high_and_usage_type_flapping or is_intensity_overload_and_usage_type_lowering or is_intensity_overload_and_usage_type_stable or is_intensity_overload_and_usage_type_flapping:
        return "extend resource"
    else:
        return "unknown"


def parse_input_to_dict(input_data) -> dict:
    """
    Формирует структурированный словарь на основе сырыы данных мониторинга

    На входе ожидается строка строки вида:

    Название команды|(Ресурс,Измерение ресурса,Дата и время сбора статистики,Загрузка ресурса);
    (Ресурс,Измерение ресурса,Дата сбора статистики,Загрузка ресурса)$Название команды|(Ресурс,
    Измерение ресурса,Дата сбора статистики,Загрузка ресурса);(Ресурс,Измерение ресурса,
    Дата сбора статистики,Загрузка ресурса)

    Правила форматирования входной строки:
    - Команды и описание их ресурсов отделяются при помощи разделителя "$"
    - Название команды от ресурсов команды отделяется при помощи разделителя "|"
    - Ресурсов команды перечислены в круглых скобках и отделяются при помощи разделителя ";"
    - Первый элемент в скобках — ID ресурса
    - Второй элемент в скобках — Измерение ресурса (CPU, RAM или NetFlow)
    - Третий элемент в скобках — Дата и время сбора статистики
    - Четвертый элемент в скобках — Загрузка ресурса в процентах (от 0 до 100)

    В результате формируется словарь вида:
    {'Название команды': {'Название ресурса': {'Измерение ресурса': ['значение 1', 'значение N']}}

    Пример
    envisioneer rich mindshare': {'SZY1417': {'CPU': ['51', '32']}}}

    :param input_data:
    :return: resources
    """
    resources = {}
    command_data_list = input_data.split("$")

    for command_data_item in command_data_list:

        command_name, command_resources = command_data_item.split("|")
        resources.setdefault(command_name, {})

        for resource in command_resources.split(";"):
            id, measurement, timestamp, value = resource.strip("()").split(",")
            resources[command_name].setdefault(id, {})
            resources[command_name][id].setdefault(measurement, []).append(int(value))

    return resources


def evaluate_monitoring_values(resources: dict) -> dict:
    """
    Формирует словарь с аналитикой на основе словаря с данными мониторинга

    Принимает словарь вида словарь вида:
    {'Название команды': {'Название ресурса': {'Измерение ресурса': ['значение 1', 'значение N']}}

    Возвращает словарь вида:
    {'Название команды':
      {'Название ресурса':
        {'Измерение ресурса':
           {'Среднее значение': значение,
           'Медиана': значение,
           'Тип нагрузки': значение,
           'Интенсивность использования': значение
        }
      }
    }

    Пример
    {'envisioneer rich mindshare': {'SZY1417': {'CPU': {'mean': 51.645, 'mediana': 53, 'usage_type': 'Stable', 'intensivity': 'Medium'}}}}

    :param resources:
    :return: analytics
    """

    analytics = {}

    for command_name, resource_ids in resources.items():
        analytics[command_name] = {}
        for resource_id, measurements in resource_ids.items():
            analytics[command_name][resource_id] = {}
            for measurement_name, values in measurements.items():

                mean_value = mean(values)
                median_value = median(values)
                usage_type = eval_usage_type(mean_value, median_value)
                intensity = eval_intensity(median_value)

                analytics[command_name][resource_id][measurement_name] = {
                    "mean": mean_value,
                    "mediana": median_value,
                    "usage_type": usage_type,
                    "intensivity": intensity
                }

    return analytics


def generate_report(analytics: dict):
    """
    Вывод отчета о ресурсах в консоль в виде таблиц на оснвое данных словаря аналитики

    :param analytics:
    :return:
    """

    console = Console()

    for command_name, resources in analytics.items():

        table = Table(title=command_name, title_justify="left")
        table.add_column("Resource")
        table.add_column("Dimension")
        table.add_column("Mean")
        table.add_column("Mediana")
        table.add_column("Usage type")
        table.add_column("Intensivity")
        table.add_column("Decision")

        for resource_id, analytics_data in resources.items():
            for measurement_name, values in analytics_data.items():
                mean_value, median_value, usage_type, intensivity = values.values()
                decision = make_decision(usage_type, intensivity)
                table.add_row(resource_id, measurement_name, str(mean_value), str(median_value), usage_type, intensivity, decision)

        console.print(table)


def main():
    input_data = input()
    resources = parse_input_to_dict(input_data)
    analytics = evaluate_monitoring_values(resources)
    generate_report(analytics)


if __name__ == '__main__':
    main()
