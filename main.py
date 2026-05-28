import os
import argparse
import hashlib

def get_file_hash(file_path):
    # Создаем объект хэширования MD5
    hasher = hashlib.md5()
    try:
        # Открываем файл в режиме чтения бинарных данных ('rb')
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        # Возвращаем уникальный "отпечаток" файла
        return hasher.hexdigest()
    except Exception:
        # Если файл нельзя прочитать (например, нет прав) — возвращаем пустоту
        return None

def main():
    # Настраиваем прием аргументов из командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("path")# путь к папке, который мы ждем от пользователя
    args = parser.parse_args()
    target_path = args.path
    # Проверка: существует ли вообще такой путь на диске
    if not os.path.exists(target_path):
        print("Путь не найден.")
        return
    # Словарь для хранения хэшей (ключ - хэш, значение - путь)
    hashes = {}
    # Список для найденных дубликатов
    duplicates = []

    print(f"Сканирую папку: {target_path}...")

# Этап 1: Сначала получим список всех файлов и отсортируем их
    all_files_list = []
    for root, dirs, files in os.walk(target_path):
        for file in files:
            all_files_list.append(os.path.join(root, file))
    
    # Сортируем: короткие имена (без "копия") пойдут в начало списка
    all_files_list.sort(key=len)

    for file_path in all_files_list:
        file_hash = get_file_hash(file_path)
        if not file_hash:
            continue
            
        if file_hash in hashes:
            duplicates.append(file_path)
        else:
            hashes[file_hash] = file_path
            print(f"✅ Оригинал: {os.path.basename(file_path)}")

    # Этап 2: Удаляем дубликаты
    for file_path in duplicates:
        # Проверяем, есть ли в имени "копия"
        if "копия" in file_path.lower():
            print(f"⚠️ Удаляю дубликат (копию): {file_path}")
            #os.remove(file_path) # РАСКОММЕНТИРУЙ ДЛЯ УДАЛЕНИЯ
        else:
            print(f"ℹ️ Файл {file_path} является дубликатом, но не содержит слова 'копия', пропускаю.")

# И в самом конце файла обязательно должны быть эти две строки:
if __name__ == "__main__":
    main()