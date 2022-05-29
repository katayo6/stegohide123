
HEADER_SIZE = 1078  # Размер заголовка файла bmp : 14 + 40 + 1024 bytes


class Encryption:
    def open_file(self):
        with open(self.origin_file_name, 'rb') as f:
            # Считывание файла изображения в байты
            self.origin_image_data = f.read()

    def copy_header(self):
        # Считывание заголовка файла bmp (14) и заголовка информации о растровом изображении (40) и палитры (1024)
        # Скопируем их в новое изображение
        for i in range(0, HEADER_SIZE):
            self.new_image_data.append(self.origin_image_data[i])
            self.bytes_counter += 1

    def hide_int(self, curr_hide_int):
        curr_hide_binary = '{:032b}'.format(curr_hide_int)
        for i in range(0, 32):
            curr_image_binary = '{0:08b}'.format(self.origin_image_data[self.bytes_counter])
            # В режиме порядка байтов наименьший значащий бит является первым битом
            new_image_binary = curr_hide_binary[i] + curr_image_binary[1:]
            new_image_int = int(new_image_binary, 2)
            self.new_image_data.append(new_image_int)
            self.bytes_counter += 1

    def hide_char(self, curr_hide_byte):
        # ord(): преобразует char в int
        # Затем получаем двоичное значение в один байт
        # a = '{0:08b}'.format(255)
        # print(a) # '1111111'
        curr_hide_binary = '{0:08b}'.format(ord(curr_hide_byte))

        # Скроем один байт в восьми байтах
        for i in range(0, len(curr_hide_binary)):
            curr_image_binary = '{0:08b}'.format(self.origin_image_data[self.bytes_counter])
            # В режиме порядка байтов наименьший значащий бит является первым битом
            new_image_binary = curr_hide_binary[i] + curr_image_binary[1:]
            new_image_int = int(new_image_binary, 2)
            self.new_image_data.append(new_image_int)
            self.bytes_counter += 1

    def do_hide(self):
        # Спрячем длину сообщения
        self.hide_int(len(self.hide_msg))
        # Спрячем сообщение байт за байтом
        for i in range(0, len(self.hide_msg)):
            self.hide_char(self.hide_msg[i])

    def copy_rest(self):
        # Скопируем остальные данные в новое изображение
        left_data = self.origin_image_data[self.bytes_counter:]
        for left_byte in left_data:
            self.new_image_data.append(left_byte)

    def write_file(self):
        with open(self.new_file_name, 'wb') as out:
            new_image_bytes = bytearray(self.new_image_data)
            out.write(new_image_bytes)

    def run(self):
        self.open_file()
        self.copy_header()
        self.do_hide()
        self.copy_rest()
        self.write_file()

    def __init__(self, origin_file_name, new_file_name, hide_msg):
        self.origin_file_name = origin_file_name
        self.new_file_name = new_file_name
        self.hide_msg = hide_msg
        self.bytes_counter = 0  # Функция в качестве указателя
        self.origin_image_data = ''  # Тип: биты
        self.new_image_data = []  # Тип: массив int
