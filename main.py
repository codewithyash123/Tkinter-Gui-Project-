import os
from tkinter import*
from PIL import Image,ImageTk
import cv2 
from tkinter import messagebox as mb
from tkinter import filedialog as fd





    
root=Tk()
root.wm_geometry("1450x700+40+30")
width=1450
height=700
root.minsize(width,height)
root.maxsize(width,height)
root.config(bg="black")
root.title("Welcome to Pycam !")

# root.wm_iconbitmap(r"icon.png")
video=Label(root,bg="green",bd=2)
video.place(x=90,y=100)

save_img=Label(root,bg="black")
save_img.place(x=940,y=100)
 


def succes():
    mb.showinfo("😞 No Preview available !","Please click Photo to see its preview or simply drag and drop any image to see its preview !")
noimg=Button(root,bg="black",fg="white",text="No Preview available !",font=("Arial",30,'bold'),command=succes)
noimg.place(x=950,y=180)

P_img=Button(root,bg="black",fg="lime",text="Camera Preview Started !",font=("Arial",30,'bold'),padx=147)
P_img.place(x=90,y=10)

    
cap=cv2.VideoCapture(0)


def show_video():
    global img,frames, cv2_image

    img_width=800
    img_height=500
    cv2_image=cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img=Image.fromarray(cv2_image)
    img=img.resize((img_width,img_height))
    frames=ImageTk.PhotoImage(image=img)
    video.frames=frames
    video.configure(image=frames)

    video.after(40,show_video)
show_video()


browse_folder=Entry(root,width=80,font=('Arial', 10),textvariable=StringVar)
browse_folder.focus_force()
browse_folder.configure(borderwidth=0,highlightthickness=2,highlightcolor="red",fg="black")
browse_folder.place(x=90,y=628,height=30)

def on_hover_browse_folder(event):
    browse_folder.configure(borderwidth=0,highlightthickness=2,highlightcolor="green",fg="black")
    
def on_leave_browse_folder(event):
    browse_folder.configure(borderwidth=0,highlightthickness=2,highlightcolor="red",fg="black")
browse_folder.bind("<Enter>",on_hover_browse_folder)
browse_folder.bind("<Leave>",on_leave_browse_folder)
def browse():
    browse_folder.delete(0,END)
    image_to_save=fd.askdirectory()
    browse_folder.insert(1,image_to_save)
browse_b=Button(root,text="🔻",command=browse,pady=3,padx=3)
browse_b.place(x=670,y=628)

    
    
def click_photo():
    
    global my_img 
    check_path=os.path.exists(browse_folder.get())
    def check_path_img():
            data=( ("png","*.png") , ("jpg","*.jpg") )
            file=fd.asksaveasfilename(filetypes=data,defaultextension="*.png")
            filename=os.path.abspath(file)
            img_name=os.path.basename(filename)
            browse_folder.delete(0,END)
            browse_folder.insert(0,filename)
            img.save(filename)
            mb.showinfo("Congratulation !",f"{img_name} Succesfully save on {filename}. ")
            noimg.destroy()
            def retake():
                global a
                a=filename
                a=a.replace(f"\{img_name}","")
                os.remove(filename)
                browse_folder.delete(0,END)
                browse_folder.insert(0,a)
                check_path=os.path.exists(browse_folder.get())
                click_photo()
            def skech_converter():
                global filename1
                a=filename
                a=a.replace(f"\{img_name}","")
                with open("path.txt",'w') as f:
                    f.write(a)
                name1=filename
                cv2_im=cv2.imread(name1)
                # convert an image from one color space to another
                grey_img = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2GRAY)
                invert = cv2.bitwise_not(grey_img)  # helps in masking of the image
                # sharp edges in images are smoothed while minimizing too much blurring
                blur = cv2.GaussianBlur(invert, (21, 21), 0)
                invertedblur = cv2.bitwise_not(blur)
                sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
                import random
                ran=random.randint(1,100)
                my_skech_img_name=f"{ran}_sketch.png"
                sketch_img =f"{a}\{my_skech_img_name}"
                cv2.imwrite(sketch_img, sketch)  
                cv2.imshow(f"{my_skech_img_name} -Preview",sketch)
                mb.showinfo("Imaged Saved !",f"Skech Image Save as {sketch_img} !")
                    
                filename1=sketch_img    
                root.update()   
                
                
            filename1=filename
            ab=Image.open(filename1)
            ab=ab.resize((450,250))
            image_save=ImageTk.PhotoImage(ab)
            save_img.image_save=image_save
            save_img.configure(image=image_save,bg="red",bd=2)
            
            def controls():
                
                retake_button=Button(root,font=("Arial",15,'bold') ,text="- Retake Photo -",padx=140,pady=20,command=retake)
                retake_button.place(x=940,y=400)
                convert_skech_button=Button(root,font=("Arial",15,'bold'),text="- Convert to Skech -",padx=124,pady=15,command=skech_converter)
                convert_skech_button.place(x=940,y=500)
            
                
            controls()
            
    if len(browse_folder.get())==0:
        mb.showwarning("Select a Path !","Select a location to save your image .")
        check_path_img()
    
    elif check_path == False:
        mb.showerror("invaild path !","Path not Found !")
        check_path_img()
    elif check_path == True:
        check_path_img()

click_Img=Button(root,text=f"Take Photo",bg="lime",font=("Arial",10,"bold"),pady=10,padx=45,command=click_photo)
click_Img.place(x=720,y=622)
def on_hover_button(event):
    global popup
    popup=Toplevel(root)
    popup.geometry("130x25+680+660")
    popup.overrideredirect(1)
    pop_message=Label(popup,text=" Browse Directory ! ",fg="black",font=("Arial",10,"bold"))
    pop_message.pack()
    
def on_hover_leave(event):
    popup.destroy()
    
def on_hover_take(event):
    global popup1
    popup1=Toplevel(root)
    popup1.geometry("120x25+945+690")
    popup1.overrideredirect(1)
    pop_message=Label(popup1,text=" Take Photo ! ",fg="black",font=("Arial",10,"bold"))
    pop_message.pack()
    
def on_hover_leave_take(event):
    popup1.destroy()
    
click_Img.bind("<Enter>",on_hover_take)
click_Img.bind("<Leave>",on_hover_leave_take)
browse_b.bind("<Enter>",on_hover_button)
browse_b.bind("<Leave>",on_hover_leave)

root.mainloop()

