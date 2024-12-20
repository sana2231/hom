import sys
import re

def parse_multiline_comment(lines):
    in_comment = False
    for line in lines:
        if '<#' in line:
            in_comment = True
        elif '#>' in line:
            in_comment = False
            continue
        if in_comment:
            continue
    return

def parse_array(line):
    match = re.match(r'(\w+)\s*=\s*\((.*?)\)', line)
    if match:
        values = match.group(2).split(',')
        result = f'{match.group(1)} = [{", ".join(value.strip() for value in values)}]'
        return result
    return None

def parse_dictionary(line):
    match = re.match(r'(\w+)\s*=\s*\{(.*?)\}', line)
    if match:
        items = match.group(2).split(',')
        dict_items = []
        for item in items:
            key_value = item.split(':')
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip().strip('"')  # Удаляем кавычки из значений
                dict_items.append(f'{key} = "{value}"')  # Добавляем кавычки к строковым значениям
        result = f'{match.group(1)} = {{ {", ".join(dict_items)} }}'
        return result
    return None

def parse_constant_declaration(line):
    match = re.match(r'(\w+)\s*->\s*(\d+)', line)  # Обновлено для числовых значений
    if match:
        return match.group(1), match.group(2)  # Возвращаем имя и значение константы
    return None, None

def parse_constant_evaluation(line, constants):
    match = re.match(r'(\w+)\s*=\s*\$(\w+)\$', line)  # Обновлено для правильного распознавания
    if match:
        const_name = match.group(2)
        value = constants.get(const_name, const_name)  # Получаем значение из словаря или имя, если не найдено
        result = f'{match.group(1)} = {value}'
        return result
    return None

def convert_to_toml(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    toml_output = []
    
    constants = {}  # Словарь для хранения значений констант
    
    in_comment = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Проверка на многострочный комментарий
        if '<#' in stripped_line:
            in_comment = True
        
        if '#>' in stripped_line and in_comment:
            in_comment = False
            continue
        
        if in_comment or stripped_line == "":
            continue
        
        array_result = parse_array(stripped_line)
        if array_result:
            toml_output.append(array_result)
            continue
        
        dict_result = parse_dictionary(stripped_line)
        if dict_result:
            toml_output.append(dict_result)
            continue
        
        constant_decl_name, constant_decl_value = parse_constant_declaration(stripped_line)
        if constant_decl_name is not None:
            constants[constant_decl_name] = constant_decl_value  # Сохраняем значение в словаре
            toml_output.append(f'{constant_decl_name} = {constant_decl_value}')  # Записываем в выходной формат
            continue
        
        constant_eval_result = parse_constant_evaluation(stripped_line, constants)
        if constant_eval_result:
            toml_output.append(constant_eval_result)
            continue
        
        # Если ничего не распознано, выводим сообщение об ошибке
        print(f'Синтаксическая ошибка в строке: {line.strip()}', file=sys.stderr)

    return '\n'.join(toml_output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: py hw3.py <путь_к_файлу>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    
    try:
        toml_output = convert_to_toml(input_file_path)
        print(toml_output)
    except Exception as e:
        print(f'Ошибка: {e}', file=sys.stderr)
