from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from Encryption import Encryption
from Decryption import Decryption
import math
import os


class Application(Frame):
    def __init__(self, master=None):
        self.file_name = ''
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def open_file(self):
        self.file_name = askopenfilename(filetypes=[('BMP File', '*.bmp')])

        # динамически изменяем текст метки
        self.name_label['text'] = 'Name: ' + self.file_name

        # очистка сообщения в msg_box
        if self.msg_box.get('1.0', END) != '':
            self.msg_box.delete('1.0', END)

        # очистка изображения
        # изображение и фотография должны быть глобальными, иначе изображение не будет отображаться
        global left_img
        left_img = None
        global left_photo
        left_photo = None
        global right_img
        right_img = None
        global right_photo
        right_photo = None

        left_img = Image.open(self.file_name)
        w, h = left_img.size
        self.dimensions_label['text'] = 'Размеры: ' + str(w) + 'x' + str(h)

        self.size_label['text'] = 'Size: ' + str(os.path.getsize(self.file_name)) + 'Bytes'

        # mode https://pillow.readthedocs.io/en/4.1.x/handbook/concepts.html#concept-modes
        if left_img.mode == 'L':
            self.mode_label['text'] = 'Режим: 8-Битные пиксели, Черно-белый'
            self.available = int((w * h) / 8 - 4)
            if self.available <= 0:
                self.available_label['text'] = 'Доступный Размер Для Stega: 0 Байт'
            else:
                self.available_label['text'] = 'Доступный Размер Для Stega:  ' + str(self.available) + 'Байт'
        elif left_img.mode == 'RGB':
            self.mode_label['text'] = 'Режим: 3x8-Битные Пиксели, Истинный Цвет'
            self.available = int((w * h * 3) / 8 - 4)
            if self.available <= 0:
                self.available_label['text'] = 'Доступный Размер Для Stega: 0 Байт'
            else:
                self.available_label['text'] = 'Доступный Размер Для Stega: ' + str(self.available) + 'Байт'
        else:
            self.mode_label['text'] = 'Mode: ' + left_img.mode

        # изменение размера изображения
        scale_w = img_display_width / w
        scale_h = img_display_height / h
        scale = min(scale_w, scale_h)
        new_w = math.ceil(scale * w)
        new_h = math.ceil(scale * h)
        left_img = left_img.resize((new_w, new_h), Image.NEAREST)

        left_photo = ImageTk.PhotoImage(left_img)

        self.left_img_canvas.create_image(img_display_width / 2, img_display_height / 2, anchor=CENTER,
                                          image=left_photo)

    def decry(self):
        if self.file_name == '':
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Пожалуйста, сначала откройте растровый файл.')
            return 0
        elif self.available < 1:
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Это изображение слишком короткое, чтобы скрыть сообщение.')
            return 0
        else:
            decryption = Decryption(self.file_name)
            decry_msg = decryption.run()
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Скрытое сообщение: "' + decry_msg + '".')

    def encry(self):
        hide_msg = self.msg_box.get('1.0', END).replace('\n', '')
        if self.file_name == '':
            if hide_msg == '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Пожалуйста, сначала откройте растровый файл.')
            return 0
        elif hide_msg == '':
            self.msg_box.insert(END, 'Введите скрытое сообщение здесь')
            return 0
        elif len(hide_msg) > self.available:
            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Введёное скрытое сообщение больше чем ' + str(self.available) + ' байт.')
            return 0
        else:
            origin_file_name = self.file_name
            # добавление "скрытый" к имени нового файла изображения
            new_file_name = self.file_name[:-4] + '_hidden' + self.file_name[-4:]
            encryption = Encryption(origin_file_name, new_file_name, hide_msg)
            encryption.run()

            global right_img
            right_img = Image.open(self.file_name)
            w, h = right_img.size
            # изменение размера изображения
            scale_w = img_display_width / w
            scale_h = img_display_height / h
            scale = min(scale_w, scale_h)
            new_w = math.ceil(scale * w)
            new_h = math.ceil(scale * h)
            img = right_img.resize((new_w, new_h), Image.NEAREST)

            global right_photo
            right_photo = ImageTk.PhotoImage(img)
            self.right_img_canvas.create_image(img_display_width / 2, img_display_height / 2, anchor=CENTER,
                                               image=right_photo)

            if self.msg_box.get('1.0', END) != '':
                self.msg_box.delete('1.0', END)
            self.msg_box.insert(END, 'Файл сохранён ' + new_file_name + '.')

    def create_widgets(self):
       
        left_frame = Frame(self)
        left_frame.pack(side=LEFT)

        show_frame = Frame(left_frame)
        show_frame.pack(side=TOP)

        open_frame = Frame(show_frame)
        open_frame.pack(side=TOP)

        open_label = Label(open_frame, text='Открыть BMP файл:')
        open_label.pack(side=LEFT)

        open_button = Button(open_frame, text='Открыть', command=self.open_file)
        open_button.pack(side=LEFT)

        self.name_label = Label(show_frame, text='Название: ')
        self.name_label.pack(side=TOP)

        self.dimensions_label = Label(show_frame, text='Размеры: ')
        self.dimensions_label.pack(side=TOP)

        self.size_label = Label(show_frame, text='Размер: ')
        self.size_label.pack(side=TOP)

        self.mode_label = Label(show_frame, text='Доступный размер для Stega: ')
        self.mode_label.pack(side=TOP)

        self.available_label = Label(show_frame, text='Режим: ')
        self.available_label.pack(side=TOP)

        self.left_img_canvas = Canvas(left_frame, bg='grey', width=img_display_width, height=img_display_height)
        self.left_img_canvas.pack(side=BOTTOM)

        right_frame = Frame(self)
        right_frame.pack(side=RIGHT)

        en_de_cry_frame = Frame(right_frame)
        en_de_cry_frame.pack(side=TOP)

        decry_button = Button(en_de_cry_frame, text='Дешифровать', command=self.decry)
        decry_button.pack(side=LEFT)

        encry_button = Button(en_de_cry_frame, text='Зашифровать', command=self.encry)
        encry_button.pack(side=RIGHT)

        msg_frame = Frame(right_frame)
        msg_frame.pack(side=TOP)

        self.msg_box = Text(msg_frame, width=42, height=7)
        self.msg_box.pack(side=BOTTOM)

        self.right_img_canvas = Canvas(right_frame, bg='grey', width=img_display_width, height=img_display_height)
        self.right_img_canvas.pack(side=BOTTOM)


left_img = None
left_photo = None
right_img = None
right_photo = None
img_display_width = 300
img_display_height = 200
app = Application()
app.master.title('LSB Steganography')
app.mainloop()
