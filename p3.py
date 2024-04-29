def f(x):
    return 3*x**2 - 4*x + 1

def df(x):
    return 6*x - 4

def newton_raphson(initial_guess, error_threshold):
    x = initial_guess
    iteration = 1
    while True:
        x_next = x - f(x) / df(x)
        error = abs((x_next - x) / x_next) * 100
        print("Iteración {}: x = {:.6f}, error = {:.6f}%".format(iteration, x_next, error))
        if error <= error_threshold:
            break
        x = x_next
        iteration += 1
    return x_next

initial_guess = 2
error_threshold = 1
root = newton_raphson(initial_guess, error_threshold)
print("\nLa raíz aproximada es:", root)
