import timeit
import datetime
import glob
import os
import argparse
from shutil import copy2
from random import shuffle
from dictionaries import *


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--summary', type=int)
parser.add_argument('-r', '--repeats', type=int)
parser.add_argument('--step', type=int)
parser.add_argument('--data_path', type=str, help='Data to test')
parser.add_argument('--save_path', type=str, help='Dir to save')

parser.add_argument('--d1', action='store_true', help='Test built-in dict')
parser.add_argument('--d2', action='store_true', help='Test hash hand-made dict')
parser.add_argument('--d3', action='store_true', help='Test AVL tree dict')
parser.add_argument('--d4', action='store_true', help='Test binary tree dict')
parser.add_argument('--d5', action='store_true', help='Test linear-search dict')
parser.add_argument('--d6', action='store_true', help='Test binary-search dict')

parser.add_argument('--test_hash', action='store_true', help='Test hash dict with different options')

parser.add_argument('-a', '--add', action='store_true', help='Test add method')
parser.add_argument('-g', '--get', action='store_true', help='Test get method')

args_ = parser.parse_args()

SUMMARY = args_.summary
REPEATS = args_.repeats
STEP = args_.step
DATA_PATH = args_.data_path
SAVE_PATH = args_.save_path

if not SUMMARY or not REPEATS or not STEP:
    print('Wrong test definition')
    exit()

if not DATA_PATH:
    print('No data to test were given')
    exit()

if not SAVE_PATH:
    print('Please select directory for the results')
    exit()

CURRENT_ADD_SAVE_PATH = SAVE_PATH + '/add/' + 's={},r={},step={}/'.format(SUMMARY, REPEATS, STEP)
CURRENT_GET_SAVE_PATH = SAVE_PATH + '/get/' + 's={},r={},step={}/'.format(SUMMARY, REPEATS, STEP)

d1 = args_.d1
d2 = args_.d2
d3 = args_.d3
d4 = args_.d4
d5 = args_.d5
d6 = args_.d6

TEST_HASH = args_.test_hash

ADD = args_.add
GET = args_.get


def measure(func):
    """Декоратор для замера времени выполнения"""
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        end = timeit.default_timer()
        return end - start
    return wrapper


def import_data(path, count):
    """
    Сохраняет необходимое количество значений из выбранного текстового файла в лист
    :param path: Текстовый файл
    :param count: Количество элементов
    :return:
    """
    data = []
    success = False
    with open(path, 'r') as file:
        for line in file:
            data.append(line[:-1])
            if len(data) == count:
                success = True
                break
    if not success:
        raise EOFError()
    return data


def fill_the_dict(dict_to_measure, data_path, to_add, repeats, file_to_save,
                  dict_creating_args=tuple(),
                  dict_creating_kwargs=dict()):
    """
    В заданный словарь добавляет заданное количество элементов заданное количество раз
    :param dict_to_measure: Тестируемый словарь
    :param data_path: Файл с данными, которые используются как ключи
    :param to_add: Количество добавляемых элементов
    :param repeats: Количество повторений
    :param file_to_save: Текстовый файл для сохранения результатов
    :param dict_creating_args: Позиционные аргументы для конструктора словаря
    :param dict_creating_kwargs: Именнованные аргументы для конструктора словаря
    :return:
    """
    data = import_data(data_path, to_add)
    results = []
    for _ in range(0, repeats):
        new_dict = dict_to_measure(*dict_creating_args, **dict_creating_kwargs)
        results.append(add_to_dict(new_dict, data))

    if file_to_save:
        file_to_save.write(str(to_add) + ' : ' + str(results) + '\n')


def extract_the_keys(dict_to_measure, data_path, to_add, repeats, file_to_save,
                     dict_creating_args=tuple(),
                     dict_creating_kwargs=dict()):
    """
    Извлекает все ключи из словаря, предварительно добавив их в него (все ключи гарантированно находятся в словаре)
    :param dict_to_measure: Тестируемый словарь
    :param data_path: Файл с данными, которые используются как ключи
    :param to_add: Количество добавляемых элементов
    :param repeats: Количество повторений
    :param file_to_save: Текстовый файл для сохранения результатов
    :param dict_creating_args: Позиционные аргументы для конструктора словаря
    :param dict_creating_kwargs: Именнованные аргументы для конструктора словаря
    :return:
    """
    data = import_data(data_path, to_add)
    results = []
    new_dict = dict_to_measure(*dict_creating_args, **dict_creating_kwargs)

    for item in data:
        new_dict[item] = 1

    for _ in range(0, repeats):
        shuffle(data)
        results.append(get_from_dict(new_dict, data))

    if file_to_save:
        file_to_save.write(str(to_add) + ' : ' + str(results) + '\n')


@measure
def add_to_dict(dict_, data):
    for item in data:
        dict_[item] = 1


@measure
def get_from_dict(dict_, data):
    for item in data:
        dict_[item]


def test_dict_method(dict_to_measure, data_path, dir_to_save, summary, repeats, step,
                     test_method=None, is_warm_up=False, note='',
                     dict_creating_args=tuple(), dict_creating_kwargs=dict()):
    """
    Тестирует заданный словарь:
        Здесь происходит вызов метода test_method с увеличением добавлямых элементов на заданный шаг
    :param dict_to_measure: Тестируемый словарь
    :param data_path: Файл с данными, которые используются как ключи
    :param dir_to_save: Директория для сохранения результатов
    :param summary: Общее количество добавлямых элементов
    :param repeats: Количество повторений
    :param step: Величина шага
    :param is_warm_up: Флаг, указывающий, является ли запуск "прогревочным" (в этом случае результаты не сохраняютяся)
    :param note: Заметка, которая будет добавлена к файлу в который сохранятся результаты
    :param test_method: Тестируемый метод (напр. fill_the_dict)
    :param dict_creating_args: Позиционные ргументы, которые будут переданы конструктору словаря
    :param dict_creating_kwargs: Именнованные аргументы, которые будут переданы констркутору словаря
    :return:
    """
    file_name = None
    if not is_warm_up:
        time = datetime.datetime.now()
        print('Testing {} on '.format(test_method.__name__) + dict_to_measure.__name__ + ' : ' + str(time))
        file_name = dir_to_save + dict_to_measure.__name__ + '.txt'
    if note:
        file_name = file_name[:-4] + '_{}'.format(note) + '.txt'

    if not is_warm_up:
        create_missing_directory(file_name)
        file = open(file_name, 'w')
    else:
        file = None

    for i in range(step, summary + 1, step):
        test_method(dict_to_measure, data_path, i, repeats, file,
                    dict_creating_args=dict_creating_args, dict_creating_kwargs=dict_creating_kwargs)

    if file:
        file.close()


def back_up_previous_results(directory_):
    for file in glob.glob(os.path.join(directory_, '*.txt')):
        index = file.rfind('/')
        to_add = 'previous_back_up/'
        dst = file[:index+1] + to_add + file[index+1:]
        create_missing_directory(dst)
        copy2(file, dst)


def create_missing_directory(path_):
    save_dir = os.path.dirname(path_)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


def warm_up(dictionary, times=5, dict_creating_args=tuple(), dict_creating_kwargs=dict()):
    """
    "Прогревочный" запуск тестируемых методов
    :param dictionary: Тестируемый словарь
    :param times: Количество запусков
    :param dict_creating_args: Позиционные ргументы, которые будут переданы конструктору словаря
    :param dict_creating_kwargs: Именнованные аргументы, которые будут переданы констркутору словаря
    :return:
    """
    print('Warm up on ' + dictionary.__name__)
    if ADD:
        for _ in range(0, times):
            test_dict_method(dictionary, DATA_PATH, None, 1000, 5, 200, test_method=fill_the_dict, is_warm_up=True,
                             dict_creating_args=dict_creating_args, dict_creating_kwargs=dict_creating_kwargs)
    if GET:
        for _ in range(0, times):
            test_dict_method(dictionary, DATA_PATH, None, 1000, 5, 200, test_method=extract_the_keys, is_warm_up=True,
                             dict_creating_args=dict_creating_args, dict_creating_kwargs=dict_creating_kwargs)
    print('End of warm up')


def test_selected_dicts():
    """Тестирует выбранные словари"""
    if ADD:
        back_up_previous_results(CURRENT_ADD_SAVE_PATH)
    if GET:
        back_up_previous_results(CURRENT_GET_SAVE_PATH)
    if d1:
        test_dict(dict)
    if d2:
        test_dict(HashDict)
    if d3:
        test_dict(BalancedBinaryTreeDict)
    if d4:
        test_dict(BinaryTreeDict)
    if d5:
        test_dict(LinearSearchDict)
    if d6:
        test_dict(BinarySearchDict)


def test_hash_dict():
    """Тестирует производительность хэш-таблицы с различными настройками"""
    test_dict(HashDict, note='standard', dict_creating_kwargs={'load_factor': 0.72,
                                                               'hash_function': hash,
                                                               'prime_ext': False})

    # test_dict(HashDict, note='bad_hash', dict_creating_kwargs={'load_factor': 0.72,
    #                                                           'hash_function': lambda x: len(str(x)),
    #                                                           'prime_ext': False})

    # test_dict(HashDict, note='const_hash', dict_creating_kwargs={'load_factor': 0.72,
    #                                                             'hash_function': lambda x: 1,
    #                                                             'prime_ext': False})

    test_dict(HashDict, note='low_load_factor', dict_creating_kwargs={'load_factor': 0.4,
                                                                      'hash_function': hash,
                                                                      'prime_ext': False})

    # test_dict(HashDict, note='prime_ext', dict_creating_kwargs={'load_factor': 0.72,
    #                                                            'hash_function': hash,
    #                                                            'prime_ext': True})

    # test_dict(HashDict, note='low_load_f_prime_ext', dict_creating_kwargs={'load_factor': 0.4,
    #                                                                       'hash_function': hash,
    #                                                                       'prime_ext': True})


def test_dict(dictionary, note='', dict_creating_args=tuple(), dict_creating_kwargs=dict()):
    warm_up(dictionary)
    if ADD:
        test_dict_method(dictionary, DATA_PATH, CURRENT_ADD_SAVE_PATH,
                         SUMMARY, REPEATS, STEP, test_method=fill_the_dict, note=note,
                         dict_creating_args=dict_creating_args, dict_creating_kwargs=dict_creating_kwargs)
    if GET:
        test_dict_method(dictionary, DATA_PATH, CURRENT_GET_SAVE_PATH,
                         SUMMARY, REPEATS, STEP, test_method=extract_the_keys, note=note,
                         dict_creating_args=dict_creating_args, dict_creating_kwargs=dict_creating_kwargs)


def main():
    try:
        import_data(DATA_PATH, SUMMARY)
    except EOFError:
        print('Not enough data to test')
        exit()
    start = datetime.datetime.today()
    test_selected_dicts()
    if TEST_HASH:
        test_hash_dict()
    end = datetime.datetime.today()
    print('Time passed: ' + str(end - start))


if __name__ == '__main__':
    main()
