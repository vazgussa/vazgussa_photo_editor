from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PIL import ImageTk, Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import webbrowser


class PhotoEditor:
    def __init__(self, master):
        # Создание окна программы
        self.master = master
        self.master.title("Редактор фотографий")
        self.master.state('zoomed')
        self.image = None
        self.filtered_image = None
        self.rotate_left_image = PhotoImage(file='Assets/rotateleft.png')
        self.rotate_right_image = PhotoImage(file='Assets/rotateright.png')
        self.mirror_image = PhotoImage(file='Assets/mirror.png')
        self.uptodown_image = PhotoImage(file='Assets/up-and-down.png')
        self.cropp_image = PhotoImage(file='Assets/crop.png')
        self.text_image = PhotoImage(file='Assets/text.png')
        self.autocontrast_image = PhotoImage(file='Assets/autocontrast.png')
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_image)
        file_menu.add_command(label="Сохранить", command=self.save_image)
        file_menu.add_command(label="Сбросить изменения", command=self.reset_image)
        file_menu.add_separator()
        file_menu.add_command(label="View GitHub", command=self.github)
        file_menu.add_command(label="Выйти", command=self.master.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        # Меню с фильтрами
        filters_menu = Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Ч/б", command=self.grayscale_image)
        filters_menu.add_command(label="Размытие по гауссу", command=self.blur_image)
        filters_menu.add_command(label="Резкость", command=self.edge_enhance_image)
        filters_menu.add_command(label="Emboss", command=self.emboss_image)
        filters_menu.add_command(label="Негатив", command=self.negative_image)
        filters_menu.add_command(label="Мозаика", command=self.mosaic_filter)
        filters_menu.add_command(label="Ludwig", command=self.ludwig_filter)
        filters_menu.add_command(label="Clarendon", command=self.clarendon_filter)
        filters_menu.add_command(label="Gingham", command=self.gingham_filter)
        filters_menu.add_command(label="Lark", command=self.lark_filter)
        filters_menu.add_command(label="Juno", command=self.juno_filter)
        filters_menu.add_command(label="Rise", command=self.rise_filter)
        filters_menu.add_command(label="Valencia", command=self.valencia_filter)
        filters_menu.add_command(label="1977", command=self.nineteen_seventy_seven_filter)
        filters_menu.add_command(label="Nashville", command=self.nashville_filter)
        filters_menu.add_command(label="X-Pro II", command=self.x_pro_ii_filter)
        filters_menu.add_command(label="Hudson", command=self.hudson_filter)
        filters_menu.add_command(label='Hefe', command=self.hefe_filter)
        filters_menu.add_separator()
        filters_menu.add_command(label='Сбросить', command=self.reset_image)
        menubar.add_cascade(label="Фильтры", menu=filters_menu)

        # Канвас на который выводятся изображения
        self.canvas = Canvas(self.master, width=1, height=1)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES, anchor=N)
        # Кнопки
        button_frame = Frame(self.master)
        button_frame.pack(side=TOP)
        crop_button = Button(button_frame, image=self.cropp_image, command=self.crop_image)
        crop_button.pack(side=LEFT)
        rotate_left_button = Button(button_frame, image=self.rotate_left_image, command=self.rotate_left)
        rotate_left_button.pack(side=LEFT)
        rotate_right_button = Button(button_frame, image=self.rotate_right_image, command=self.rotate_right)
        rotate_right_button.pack(side=LEFT)
        flip_horizontal_button = Button(button_frame, image=self.mirror_image, command=self.flip_horizontal)
        flip_horizontal_button.pack(side=LEFT)
        flip_vertical_button = Button(button_frame, image=self.uptodown_image, command=self.flip_vertical)
        flip_vertical_button.pack(side=LEFT)
        text_button = Button(button_frame, image=self.text_image, command=self.add_text)
        text_button.pack(side=LEFT)
        autocontrast_button = Button(button_frame, image=self.autocontrast_image, command=self.automatic_contrast)
        autocontrast_button.pack(side=LEFT)

    def github(self):
        webbrowser.open_new_tab('https://github.com/vazgussa/vazgussa_photo_editor/')

    # Файлдиалог для открытия изображений
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.filtered_image = self.image.copy()
            self.display_image()

    # Файлдиалог для сохранения изображений
    def save_image(self):
        if self.filtered_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.filtered_image.save(file_path)

    # Вывод картинки в канвас
    def display_image(self):
        if self.image:
            self.canvas.delete(ALL)
            while self.filtered_image.size[0] > 1920 or self.filtered_image.size[1] > 1080:
                new_width = self.filtered_image.size[0] // 2
                new_height = self.filtered_image.size[1] // 2
                self.filtered_image = self.filtered_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.photo_image = ImageTk.PhotoImage(self.filtered_image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)

    # Обрезка изображений по указанным x0, y0, x, y
    def crop_image(self):
        if self.image:
            crop_window = Toplevel()
            crop_window.title("Обрезка изображения")
            Label(crop_window, text="Введите параметры обрезки:").grid(row=0, column=0, columnspan=2)
            Label(crop_window, text="Лево:").grid(row=1, column=0)
            left_entry = Entry(crop_window)
            left_entry.grid(row=1, column=1)
            Label(crop_window, text="Верх:").grid(row=2, column=0)
            upper_entry = Entry(crop_window)
            upper_entry.grid(row=2, column=1)
            Label(crop_window, text="Право:").grid(row=3, column=0)
            right_entry = Entry(crop_window)
            right_entry.grid(row=3, column=1)
            Label(crop_window, text="Низ:").grid(row=4, column=0)
            lower_entry = Entry(crop_window)
            lower_entry.grid(row=4, column=1)

            # callback
            def crop_image_callback():
                try:
                    left = int(left_entry.get())
                    upper = int(upper_entry.get())
                    right = int(right_entry.get())
                    lower = int(lower_entry.get())

                    self.filtered_image = self.image.crop((left, upper, right, lower))
                    self.display_image()
                    crop_window.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите числовые значения и повторите попытку.")

            Button(crop_window, text="Обрезать", command=crop_image_callback).grid(row=5, column=0, columnspan=2)

    # Различные классические фильтры
    def grayscale_image(self):
        if self.image:
            self.filtered_image = self.image.convert("L")
            self.display_image()

    def blur_image(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.BLUR)
            self.display_image()

    def negative_image(self):
        if self.image:
            self.filtered_image = ImageOps.invert(self.image.convert('RGB')).convert('RGBA')
            self.display_image()

    def edge_enhance_image(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.display_image()

    def emboss_image(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.EMBOSS)
            self.display_image()

    def mosaic_filter(self):
        if self.image:
            width, height = self.filtered_image.size
            width = (width // 10) * 10
            height = (height // 10) * 10
            self.filtered_image = self.filtered_image.crop((0, 0, width, height))
            self.filtered_image = self.filtered_image.resize((width // 10, height // 10), resample=Image.BILINEAR)
            self.filtered_image = self.filtered_image.resize((width, height), resample=Image.NEAREST)
            self.display_image()

    # Фильтры из Instagram
    def ludwig_filter(self):
        if self.image:
            contrast = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = contrast.enhance(1.2)
            saturation = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = saturation.enhance(1.2)
            color = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = color.enhance(1.1)
            self.display_image()

    def clarendon_filter(self):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def gingham_filter(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def lark_filter(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.filtered_image = self.filtered_image.filter(ImageFilter.GaussianBlur(radius=1))
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def juno_filter(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            self.display_image()

    def rise_filter(self):
        if self.image:
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.8)
            self.display_image()

    def valencia_filter(self):
        if self.image:
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            self.display_image()

    def nineteen_seventy_seven_filter(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def nashville_filter(self):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Sharpness(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def x_pro_ii_filter(self):
        if self.image:
            self.filtered_image = ImageOps.colorize(self.filtered_image.convert('L'), "#ffcc00", "#333333")
            self.filtered_image = self.filtered_image.filter(ImageFilter.SMOOTH)
            self.filtered_image = Image.blend(self.filtered_image, self.filtered_image.convert('RGB'), 0.5)

    def hudson_filter(self):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def hefe_filter(self):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.5)
            self.display_image()

    def reset_image(self):
        if self.image:
            self.filtered_image = self.image.copy()
            self.display_image()

    def rotate_left(self):
        if self.image:
            self.filtered_image = self.filtered_image.rotate(90, expand=True)
            self.display_image()

    def rotate_right(self):
        if self.image:
            self.filtered_image = self.filtered_image.rotate(-90, expand=True)
            self.display_image()

    def flip_horizontal(self):
        if self.image:
            self.filtered_image = self.filtered_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image()

    def flip_vertical(self):
        if self.image:
            self.filtered_image = self.filtered_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.display_image()

    def add_text(self):
        if self.image:
            text_image = Image.new('RGBA', self.filtered_image.size, (255, 255, 255, 0))
            text = simpledialog.askstring("Добавление текста", "Введите текст:")
            font_size = simpledialog.askinteger("Добавление текста", "Введите размер шрифта:")
            color = simpledialog.askstring('Добавление текста', 'Введите цвет в формате R G B:').split()
            color = [int(elem) for elem in color]
            draw = ImageDraw.Draw(text_image)
            font = ImageFont.truetype('arial.ttf', font_size)
            draw.text((10, self.filtered_image.size[1] - font_size), text, font=font, fill=(color[0], color[1], color[2], 255))
            self.filtered_image = Image.alpha_composite(self.filtered_image.convert('RGBA'), text_image)
            self.display_image()

    def automatic_contrast(self):
        if self.image:
            self.filtered_image = self.filtered_image.convert('RGB')
            self.filtered_image = ImageOps.autocontrast(self.filtered_image, cutoff=0)
            self.display_image()


root = Tk()
editor = PhotoEditor(root)
root.mainloop()
