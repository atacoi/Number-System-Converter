import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import messagebox

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    WIDTH  = 550
    HEIGHT = 200
    MIN_WIDTH  = 550
    MIN_HEIGHT = 200

    def __init__(self):
        super().__init__()
        self.title("Number System Converter")

        self.columnconfigure(0, weight=1)

        container = tk.Frame(self)
        container.place(anchor="c", relx=.5, rely=.5)

        frame1 = Format(container, "From:", 0)
        frame1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        frame2 = Format(container, "To:", 1)
        frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        writer = Write(container, frame1, frame2)
        writer.grid(row=2, column=0, columnspan=2, sticky="we")

        screen_width  = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
    
        x = (screen_width - Application.WIDTH) // 2
        y = (screen_height - Application.HEIGHT) // 2

        self.geometry(f"{Application.WIDTH}x{Application.HEIGHT}+{x}+{y}")
        self.minsize(Application.MIN_WIDTH, Application.MIN_HEIGHT)

        made_by_lbl = ttk.Label(container, text="Created by https://github.com/atacoi")
        made_by_lbl.grid(row=3, column=1, sticky="se", pady=5)

class Format(tk.Frame):
    OPTIONS = ["Decimal", "Binary", "Octal", "Hexadecimal"]

    def __init__(self, parent, lbl_text, starting_index):
        super().__init__(parent)
        self.lbl = ttk.Label(self, text=lbl_text)
        self.lbl.grid(row=0, column=0)

        self.clicked = StringVar()
        self.clicked.set(Format.OPTIONS[starting_index]) 
        print(f"Options: {Format.OPTIONS}")
        self.combo_box = ttk.Combobox(self, textvariable=self.clicked, values=Format.OPTIONS, state="readonly")
        self.combo_box.grid(row=0, column=1)

class Write(tk.Frame):

    def __init__(self, parent, input_frame, output_frame):
        super().__init__(parent)

        self.columnconfigure(1, weight=1)

        self.input_lbl = ttk.Label(self, text="Input:")
        self.input_lbl.grid(row=0, column=0, sticky="w")

        self.input_clicked  = input_frame.clicked
        self.output_clicked = output_frame.clicked
        
        self.input = ttk.Entry(self)
        self.input.grid(row=0, column=1, sticky="ew")

        self.input.bind("<Return>", self.process_input)

        self.output_lbl = ttk.Label(self, text="Output:")
        self.output_lbl.grid(row=1, column=0, sticky="w")

        self.output_text = StringVar()
        self.output = ttk.Entry(self, textvariable=self.output_text, state="readonly")
        self.output.grid(row=1, column=1, sticky="ew")

        self.btn = ttk.Button(self, text="Convert", command=self.process_input)
        self.btn.grid(row=2, column=0, columnspan=2)

    # Returns one of the codes listed below:
    # 0 - Valid input
    # 1 - Empty input
    # 2 - Input numerical system not found
    # 3 - Invalid syntax for input string
    # 4 - Converting to same numerical system
    def is_valid(self, input, input_clicked, output_clicked):
        if(not input):
            return 1
        
        alpha = []
        if(input_clicked == "Decimal"):
            alpha = [str(i) for i in range(10)]

        if(input_clicked == "Binary"):
            alpha = ['0', '1']
        
        if(input_clicked == "Octal"):
            alpha = [str(i) for i in range(8)]

        if(input_clicked == "Hexadecimal"):
            alpha = [str(i) if i < 10 else chr((i-10)+ord('a')) for i in range(16)]

        if(not alpha):
            return 2
        
        for s in input: 
            if not (s.lower() in alpha):
                return 3  
        
        if(input_clicked == output_clicked):
            return 4

        return 0
    
    # Cleanup function to call external class with static methods
    def convert(self, input, input_clicked, output_clicked):
        output = ""
        if(input_clicked == "Decimal"):
            if(output_clicked == "Binary"):
                return Converter.dec_to_bin(input)
            
            if(output_clicked == "Octal"):
                return Converter.dec_to_oct(input)
            
            if(output_clicked == "Hexadecimal"):
                return Converter.dec_to_hex(input)

        if(input_clicked == "Binary"):
            if(output_clicked == "Decimal"):
                return int(input, 2)
            
            if(output_clicked == "Octal"):
                return Converter.bin_to_oct(input)
            
            if(output_clicked == "Hexadecimal"):
                return Converter.bin_to_hex(input)
        
        if(input_clicked == "Octal"):
            if(output_clicked == "Decimal"):
                return int(input, 8)
            
            if(output_clicked == "Binary"):
                return Converter.oct_to_bin(input)

            if(output_clicked == "Hexadecimal"):
                # convert to binary then to hex
                bin = Converter.oct_to_bin(input)
                return Converter.bin_to_hex(bin)

        if(input_clicked == "Hexadecimal"):
            if(output_clicked == "Decimal"):
                return int(input, 16)

            if(output_clicked == "Binary"):
                return Converter.hex_to_bin(input)
        
            if(output_clicked == "Octal"):
                # convert to binary then to octal
                bin = Converter.hex_to_bin(input)
                return Converter.bin_to_oct(bin)

        return output

    def process_input(self, event=None):
        input          = self.input.get()
        input_clicked  = self.input_clicked.get()
        output_clicked = self.output_clicked.get()

        code = self.is_valid(input, input_clicked, output_clicked)

        if(code == 1):
            messagebox.showinfo("Alert", "Empty Input!")
            return

        if(code == 2):
            messagebox.showinfo("Alert", "Numeric system not found!")
            return

        if(code == 3):
            messagebox.showinfo("Alert", "Invalid input!")
            return

        if(code == 4):
            self.output_text.set(input)

        if(code == 0):
            self.output_text.set(self.convert(input, input_clicked, output_clicked))

class Converter():

    # converts a decimal number into a binary number
    @staticmethod
    def dec_to_bin(input : str) -> str:
        num    = int(input)
        output = ""
        
        while(num != 0): 
            output = str(num % 2) + output
            num //= 2
        return output
    
    # converts a decimal number into a octal number
    @staticmethod
    def dec_to_oct(input : str) -> str:
        num    = int(input)
        output = ""
        
        while(num != 0): 
            output = str(num % 8) + output
            num //= 8
        return output
    
    # converts a decimal number into a hexadecimal number
    # hex numbers > 9 will be represented by capital numbers A, B, ... , F
    @staticmethod
    def dec_to_hex(input : str) -> str:
        num    = int(input)
        output = ""
        
        while(num != 0): 
            rem = num % 16
            output = (str(rem) if rem < 10 else chr(rem-10 + ord("A"))) + output
            num //= 16
        return output
        
    # converts a binary number into a octal number 
    # uses the group by 3 method 
    @staticmethod
    def bin_to_oct(input: str) -> str:
        output = ""
        size   = len(input)
        arr = ["000", "001", "010", "011", "100", "101", "110", "111"]
        d   = {} 
        i   = 0
        for a in arr:
            d[a] = i 
            i += 1

        zeros = ""
        for i in range(3 - size % 3):
            zeros += '0'
        input = zeros + input
        
        size  = len(input)
        count = 0
        i = 0
        while(count < size // 3):
            output += str(d[input[i:(i+3)]])
            count += 1
            i += 3
        t = int(output) # get rid of preceeding zeros 
        output = str(t)
        return output
    
    # converts a binary number into a hexadecimal number 
    # uses the group by 4 method 
    @staticmethod
    def bin_to_hex(input: str) -> str:
        output = ""
        size   = len(input)
        arr = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
               "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
        d   = {} 
        i   = 0
        for a in arr:
            d[a] = i 
            i += 1

        zeros = ""
        for i in range(4 - size % 4):
            zeros += '0'
        input = zeros + input
        
        size  = len(input)
        count = 0
        i = 0
        while(count < size // 4):
            num = d[input[i:(i+4)]]
            output += str(num) if num < 10 else chr((num - 10) + ord("A"))
            count += 1
            i += 4

        # remove preceeding 0s 
        i = 0
        while(output[i] == '0'):
            i += 1
        output = output[i:len(output)]
        return output
    
    # converts octal number into a binary number
    @staticmethod
    def oct_to_bin(input: str) -> str:
        output = ""
        arr    = ["000", "001", "010", "011", "100", "101", "110", "111"]

        for i in input: 
            output += arr[int(i)]
        t = int(output) # get rid of preceeding zeros 
        output = str(t)
        return output
    
    # converts hexadecimal number into a binary number
    @staticmethod
    def hex_to_bin(input: str) -> str:
        output = ""
        arr = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
               "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
        for i in input: 
            num = int(i) if i.isdigit() else ord(i.lower()) - ord('a') + 10
            output += arr[num]
        t = int(output) # get rid of preceeding zeros 
        output = str(t)
        return output

if __name__ == "__main__":
    main()