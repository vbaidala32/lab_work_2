import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, messagebox, END


# Функція для побудови інтерполяційного багаточлена Лагранжа
def lagrange_polynomial(x_values, y_values):
    x = sp.Symbol('x')
    n = len(x_values)
    polynomial = 0

    for i in range(n):
        polynomial_term = y_values[i]
        for j in range(n):
            if i != j:
                polynomial_term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        polynomial += polynomial_term

    # Спрощення багаточлена
    return sp.simplify(polynomial)


# Функція для перетворення полінома в рядковий формат
def polynomial_to_string(polynomial, use_caret=True):
    formatted_poly_str = sp.sstr(polynomial).replace("**", "^" if use_caret else "**")
    return formatted_poly_str


# Функція для побудови інтерполяційного багаточлена Лагранжа
def lagrange_interpolation(x_values, y_values, x):
    n = len(x_values)
    result = 0

    for i in range(n):
        polynomial_term = y_values[i]
        for j in range(n):
            if i != j:
                polynomial_term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += polynomial_term
    return result


# Функція для побудови графіка
def plot_graph(x_values, y_values, approx_points, approx_values):
    x_plot = np.linspace(min(x_values) - 1, max(x_values) + 1, 1000)
    y_plot = [lagrange_interpolation(x_values, y_values, x) for x in x_plot]

    plt.plot(x_plot, y_plot, label='Ln(x)', color='blue')

    # Відображення початкових точок
    plt.scatter(x_values, y_values, color='red', label='Starting points')

    # Відображення наближених точок
    plt.scatter(approx_points, approx_values, color='green', label='Approximate points')

    plt.xlabel('x')
    plt.ylabel('Ln(x)')
    plt.title('Interpolation Lagrange polynomial')
    plt.legend()
    plt.grid(True)
    plt.show()


# Функція для обробки натискання кнопки
def calculate(entry_x, entry_y, entry_approx_points, text_output):
    try:
        # Отримання значень
        x_values = list(map(float, entry_x.get().split()))
        y_values = list(map(float, entry_y.get().split()))

        if len(x_values) != len(y_values):
            raise ValueError("You must enter same number of values for x and f(x).")

        approximate_points = list(map(float, entry_approx_points.get().split()))
        approximate_values = [lagrange_interpolation(x_values, y_values, x) for x in approximate_points]

        # Очищення текстового поля для виведення результатів
        text_output.delete(1.0, END)

        # Побудова багаточлена Лагранжа за допомогою SymPy
        polynomial = lagrange_polynomial(x_values, y_values)

        # Виведення багаточлена зі степенями у форматі "^"
        formatted_polynomial = polynomial_to_string(polynomial, use_caret=True)
        text_output.insert(END, f"Ln(x) = {formatted_polynomial}\n\n")

        # Виведення наближених значень
        text_output.insert(END, "Approximate values of the function:\n")
        for x, y in zip(approximate_points, approximate_values):
            text_output.insert(END, f"f({x}) ≈ {round(y, 3)}\n")

        # Побудова графіка в окремому вікні
        plot_graph(x_values, y_values, approximate_points, approximate_values)

    except ValueError as e:
        messagebox.showerror("Error", str(e))


# Функція для запуску інтерфейсу
def run_program():
    root = Tk()
    root.title("Lagrange interpolation")

    Label(root, text="Enter 4 values for x (separated by a space):").grid(row=0, column=0, columnspan=2)
    entry_x = Entry(root)
    entry_x.grid(row=1, column=0, columnspan=2)

    Label(root, text="Enter the 4 matching values for f(x) (separated by a space):").grid(row=2, column=0, columnspan=2)
    entry_y = Entry(root)
    entry_y.grid(row=3, column=0, columnspan=2)

    Label(root, text="Enter points for approximate values (separated by a space):").grid(row=4, column=0, columnspan=2)
    entry_approx_points = Entry(root)
    entry_approx_points.grid(row=5, column=0, columnspan=2)

    button_calculate = Button(root, text="Calculate", command=lambda: calculate(entry_x, entry_y, entry_approx_points, text_output))
    button_calculate.grid(row=6, column=0, columnspan=2)

    # Текстове поле для виведення багаточлена та наближених значень
    text_output = Text(root, height=10, width=50)
    text_output.grid(row=7, column=0, columnspan=2)

    # Додаємо прокрутку, якщо результати будуть великими
    scroll = Scrollbar(root, command=text_output.yview)
    text_output.config(yscrollcommand=scroll.set)
    scroll.grid(row=7, column=2, sticky='nsew')

    root.mainloop()


# Головний блок
if __name__ == '__main__':
    run_program()


