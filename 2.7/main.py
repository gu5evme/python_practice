if __name__ == '__main__':

    branch_name = input("Название ветки: ").capitalize()
    test_pass_result = int(input("Результат прохождения тестов: "))
    coverage_diff_percent = float(input("Изменение coverage: "))
    approve_count = int(input("Количество approve: "))

    is_test_pass = test_pass_result == 1
    is_enough_approve = approve_count >= 3
    is_coverage_grow = coverage_diff_percent > 0

    if branch_name in ("Staging", "Development"):
        if is_test_pass and is_coverage_grow and (coverage_diff_percent > 5 or (is_enough_approve and coverage_diff_percent <= 5)):
            print(f"Внимание! Код из {branch_name} отправлен в релиз!")
        else:
            print(f"Код из {branch_name} с результатами тесты: {is_test_pass}, coverage: {coverage_diff_percent}%, approve: {approve_count} в релиз не попадает")
    else:
        print(f"В ветке {branch_name} непроверенный код, пропускаем")
