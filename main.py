from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from pathlib import Path

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

def retrieve_input():
    genes=textBox.get("1.0","end-1c")
    genes = [gene.strip() for gene in genes.split('\n')]
    vcf_folder = folder_path.get()
    if vcf_folder:
        vcf_path = Path(vcf_folder)
    else:
        messagebox.showerror("Error!", "Enter VCF folder.")
    if not genes:
        messagebox.showerror("Error!", "Enter genes.")

    vcfs = [vcf for vcf in vcf_path.glob('*.vcf')]
    if not vcfs:
        messagebox.showerror("Error!", "Can't find vcf files in given path. Make sure they're not gzipped. I don't have time to add gzip support.")

    filtered_path = vcf_path.joinpath('filtered')
    filtered_path.mkdir(exist_ok=True, parents=True)
    for vcf in vcfs:
        filtered_vcf = filtered_path.joinpath(vcf.name)
        with open(filtered_vcf.as_posix(), 'w') as g:
            with open(vcf.as_posix()) as f:
                lines = f.read().splitlines()

            for line in lines:
                if line.startswith('#'):
                    g.write(f'{line}\n')
                else:
                    for gene in genes:
                        if gene in line:
                            g.write(f'{line}\n')

root = Tk()
folder_path = StringVar()
lbl1 = Label(master=root,textvariable=folder_path)
button2 = Button(text="Browse VCF folder", command=browse_button)

lbl2 = Label(root, text = "Genes")
textBox=Text(root, height=20, width=20)
buttonCommit=Button(root, height=1, width=100, text="Filter by gene names!",
                    command=lambda: retrieve_input())
#command=lambda: retrieve_input() >>> just means do this when i press the button
lbl1.pack()
lbl2.pack()
textBox.pack()
button2.pack()
buttonCommit.pack()

mainloop()
