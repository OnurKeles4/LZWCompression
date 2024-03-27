import tkinter.messagebox

from PIL import ImageTk
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from ImageMethods import *
from Project1Final import *
#from Project1Final import Text

class UserInterface(tk.Tk):

    def __init__(self, *args: list, **kwargs: dict) -> None:
        print("UI Started")
        super().__init__(*args, **kwargs)

        self.title("LZW Project")
        self.directory = os.getcwd()
        #self.path = "TOBE.txt"  # base value

        self.path = os.path.join(self.directory, "pixel_art.bmp")                   #a start up file needs to exists for path
        self.second_path = os.path.join(self.directory, "pixel_art_decompress.png")
        #try to add different path for temp image
        try:
            self.org_image = Image.open(self.path)
        except:
            self.org_image = Image.new("RGB", (50, 50), (0, 0, 0))

        try:
            self.second_image = Image.open(self.second_path)
        except:
            self.second_path = self.path  # No file in the located dictionary
            self.second_image = self.org_image

        self.reference = ImageTk.PhotoImage(self.org_image)
        self.second_reference = ImageTk.PhotoImage(self.second_image)

        self.imageSize = 0.0
        self.second_imageSize = 1.0

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container = ttk.Frame(self, padding=30)

        self.container.grid(row=0, column=0)
        self.container.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.container.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)


        """self.agreement = tk.StringVar(self.container, "color")
        self.check_box = ttk.Checkbutton(self.container, text="Gray Image", variable=self.agreement, onvalue="gray", offvalue="color")
        print(self.agreement)
        self.check_box.grid(row=5,column=4,columnspan=2)"""

        self.org_title_lbl = ttk.Label(self.container, text="Image", anchor="center")
        self.org_title_lbl.grid(row=0, column=0, columnspan=2)

        self.second_title_lbl = ttk.Label(self.container, text="Second Image", anchor="center")
        self.second_title_lbl.grid(row=0, column=2, columnspan=2)

        self.org_image_lbl = ttk.Label(self.container, image=self.reference, anchor="center")
        self.org_image_lbl.grid(row=1, column=0, columnspan=2)

        self.second_image_lbl = ttk.Label(self.container, image=self.second_reference, anchor="center")
        self.second_image_lbl.grid(row=1, column=2, columnspan=2)

        self.org_info_lbl = ttk.Label(self.container)
        self.org_info_lbl.grid(row=2, column=0, columnspan=2)

        self.comparison_lbl = ttk.Label(self.container, text=f"{(self.imageSize / self.second_imageSize).__round__(2)}",
                                        anchor="center")
        self.comparison_lbl.grid(row=5, column=3, columnspan=2)

        self.updateImageInfo("org")

        self.second_info_lbl = ttk.Label(self.container)
        self.second_info_lbl.grid(row=2, column=2, columnspan=2)

        self.updateImageInfo("second")


        self.ask_file_button = ttk.Button(self.container, text="Open File",
                                          command=self.loadFile)
        self.ask_file_button.grid(row=3, column=0, columnspan=1)

        self.comp_image_button = ttk.Button(self.container, text="Compress Image",
                                                       command=self.compImageButton)
        self.comp_image_button.grid(row=3, column=1, columnspan=2)

        self.decomp_image_button = ttk.Button(self.container, text="Decompress Image",
                                            command=self.decompImageButton)
        self.decomp_image_button.grid(row=4, column=1, columnspan=2)

        self.comp_text_button = ttk.Button(self.container, text="Compress Text",
                                                      command=self.compTextButton)
        self.comp_text_button.grid(row=3, column=4)

        self.decomp_text_button = ttk.Button(self.container, text="Decompress Text",
                                                      command=self.decompTextButton)
        self.decomp_text_button.grid(row=4, column=4)

    def isGray(self):
        if(self.agreement):
            print("It is gray")
        else:
            print("Its is colored")

    def getImageInfo(self, image, path, text):

        img_array = np.array(image)

        width = img_array.shape[1]
        height = img_array.shape[0]
        str = ""

        if text == "org":
            self.imageSize = (os.stat(path).st_size/1024).__round__(2)
            str = f"Width: {width}, Height: {height} \n Size {self.imageSize} kb"
        elif text == "second":
            self.second_imageSize = (os.stat(path).st_size/1024).__round__(2)
            str = f"Width: {width}, Height: {height} \n Size {self.second_imageSize} kb"

        return str

    def getTextInfo(self):

        return ""

    def updateImageInfo(self, lbl):

        if lbl == "org":
            #print("org")
            self.org_title_lbl.config(text="Image")
            self.org_title_lbl.grid(row=0, column=0, columnspan=2)

            info = self.getImageInfo(self.org_image, self.path, lbl)
            self.org_info_lbl.configure(text=info, anchor="center")
        elif lbl == "second":
            #print("second")
            self.second_title_lbl.config(text="Second Image")
            self.second_title_lbl.grid(row=0, column=2, columnspan=2)

            info = self.getImageInfo(self.second_image, self.second_path, lbl)
            self.second_info_lbl.configure(text=info, anchor="center")
        else:
            print("Wrong information")

        if self.imageSize != 0 and self.second_imageSize != 0:
            self.comparison_lbl.config(text=f"Comparison of files: {(self.imageSize / self.second_imageSize).__round__(2)}")

    def updateTextInfo(self):
        info = self.getTextInfo()
        self.org_title_lbl.config(text="Text")
        self.org_title_lbl.grid(row=0, column=0, columnspan=2)

        self.second_title_lbl.config(text="Text")
        self.second_title_lbl.grid(row=0, column=2, columnspan=2)

        self.org_info_lbl.configure(text=info, anchor="center")
        self.second_info_lbl.configure(text=info, anchor="center")

    def updateBinInfo(self):
        info = self.getTextInfo()
        self.org_title_lbl.config(text="Bin")
        self.org_title_lbl.grid(row=0, column=0, columnspan=2)

        self.second_title_lbl.config(text="Bin")
        self.second_title_lbl.grid(row=0, column=2, columnspan=2)

        self.org_info_lbl.configure(text=info, anchor="center")
        self.second_info_lbl.configure(text=info, anchor="center")

    def loadFile(self):
        self.ask_file_button.configure(state="disabled", text="File loading")
        path = filedialog.askopenfile(initialdir=self.directory, title="Select an File",
                                      filetypes=[
                                          ('png files', '*.png'), ('txt files', '*.txt'), ('bmp files', '*.bmp'), ('bin files','*.bin')])
        if path:
            self.path = path.name
            if self.isImageExtension():
                self.path = path.name
                self.org_image = Image.open(self.path)
                self.reference = ImageTk.PhotoImage(self.org_image)
                self.org_image_lbl.configure(image = self.reference)
                self.updateImageInfo("org")

                #print("file exists?", os.path.isfile(path.name + "_decompress.png"))
                if path.name.find("_decompress") != -1:
                    print("This image is already decompressed")
                    self.second_path = path.name
                if os.path.isfile(path.name.split('.')[0] + "_decompress.png"):
                    self.second_path = path.name.split('.')[0] + "_decompress.png"
                else:
                    self.second_path = path.name
                self.second_image = Image.open(self.second_path)
                self.second_reference = ImageTk.PhotoImage(self.second_image)
                self.second_image_lbl.configure(image=self.second_reference)
                self.updateImageInfo("second")
            elif self.isBinExtension() or self.isTextExtension():           # Try to create a text widget later.
                self.path = path.name
                if self.isTextExtension():
                    self.updateTextInfo()
                else:
                    self.updateBinInfo()
                self.comparison_lbl.config(
                    text="incomparable file")
                self.org_image = Image.open("small-file-icon-21.jpg")
                self.reference = ImageTk.PhotoImage(self.org_image)
                self.org_image_lbl.configure(image=self.reference)

                self.second_image = Image.open("small-file-icon-21.jpg")
                self.second_reference = ImageTk.PhotoImage(self.second_image)
                self.second_image_lbl.configure(image=self.second_reference)



        self.ask_file_button.configure(state="normal", text="Open File")

    def compImageButton(self):
        if self.isImageExtension():
            #self.decomp_image_button.configure(state="disabled", text="File Compressing")
            CompressImage(self.path)
            #self.decomp_image_button.configure(state="normal", text="Decompress Image")
            tkinter.messagebox.showinfo(title="Completed", message="Successfully Compressed!")
        else:
            self.Warning()

    def updateDecompedImage(self):
        self.second_path = self.path.split('.')[0] + "_decompress.png"
        self.second_image = Image.open(self.second_path)
        self.second_reference = ImageTk.PhotoImage(self.second_image)
        self.second_image_lbl.configure(image=self.second_reference)
        self.updateImageInfo("second")

    def decompImageButton(self):
        if self.isImageExtension():
            #print("decomp button  ",self.path.split('.')[0] + ".bin")
            #self.comp_image_button.configure(state="disabled", text="File Decompressing")
            DecompressImage(self.path.split('.')[0] + ".bin")
            #self.comp_image_button.configure(state="normal", text="Compress Image")
            tkinter.messagebox.showinfo(title="Completed", message="Successfully Decompressed!")
            self.updateDecompedImage()
        else:
            self.Warning()

    def Warning(self):
        tkinter.messagebox.showwarning(title="Path Error", message= "Wrong Path extension\n"
                                                                    f"{self.path.split('.')[1]}")
        print("wrong path:", self.path.split('.')[1])

    def compTextButton(self):
        if self.isTextExtension():
            CompressText(self.path)
            tkinter.messagebox.showinfo(title="Completed", message="Successfully Compressed!")
        else:
            self.Warning()

    def decompTextButton(self):
        if self.isTextExtension():
            DecompressText(self.path.split('.')[0] + ".bin")
            tkinter.messagebox.showinfo(title="Completed", message="Successfully Decompressed!")
        else:
            self.Warning()

    def isImageExtension(self):
        #print("fff", str(self.path).split('.')[1])
        return str(self.path).split('.')[1] == "bmp" or str(self.path).split('.')[1] == "png"

    def isBinExtension(self):
        #print("ggg", str(self.path).split('.')[1])
        return self.path.split('.')[1] == "bin"

    def isTextExtension(self):
        #print("hh", str(self.path).split('.')[1])
        return self.path.split('.')[1] == "txt"

if __name__ == '__main__':
    UserInterface().mainloop()
