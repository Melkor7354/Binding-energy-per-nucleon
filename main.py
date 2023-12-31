import tkinter as tk
import csv
import matplotlib.pyplot as plt

file = open('elements_and_isotopes.csv', 'r')
file1 = open('all_elements.csv', 'r')
dat = csv.reader(file)
dat1 = csv.reader(file1)
data = []
data1 = []
for i in dat:
    data.append(i)
for i in dat1:
    data1.append(i)
primary = 'black'
secondary = 'dark blue'
text = 'white'
font = ['Courier', 12]
title = ['Courier', 16]
mass_proton = 1.007277
mass_neutron = 1.008665
elements = []
for j in data:
    if j[0] in elements:
        pass
    else:
        elements.append(j[0])


class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title("Binding Energy per Nucleon Calculator")
        self.minsize(int(self.winfo_screenwidth()//1.8), int(self.winfo_screenheight()//1.8))
        self.maxsize(int(self.winfo_screenwidth()//1.8), int(self.winfo_screenheight()//1.8))
        self.switch_frame(Menu)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class Calculator(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=Interface.winfo_screenheight(self), width=Interface.winfo_screenwidth(self), bg=primary)
        HomeButton(command=lambda: master.switch_frame(Menu)).place(relx=0.002, rely=0.92)
        self.warning = tk.Label(text='''Enter Atomic Number and Atomic mass of isotope''',
                                bg=primary, fg=text, font=font)
        self.warning.place(relx=0.2, rely=0.02)
        self.number = tk.Entry(bg=secondary, fg=text, width=20, font=font)
        self.mass = tk.Entry(bg=secondary, fg=text, width=20, font=font)
        self.number_label = tk.Label(text="Enter Atomic Number (Z)", font=font, bg=primary, fg=text)
        self.mass_label = tk.Label(text='Enter Atomic Mass (A)', font=font, bg=primary, fg=text)
        self.number.place(relx=0.5, rely=0.1)
        self.mass.place(relx=0.5, rely=0.2)
        self.number_label.place(relx=0.19, rely=0.1)
        self.mass_label.place(relx=0.2, rely=0.2)
        self.element = DisplayLabel(display="Element: ")
        self.Z = DisplayLabel(display="Atomic Number: ")
        self.A = DisplayLabel(display="Atomic Mass: ")
        self.delta_m = DisplayLabel(display="Mass Defect: ")
        self.binding_energy = DisplayLabel(display="Binding Energy: ")
        self.energy_per_nucleon = DisplayLabel(display="Energy per Nucleon: ")
        self.Z.place(relx=0.2, rely=0.4)
        self.A.place(relx=0.5, rely=0.4)
        self.delta_m.place(relx=0.2, rely=0.5)
        self.binding_energy.place(relx=0.2, rely=0.6)
        self.energy_per_nucleon.place(relx=0.2, rely=0.7)

        submit = tk.Button(text='SUBMIT', command=lambda: self.display(self.number.get(), self.mass.get()), fg=text,
                           bg=secondary, font=font)
        submit.place(relx=0.42, rely=0.29)

    def display(self, atomic_number, atomic_mass):
        try:
            z = int(atomic_number)
            a = int(atomic_mass)

            isotope_found = 0
            for i in data1:
                if (i[0] == atomic_number) and (i[3] == atomic_mass):
                    isotope_found = 1
                    m = (z * mass_proton) + ((a-z) * mass_neutron) - float(i[4])
                    be = m * 931.5
                    e = be / a
                    self.element.config(text=f"Element: {i[2]}")
                    self.Z.config(text=f"Atomic Number: {z} amu")
                    self.A.config(text=f"Atomic Mass: {a} amu")
                    self.delta_m.config(text=f"Mass defect: {m} amu")
                    self.binding_energy.config(text=f"Binding Energy: {be} MeV")
                    self.energy_per_nucleon.config(text=f"Energy Per Nucleon: {e} MeV")
                    break
                else:
                    pass
            if isotope_found == 0:
                self.warning.config(text="Isotope Not Found")
                self.warning.place(relx=0.3, rely=0.02)
        except ValueError:
            self.warning.config(text="Please enter integers as Z and A.")
            self.warning.place(relx=0.3, rely=0.02)
            return False


class Menu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self)
        self.config(height=Interface.winfo_screenheight(self), width=Interface.winfo_screenwidth(self), bg=primary)
        MenuButton(display='Calculator', command=lambda: master.switch_frame(Calculator)).place(relx=0.4, rely=0.5)
        MenuButton(display='Graph', command=graph).place(relx=0.4, rely=0.7)
        tk.Label(text="Binding Energy Calculator", bg=secondary, fg=text, font=title).place(relx=0.3, rely=0.2)


class HomeButton(tk.Button):
    def __init__(self, command):
        tk.Button.__init__(self)
        self.command = command
        self['command'] = self.command
        self.config(bg=secondary, fg=text, text="Return to home page", font=font)


class MenuButton(tk.Button):
    def __init__(self, display, command):
        tk.Button.__init__(self)
        self.config(width=15, bg=secondary, fg=text, font=font)
        self.text = display
        self.command = command
        self['command'] = self.command
        self['text'] = self.text


class DisplayLabel(tk.Label):
    def __init__(self, display):
        tk.Label.__init__(self)
        self.config(bg=primary, fg=text, font=font)
        self.text = display
        self['text'] = self.text


def graph():
    fig, ax = plt.subplots()
    x = []
    y = []
    for i in elements:
        total = 0
        count = 0
        total_mass = 0
        for j in data:
            if i == j[0]:
                m = (int(j[0]) * mass_proton) + (((int(j[3]) - int((j[0]))) * mass_neutron) - float(j[4]))
                be = m * 931.5
                e = be / int(j[3])
                total += e
                count += 1
                total_mass += int(j[3])
            else:
                pass

        average_be = total/count
        average_mass = total_mass/count
        if average_be > 0:
            x.append(average_mass)
            y.append(average_be)
        else:
            pass

    plt.plot(x, y, '-r')
    plt.title(r'Variation of Binding Energy per Nucleon with Atomic Mass')
    plt.axhline(linewidth=2, color='grey')
    plt.axvline(linewidth=2, color='grey')
    plt.ylabel("Binding Energy per Nucleon in MeV")
    plt.xlabel("Atomic Mass")
    plt.grid(axis='both', color='grey')
    plt.axvline(x=60, color='black')
    plt.annotate('Fusion', xy=(55, 6), xytext=(10, 6), arrowprops=dict(arrowstyle='->',
                                                                       color='red',
                                                                       lw=3,
                                                                       ls='--'))
    plt.annotate('Fission', xy=(65, 6), xytext=(110, 6), arrowprops=dict(arrowstyle='->',
                                                                         color='red',
                                                                         lw=3,
                                                                         ls='--'))
    ax.set_facecolor('white')
    plt.show()


app = Interface()
app.mainloop()
