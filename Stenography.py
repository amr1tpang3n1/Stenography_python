from tkinter import *
from PIL import Image
import Custom_Encryption
from tkinter import messagebox

class ImgStenography:
    def __init__(self):
         self.root = Tk()
         self.root.iconbitmap("icon.ico")
         self.root.title("Image Stenography Tool")
         self.root.geometry("600x500")
         self.root.resizable(0,0)
         self.root.config(bg= "#70adda")

         self.label = Label(text = "Enter Filepath for Injecting/Decoding Data: ", font = ("times",16), bg = "#70adda")
         self.label.place(x = 10, y = 20)
         self.entry = Entry(self.root, font = ("times" , 16), width = 50)
         self.entry.place(x = 20, y = 70)

         self.label2 = Label(text = "Enter Data to Inject inside the file: [Blank for Decoding]", font = ("times",16), bg = "#70adda")
         self.label2.place(x = 10, y = 120)
         self.entry2 = Entry(self.root, font = ("times" , 16), width = 50)
         self.entry2.place(x = 20, y = 170)

         self.label3 = Label(text = "Enter Encryption/ Decryption Key:", font = ("times",16), bg = "#70adda")
         self.label3.place(x = 10, y = 220)
         self.entry3 = Entry(self.root, font = ("times" , 16), width = 50)
         self.entry3.place(x = 20, y = 270)

         self.label4 = Label(text = "New File Name for Encrypted File [Blank for Decoding]:", font = ("times",16), bg = "#70adda")
         self.label4.place(x = 10, y = 320)
         self.entry4 = Entry(self.root, font = ("times" , 16), width = 50)
         self.entry4.place(x = 20, y = 370)

         self.btn1 = Button(self.root, font=("times",16), command = self.encode, text = "Encode")
         self.btn1.place(x = 200, y = 450)
         self.btn2 = Button(self.root,font = ("times",16), command = self.decode, text = "Decode")
         self.btn2.place(x = 300, y = 450)
         self.entry.focus()
         self.root.mainloop()

    def ExtractImageData(self,data):
         new_data = []
         for i in data:
              new_data.append(format(ord(i), '08b'))
         return new_data

    def PixExtraction(self,pix, data):
         datalist = self.ExtractImageData(data)
         lendata = len(datalist)
         imdata = iter(pix)

         for i in range(lendata):
              # List comprehension
              pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]

              for j in range(0, 8):
                   if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                        pix[j] -= 1

                   elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                        if (pix[j] != 0):
                             pix[j] -= 1
                        else:
                             pix[j] += 1

              if (i == lendata - 1):
                   if (pix[-1] % 2 == 0):
                        if (pix[-1] != 0):
                             pix[-1] -= 1
                        else:
                             pix[-1] += 1

              else:
                   if (pix[-1] % 2 != 0):
                        pix[-1] -= 1

              pix = tuple(pix)
              yield pix[0:3]
              yield pix[3:6]
              yield pix[6:9]

    def encode_in_new_img(self,new_img,data):
        w = new_img.size[0]
        (x, y) = (0, 0)

        for pixel in self.PixExtraction(new_img.getdata(), data):
          # Putting modified pixels in the new image
          new_img.putpixel((x, y), pixel)
          if (x == w - 1):
                   x = 0
                   y += 1
          else:
                   x += 1

    def encode(self):
        img = self.entry.get()
        image = Image.open(img, 'r')
        initial = self.entry2.get()
        key = int(self.entry3.get())
        data = Custom_Encryption.Encrypt_Ceaser_cipher(initial, key)
        if (len(data) == 0):
            raise ValueError('Data is empty')
        newimg = image.copy()
        self.encode_in_new_img(newimg, data)

        new_img_name = self.entry4.get()
        newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        messagebox.showinfo("Success !", "Encryption and Encoding of Data in File Successful !" )
        print("Encoded !")

    def decode(self):
        img = self.entry.get()
        key = int(self.entry3.get())
        image = Image.open(img, 'r')

        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]

            # string of binary data
            binstr = ''
            for i in pixels[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if (pixels[-1] % 2 != 0):
                data = Custom_Encryption.Decrypt_rot_13(data, key)
                print(f"Decoded text : {data}")
                messagebox.showinfo("Decryption Success !", f"Decoded Message : {data}")
                return data

ImgStenography()