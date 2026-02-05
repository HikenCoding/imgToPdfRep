import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import os


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar();
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        

        self.initialize_ui()
        
    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        select_images_button = tk.Button(self.root, text="Select Images", command=self.
                                         select_images)
        select_images_button.pack(pady=(0,10))
        
        self.selected_images_listbox.pack(pady=(0,10), fill=tk.BOTH, expand=True)
        
        label = tk.Label(self.root, text="Enter output PDF name:")
        label.pack()
        
        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40,
                                  justify='center')
        pdf_name_entry.pack()
        
        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.
                                         convert_images_to_pdf)
        convert_button.pack(pady=(20,40))
        
        savePdfInFolder = tk.Button(
            self.root, 
            text="Save Images in Desktop", 
            command=self.save_pdf_in_folder)
        savePdfInFolder.pack(pady=(30,50))
        
        clear_images_button = tk.Button(
            self.root, 
            text="Select Images",
            command=self.clear_images)
        clear_images_button.pack(pady=(0,10))
        

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", 
                                                       filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        self.update_selected_images_listbox()
        
    def clear_images(self):
        self.selected_images_listbox.delete(0, tk.END)
        
    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        
        for image_path in self.image_paths:
            _, image_path = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_path)
            
    def convert_images_to_pdf(self):
        if not self.image_paths:
            return 
        
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612,792))
        
        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2
            
            pdf.setFillColor(colors.white)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()
        
        pdf.save()
    
    def choose_save_path(self, default_name="converted.pdf"):
        return filedialog.asksaveasfilename(
            title="PDF speichern unter ...",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF-Datei", "*.pdf")]
        )
        
    def save_pdf_in_folder(self):
        if not self.image_paths:
            return
        
        save_path = self.choose_save_path("converted.pdf")
        if not save_path:
            return
        
        page_w, page_h = A4
        c = canvas.Canvas(save_path, pagesize=A4)
        
        for img_path in self.image_paths:
            img = Image.open(img_path)
            img_w, img_h = img.size
            
            scale = min(page_w / img_w, page_h / img_h)
            new_w = img_w * scale
            new_h = img_h * scale
            
            x =(page_w -new_w) / 2
            y =(page_h - new_h) /2
            
            c.drawImage(ImageReader(img), x, y, width=new_w, height=new_h)
            c.showPage()
            
        c.save()
        
 
        
        
def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()
    
    
if __name__ == "__main__":
    main()        