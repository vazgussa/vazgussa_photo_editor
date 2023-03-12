from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageFilter, ImageEnhance, ImageOps

class PhotoEditor:
    def __init__(self, master):
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
        # Create menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # Create file menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_image)
        file_menu.add_command(label="Сохранить", command=self.save_image)
        file_menu.add_command(label="Сбросить изменения", command=self.reset_image)
        file_menu.add_separator()
        file_menu.add_command(label="Выйти", command=self.master.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Create filters menu
        filters_menu = Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Ч/б", command=self.grayscale_image)
        filters_menu.add_command(label="Размытие по гауссу", command=self.blur_image)
        filters_menu.add_command(label="Резкость", command=self.edge_enhance_image)
        filters_menu.add_command(label="Emboss", command=self.emboss_image)
        filters_menu.add_command(label="Негатив", command=self.negative_image)
        filters_menu.add_command(label="Ludwig", command=self.ludwig_filter)
        filters_menu.add_command(label="Clarendon", command=self.clarendon_filter)
        filters_menu.add_command(label="Gingham", command=self.gingham_filter)
        filters_menu.add_command(label="Lark", command=self.lark_filter)
        filters_menu.add_separator()
        filters_menu.add_command(label='Сбросить фильтры', command=self.reset_image)
        menubar.add_cascade(label="Фильтры", menu=filters_menu)

        # Create canvas for displaying image
        self.canvas = Canvas(self.master, width=1920, height=800)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES, anchor=N)

        # Create frame for buttons
        button_frame = Frame(self.master)
        button_frame.pack(side=TOP)

        # Create reset button
        crop_button = Button(button_frame, image=self.cropp_image, command=self.crop_image)
        crop_button.pack(side=LEFT)

        # Create rotate buttons
        rotate_left_button = Button(button_frame, image=self.rotate_left_image, command=self.rotate_left)
        rotate_left_button.pack(side=LEFT)
        rotate_right_button = Button(button_frame, image=self.rotate_right_image, command=self.rotate_right)
        rotate_right_button.pack(side=LEFT)

        # Create flip buttons
        flip_horizontal_button = Button(button_frame, image=self.mirror_image, command=self.flip_horizontal)
        flip_horizontal_button.pack(side=LEFT)
        flip_vertical_button = Button(button_frame, image=self.uptodown_image, command=self.flip_vertical)
        flip_vertical_button.pack(side=LEFT)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.filtered_image = self.image.copy()
            self.display_image()

    def save_image(self):
        if self.filtered_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.filtered_image.save(file_path)

    def display_image(self):
        if self.image:
            self.canvas.delete(ALL)
            # check if image needs to be resized
            while self.filtered_image.size[0] > 1920 or self.filtered_image.size[1] > 1080:
                new_width = self.filtered_image.size[0] // 2
                new_height = self.filtered_image.size[1] // 2
                self.filtered_image = self.filtered_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.photo_image = ImageTk.PhotoImage(self.filtered_image)
            self.canvas.create_image(0, 0, anchor=NW, image=self.photo_image)

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
            self.filtered_image = ImageOps.invert(self.image)
            self.display_image()

    def ludwig_filter(self):
        if self.image:
            self.filtered_image = self.image
            contrast = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = contrast.enhance(1.2)
            saturation = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = saturation.enhance(1.2)
            color = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = color.enhance(1.1)
            self.display_image()

    def clarendon_filter(self):
        if self.image:
            self.filtered_image = self.image
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def gingham_filter(self):
        if self.image:
            self.filtered_image = self.image
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def lark_filter(self):
        if self.image:
            self.filtered_image = self.image
            enhancer = ImageEnhance.Brightness(self.filtered_image)
            self.filtered_image = enhancer.enhance(0.9)
            enhancer = ImageEnhance.Contrast(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.filtered_image = self.filtered_image.filter(ImageFilter.GaussianBlur(radius=1))
            enhancer = ImageEnhance.Color(self.filtered_image)
            self.filtered_image = enhancer.enhance(1.1)
            self.display_image()

    def edge_enhance_image(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.display_image()

    def emboss_image(self):
        if self.image:
            self.filtered_image = self.image.filter(ImageFilter.EMBOSS)
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


if __name__ == '__main__':
    root = Tk()
    editor = PhotoEditor(root)
    root.mainloop()
