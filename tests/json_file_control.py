import json


def load_json():
    try:
        with open("json_file_control.json", "r", encoding="utf-8") as file:
            content = file.read().strip()
            return json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(data):
    with open("json_file_control.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def print_json_data():
    data = load_json()
    print('\n[ JSON Data ]')
    print(json.dumps(data, indent=4, ensure_ascii=False))


def key_value_input(dvsn):
    while True:
        print(f'\n{dvsn} 입력')
        text = input('>>> ')
        if not text:
            print('\n빈 값은 입력될 수 없습니다.')
        else:
            return text


def add_json_data():
    data = load_json()
    key = key_value_input("Key")
    value = key_value_input("Value")
    data[key] = value
    save_json(data)
    print('\nJSON Data 추가 성공')
    print_json_data()


def del_json_data():
    data = load_json()
    key = key_value_input("Key")
    del data[key]
    save_json(data)
    print('\nJSON Data 삭제 성공')
    print_json_data()


while True:
    print('\n작업 선택')
    print('0: 종료')
    print('1: JSON Data 출력')
    print('2: JSON Data 추가')
    print('3: JSON Data 삭제')
    user_input = input('>>> ').strip()
    if user_input == '0':
        break
    elif user_input == '1':
        print_json_data()
    elif user_input == '2':
        add_json_data()
    elif user_input == '3':
        del_json_data()
    else:
        print('\n올바른 번호를 입력하세요')
