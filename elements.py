import pandas as pd
from periodictable import elements

# Creating lists to store data
atomic_numbers = []
element_symbols = []
element_names = []
mass_numbers = []
mass_of_nucleus = []


def get_mass_number(isotope):
    a = str(isotope)
    b = ''
    for i in a:
        if i == '-':
            break
        else:
            b += i
    if b == 'D':
        b = 2
    elif b == 'T':
        b = 3
    else:
        b = int(b)
    return b

# Looping through all elements
for element in elements:
    for isotope in element:
        atomic_numbers.append(element.number)
        element_symbols.append(element.symbol)
        element_names.append(element.name)
        mass_numbers.append(get_mass_number(isotope))
        mass_of_nucleus.append(isotope.mass)

# Creating a DataFrame
data = {
    'Atomic Number': atomic_numbers,
    'Element Symbol': element_symbols,
    'Element Name': element_names,
    'Mass Number': mass_numbers,
    'Mass of Nucleus': mass_of_nucleus
}

df = pd.DataFrame(data)

# Writing DataFrame to CSV
df.to_csv('all_elements.csv', index=False)
