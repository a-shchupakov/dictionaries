import csv
import argparse
import glob
import os


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, help='Analyze all txt''s in directory')
    return parser


def analyze_file(file_to_analyze, file_to_save):
    """
    Здесь происходит анализ данных и их сохранение в формате .csv
    :param file_to_analyze: Анализируемый файл
    :param file_to_save: Файл, в который будет записана статистика
    :return:
    """
    with open(file_to_analyze, 'r', newline='') as data:
        with open(file_to_save, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(('elements added', 'time'))
            for line in data:
                line = line[:-1]
                array = extract_list(line)
                added = line.split(' : ')[0]
                repeats = len(array)
                average_value = sum(map(float, array)) / repeats
                writer.writerow((added, average_value))


def extract_list(line):
    b_index = line.index('[')
    e_index = line.index(']')
    return (line[b_index+1:e_index]).split(', ')


def analyze_directory(directory_):
    for filename in glob.glob(os.path.join(directory_, '*.txt')):
        to_save = filename.replace('raw_results', 'final_results')
        to_save = to_save[:-3] + 'csv'
        save_dir = os.path.dirname(to_save)
        save_dir = os.path.normpath(save_dir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        analyze_file(file_to_analyze=filename, file_to_save=to_save)
        print('Saved to: ' + save_dir)


def main():
    parser = create_parser()
    args = parser.parse_args()

    directory = args.directory

    analyze_directory(directory)


if __name__ == '__main__':
    main()
