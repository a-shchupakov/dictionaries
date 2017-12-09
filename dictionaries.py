import copy
import queue

PRIME_LIST = [2, 3, 5, 7, 11, 13, 17, 23, 29, 37, 47,
              59, 73, 97, 127, 151, 197, 251, 313, 397,
              499, 631, 797, 1009, 1259, 1597, 2011, 2539,
              3203, 4027, 5087, 6421, 8089, 10193, 12853, 16193,
              20399, 25717, 32401, 40823, 51437, 64811, 81649,
              102877, 129607, 163307, 205759, 259229, 326617,
              411527, 518509, 653267, 823117, 1037059, 1306601,
              1646237, 2074129, 2613229, 3292489, 4148279, 5226491,
              6584983, 8296553, 10453007, 13169977, 16593127, 20906033,
              26339969, 33186281, 41812097, 52679969, 66372617,
              83624237, 105359939, 132745199, 167248483, 210719881,
              265490441, 334496971, 421439783, 530980861, 668993977,
              842879579, 1061961721, 1337987929, 1685759167, 2123923447,
              2675975881, 3371518343, 4247846927, 5351951779, 6743036717,
              8495693897, 10703903591, 13486073473, 16991387857,
              21407807219, 26972146961, 33982775741, 42815614441,
              53944293929, 67965551447, 85631228929, 107888587883,
              135931102921, 171262457903, 215777175787, 271862205833,
              342524915839, 431554351609, 543724411781, 685049831731,
              863108703229, 1087448823553, 1370099663459, 1726217406467,
              2174897647073, 2740199326961, 3452434812973, 4349795294267,
              5480398654009, 6904869625999, 8699590588571, 10960797308051,
              13809739252051, 17399181177241, 21921594616111, 27619478504183,
              34798362354533, 43843189232363, 55238957008387, 69596724709081,
              87686378464759, 110477914016779, 139193449418173,
              175372756929481, 220955828033581, 278386898836457,
              350745513859007, 441911656067171, 556773797672909,
              701491027718027, 883823312134381, 1113547595345903,
              1402982055436147, 1767646624268779, 2227095190691797,
              2805964110872297, 3535293248537579, 4454190381383713,
              5611928221744609, 7070586497075177, 8908380762767489,
              11223856443489329, 14141172994150357, 17816761525534927,
              22447712886978529, 28282345988300791, 35633523051069991,
              44895425773957261, 56564691976601587, 71267046102139967,
              89790851547914507, 113129383953203213, 142534092204280003,
              179581703095829107, 226258767906406483, 285068184408560057,
              359163406191658253, 452517535812813007, 570136368817120201,
              718326812383316683, 905035071625626043, 1140272737634240411,
              1436653624766633509, 1810070143251252131, 2280545475268481167,
              2873307249533267101, 3620140286502504283, 4561090950536962147,
              5746614499066534157, 7240280573005008577, 9122181901073924329,
              11493228998133068689, 14480561146010017169, 18446744073709551557]


class LinearSearchDict:
    """
    Словарь с линейным поиском
    """
    def __init__(self):
        self.__arr = []

    def __getitem__(self, key):
        return self._linear_search(key)

    def __setitem__(self, key, value):
        try:
            index = self._get_index(key)
            self.__arr[index] = (key, value)
        except KeyError:
            self.__arr.append((key, value))

    def items(self):
        temp = copy.deepcopy(self.__arr)
        return temp

    def pop(self, key):
        index = self._get_index(key)
        value = self.__arr[index][1]
        del self.__arr[index]
        return value

    def _get_index(self, key):
        for index in range(0, len(self.__arr)):
            if self.__arr[index][0] == key:
                return index
        raise KeyError

    def _linear_search(self, key):
        index = self._get_index(key)
        return self.__arr[index][1]


class BinarySearchDict:
    """
    Словарь с бинарным поиском на массиве
    В каждом элементе массива 0-ой индекс - ключ, 1-ый индекс - значение
    Словарь может содержать только объекты одного и того же класса
    """
    def __init__(self):
        self.__arr = []

    def __getitem__(self, key):
        index = BinarySearchDict._binary_search(self.__arr, key)
        return self.__arr[index][1]

    def __setitem__(self, key, value):
        if not self._is_same_types(key):
            raise TypeError('Incomparable types')
        if not len(self.__arr):
            self.__arr.append((key, value))
        try:
            index = BinarySearchDict._binary_search(self.__arr, key)
            self.__arr[index] = (key, value)
        except KeyError:
            self.__arr.append((key, value))
        finally:
            self.__arr.sort(key=lambda x: x[0])

    def items(self):
        temp = copy.deepcopy(self.__arr)
        return temp

    def pop(self, key):
        index = BinarySearchDict._binary_search(self.__arr, key)
        value = self.__arr[index][1]
        del self.__arr[index]
        self.__arr.sort(key=lambda x: x[0])
        return value

    def _is_same_types(self, key):
        if self.__arr:
            type_of = type(self.__arr[0][0])
            return isinstance(key, type_of)
        return True

    @staticmethod
    def _binary_search(arr, key):
        i = 0
        j = len(arr) - 1
        while i < j:
            mid_point = int((i + j) / 2)
            if key > arr[mid_point][0]:
                i = mid_point + 1
            else:
                j = mid_point
        if arr[j][0] == key:
            return j
        else:
            raise KeyError


class TreeNode:
    """
    Вспомогательный класс, отвечающий за узел бинарного дерева
    """
    def __init__(self):
        self.key = None
        self.value = None
        self.left = None
        self.right = None
        self.parent = None


class BinaryTreeDict:
    """
    Словарь, построенный с помощью бинарного дерева
    Может содержать в качестве ключей только объекты одного и того же типа
    """
    def __init__(self):
        self.__hill = TreeNode()

    def __getitem__(self, key):
        node = BinaryTreeDict._search(self.__hill, key)
        return node.value

    def __setitem__(self, key, value):
        if not self._is_same_types(key):
            raise TypeError('Incomparable types')
        try:
            node = BinaryTreeDict._search(self.__hill, key)
            node.value = value
        except KeyError:
            return self._add_element(key, value)

    def pop(self, key):
        node = BinaryTreeDict._search(self.__hill, key)
        if node.left is None and node.right is None:
            # Случай, когда удаляемый элемент - лист дерева
            if node.key < node.parent.key:
                node.parent.left = None
            else:
                node.parent.right = None
        elif node.left is None and node.right is not None:
            # Случай, когда удаляемый элемент имеет одно поддерево
            if node.parent is None:
                if node.left is None:
                    self.__hill = node.right
                else:
                    self.__hill = node.left
            elif node.key < node.parent.key:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
            node.right.parent = node.parent
        elif node.left is not None and node.right is not None:
            # Случай, когда удаляемый элемент имеет два поддерева
            min_ = BinaryTreeDict.min(node.right)
            if min_.left is None and min_.right is None:
                min_.parent.left = None
                node.key = min_.key
                node.value = min_.value
            else:
                min_.parent.left = min_.right
                min_.right.parent = min_.parent
                node.key = min_.key
                node.value = min_.value

    def _add_element(self, key, value):
        node = self.__hill
        source = None
        if node.key is None:
            node.key = key
            node.value = value
            return
        while True:
            if key < node.key:
                if node.left is None:
                    source = type(node)()
                    node.left = source
                    break
                node = node.left
            else:
                if node.right is None:
                    source = type(node)()
                    node.right = source
                    break
                node = node.right
        source.key = key
        source.value = value
        source.parent = node

    def items(self):
        t_queue = queue.Queue()
        t_queue.put(self.__hill)
        results = []
        while not t_queue.empty():
            node = t_queue.get()
            if node.left is not None:
                t_queue.put(node.left)
            if node.right is not None:
                t_queue.put(node.right)
            results.append((node.key, node.value))
        return results

    def _is_same_types(self, key):
        source = self.__hill.key
        if source is not None:
            return isinstance(key, type(source))
        return True

    @staticmethod
    def min(root):
        """
        Метод возвращает экземпляр класса TreeNode
        с минимальным значением ключа в выбранной части поддерева
        """
        node = root
        while node is not None and node.left is not None:
            node = node.left
        return node

    @staticmethod
    def _search(node, key):
        if key is None or node is None or node.key is None:
            raise KeyError
        if key == node.key:
            return node
        if key < node.key:
            return BinaryTreeDict._search(node.left, key)
        else:
            return BinaryTreeDict._search(node.right, key)


class BalancedTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class BalancedBinaryTreeDict:
    def __init__(self):
        self.hill = None

    def __getitem__(self, key):
        node = BalancedBinaryTreeDict.search(self.hill, key)
        return node.value

    def __setitem__(self, key, value):
        if not self.is_same_types(key):
            raise TypeError('Incomparable types')
        try:
            node = BalancedBinaryTreeDict.search(self.hill, key)
            node.value = value
        except KeyError:
            if self.hill is None:
                self.hill = BalancedTreeNode(key, value)
                return
            self.add_element(self.hill, key, value)

    def items(self):
        """
        Метод возвращает все пары ключ-значение
        """
        t_queue = queue.Queue()
        t_queue.put(self.hill)
        results = []
        while not t_queue.empty():
            node = t_queue.get()
            if node.left is not None:
                t_queue.put(node.left)
            if node.right is not None:
                t_queue.put(node.right)
            results.append((node.key, node.value))
        return results

    def is_same_types(self, key):
        """
        Метод определяет, совпадают ли типы ключей в словаре с типом объекта key
        """
        source = self.hill
        if source is not None:
            return isinstance(key, type(source.key))
        return True

    def add_element(self, node, key, value):
        if node is None:
            return BalancedTreeNode(key, value)
        else:
            if key < node.key:
                node.left = self.add_element(node.left, key, value)
            else:
                node.right = self.add_element(node.right, key, value)
        return self.balance(node)

    @staticmethod
    def search(node, key):
        if key is None or node is None or node.key is None:
            raise KeyError
        if key == node.key:
            return node
        if key < node.key:
            return BalancedBinaryTreeDict.search(node.left, key)
        else:
            return BalancedBinaryTreeDict.search(node.right, key)

    def balance_factor(self, node):
        return self.get_height(node.right) - self.get_height(node.left)

    def get_height(self, node):
        return node.height if node else 0

    def fix_height(self, node):
        h1 = self.get_height(node.left)
        h2 = self.get_height(node.right)
        node.height = max(h1, h2) + 1

    def rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node

        self.fix_height(node)
        self.fix_height(left)

        if node.key == self.hill.key:
            self.hill = left

        return left

    def rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node

        self.fix_height(node)
        self.fix_height(right)

        if node.key == self.hill.key:
            self.hill = right

        return right

    def balance(self, node):
        self.fix_height(node)
        if self.balance_factor(node) == 2:
            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        if self.balance_factor(node) == -2:
            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        return node


class HashDict:
    def __init__(self, start_capacity=1, step=1, load_factor=0.72, hash_function=hash, prime_ext=False):
        """
        :param start_capacity: Стартовая длина масива
        :param step: Шаг в линейном пробировании
        :param load_factor: Показатель заполненности, по достижении которого таблица расширится
        :param hash_function: Функция, вычисляющая хеш. По умолчанию используется встроенная
        :param prime_ext: Модификатор расширения основого массива (в качестве длины использует простые числа)
        """
        if load_factor > 1.0:
            raise ValueError("Invalid load factor")
        if prime_ext:
            gen = prime_generator()
            self.next_ext_number = (lambda: next(gen))
        self.load_factor = load_factor
        self.count = 0
        self.capacity = start_capacity
        self.step = step
        self.array = [None] * start_capacity
        self.deleted_flags = [False] * start_capacity
        HashDict.hash_func = hash_function

    def __getitem__(self, item):
        return self.search(item)

    def __setitem__(self, key, value):
        self.add_element(key, value)

    def add_element(self, key, value):
        self.enlarge()
        key_hash = HashDict.hash_func(key)
        index = self.hash_index(key_hash)
        for i in range(0, self.capacity):
            check_index = (index + i * self.step) % self.capacity
            if self.deleted_flags[check_index] or self.array[check_index] is None:
                self.array[check_index] = (key, value)
                self.deleted_flags[check_index] = False
                self.count += 1
                break

            elif self.array[check_index] is not None:
                if self.array[check_index][0] == key:
                    self.array[check_index] = (key, value)

    def search(self, key):
        key_hash = HashDict.hash_func(key)
        index = self.hash_index(key_hash)
        for i in range(0, self.capacity):
            check_index = (index + i * self.step) % self.capacity
            if self.deleted_flags[check_index]:
                continue

            if self.array[check_index] is None:
                break

            if self.array[check_index][0] == key:
                return self.array[check_index][1]
        raise KeyError

    def pop(self, key):
        key_hash = HashDict.hash_func(key)
        index = self.hash_index(key_hash)
        for i in range(0, self.capacity):
            check_index = (index + i * self.step) % self.capacity
            if self.deleted_flags[check_index]:
                continue

            if self.array[check_index] is None:
                break

            if self.array[check_index][0] == key:
                self.deleted_flags[check_index] = True
                self.count -= 1
                return self.array[check_index][1]
        raise KeyError

    def items(self):
        items = []
        for i in range(0, self.capacity):
            if self.deleted_flags[i] or self.array[i] is None:
                continue
            items.append((self.array[i][0], self.array[i][1]))
        return items

    def enlarge(self):
        if self.count / self.capacity < self.load_factor:
            return
        items_to_copy = self.items()
        new_capacity = self.next_ext_number()
        self.capacity, self.array, self.deleted_flags = new_capacity, [None] * new_capacity, [False] * new_capacity
        self.count = 0
        for item in items_to_copy:
            self.add_element(*item)

    def next_ext_number(self):
        return len(self.array) * 2

    def hash_index(self, hash_value):
        return hash_value & (self.capacity - 1)

    @staticmethod
    def hash_func(key):
        return 0


def prime_generator():
    for prime in PRIME_LIST:
        yield prime


def main():
    pass


if __name__ == '__main__':
    main()
