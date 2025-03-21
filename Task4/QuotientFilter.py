import mmh3


class QuotientFilter:
    def __init__(self, size, remainder_bits, seed=None):
        self.size = size
        self.remainder_bits = remainder_bits
        self.table = [None] * size
        self.occupied = [False] * size  # Q-bit: каноническая ячейка занята
        self.shift = [False] * size  # S-bit: элемент вставлен не в свою каноническую ячейку
        self.continuation = [False] * size  # C-bit: элемент является продолжением
        if seed is None:
            from random import randint
            self.seed = randint(1, 100)
        else:
            self.seed = seed

    def _hash(self, x):
        h = mmh3.hash(x, seed=self.seed)
        quotient = h % self.size
        remainder = h % (2 ** self.remainder_bits)
        return quotient, remainder

    def _increment(self, index):
        return (index + 1) % self.size

    def _find_run_start(self, q):
        # Находит индекс начала run для заданного bucket q
        # Если слот q не сдвинут (shift=False), то run начинается непосредственно в q
        # Иначе, мы ищем начало кластера, а затем «продвигаемся» по запускам до нужного bucket

        # Если элемент в канонической ячейке q не сдвинут, то его run начинается в q
        if not self.shift[q]:
            return q

        # Найдём начало кластера: двигаемся назад, пока не найдём элемент, у которого shifted == False
        i = q
        while self.shift[i]:
            i = (i - 1) % self.size
            # В случае полного цикла выходим, чтобы избежать зацикливания
            if i == q:
                break

        # Теперь продвигаемся вперёд по «запускам». Каждый run начинается с ячейки, где continuation == False
        run_index = i
        bucket = i
        while bucket != q:
            # Переходим к следующему слоту.
            run_index = self._increment(run_index)
            # Пропускаем все элементы, являющиеся продолжением текущего run
            while self.continuation[run_index]:
                run_index = self._increment(run_index)
            bucket = self._increment(bucket)
        return run_index

    def _shift_right(self, start_index):
        # Находит ближайшую свободную ячейку, начиная с start_index,
        # и сдвигает все элементы между start_index и этой свободной ячейкой вправо.
        # При сдвиге устанавливается S-бит (shifted=True)

        i = start_index
        # Поиск первого свободного слота
        while self.occupied[i]:
            i = self._increment(i)
            if i == start_index:
                raise Exception("Фильтр заполнен!")
        # Сдвиг элементов вправо от найденного места до start_index
        while i != start_index:
            prev = (i - 1) % self.size
            self.table[i] = self.table[prev]
            self.occupied[i] = True
            # При сдвиге элемент уже точно не находится в канонической ячейке
            self.shift[i] = True
            self.continuation[i] = self.continuation[prev]
            i = prev
        # Очищаем ячейку для вставки нового элемента
        self.table[start_index] = None
        self.occupied[start_index] = False
        self.shift[start_index] = False
        self.continuation[start_index] = False
        return start_index

    def insert(self, x):
        q, r = self._hash(x)
        # Обязательно отмечаем, что в канонической ячейке q должен быть установлен Q-бит
        self.occupied[q] = True
        # Если каноническая ячейка пуста, вставляем элемент напрямую
        if self.table[q] is None:
            self.table[q] = r
            self.shift[q] = False
            self.continuation[q] = False
            return

        # Находим начало run для bucket q
        run_start = self._find_run_start(q)
        # Выбираем позицию для вставки
        # Здесь для простоты мы вставляем элемент в конец run
        pos = run_start
        while True:
            next_pos = self._increment(pos)
            # Если следующий слот либо пуст, либо не является продолжением (то есть конец run)
            if not self.occupied[next_pos] or not self.continuation[next_pos]:
                break
            pos = next_pos
        insertion_index = self._increment(pos)
        # Сдвигаем элементы вправо, чтобы освободить место для нового элемента
        self._shift_right(insertion_index)
        # Вставляем новый остаток
        self.table[insertion_index] = r
        self.occupied[insertion_index] = True
        # Если элемент вставлен не в свой канонический bucket, S-бит устанавливается в True
        self.shift[insertion_index] = (insertion_index != q)
        # Если позиция вставки не является началом run, то устанавливаем C-бит
        self.continuation[insertion_index] = (insertion_index != run_start)

    def check(self, x):
        q, r = self._hash(x)
        # Если каноническая ячейка не занята, элемент точно отсутствует
        if not self.occupied[q]:
            return False
        # Находим начало run для bucket q
        run_start = self._find_run_start(q)
        pos = run_start
        # Последовательно перебираем все элементы run
        while True:
            if self.table[pos] == r:
                return True
            next_pos = self._increment(pos)
            # Если следующий слот пуст или не является продолжением, то run закончился
            if not self.occupied[next_pos] or not self.continuation[next_pos]:
                break
            pos = next_pos
        return False
