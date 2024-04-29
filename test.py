my_string = "python"
x = 0
for i in my_string:
    x = x + 1
print(my_string[0:x])

x = len(my_string)  # Reiniciar x al tamaño de la cadena
for i in my_string:
    x = x - 1
    print(my_string[0:x])
