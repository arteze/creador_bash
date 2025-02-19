#!/bin/python

import tkinter as tk
from tkinter import ttk

class DraggableEntry(ttk.Entry):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		self.bind("<Button-1>", self.start_drag)

	def start_drag(self, event):
		self._drag_start_x = event.x
		self._drag_start_y = event.y
		self.bind("<B1-Motion>", self.drag)
		self.bind("<ButtonRelease-1>", self.stop_drag)

	def drag(self, event):
		x = event.x - self._drag_start_x
		y = event.y - self._drag_start_y
		self.place(x=self.winfo_x() + x, y=self.winfo_y() + y)

	def stop_drag(self, event):
		self.unbind("<B1-Motion>")
		self.unbind("<ButtonRelease-1>")

def actualizar_orden():
	global entradas
	posiciones = [(entry.winfo_y(), entry) for entry in entradas]
	posiciones.sort()
	entradas = [entry for _, entry in posiciones]

def crear_comando():
	global entradas
	comando = base_cmd.get()

	# Ordenar las entradas por su posición vertical antes de combinarlas
	entradas.sort(key=lambda entry: entry.winfo_y())  # Ordenar de arriba a abajo

	args = [entry.get() for entry in entradas if entry.get()]
	for arg in args:
		comando += " " + arg
	resultado.set(comando)

def cambiar_foco(event):
	widget = event.widget
	try:
		index = entradas.index(widget)
	except ValueError:
		return
	next_index = (index + 1) % len(entradas)
	entradas[next_index].focus_set()
	return "break"

def mover_entrada(index, direccion):
	global entradas
	if direccion == "arriba" and index > 0:
		entradas[index], entradas[index - 1] = entradas[index - 1], entradas[index]
	elif direccion == "abajo" and index < len(entradas) - 1:
		entradas[index], entradas[index + 1] = entradas[index + 1], entradas[index]
	
	# Reordenar visualmente los inputs
	for i, entry in enumerate(entradas):
		entry.grid(row=i+1, column=1)

# Ventana principal
ventana = tk.Tk()
ventana.title("Creador de Comandos Bash")

# Comando base
base_cmd_label = ttk.Label(ventana, text="Comando Base:")
base_cmd_label.grid(row=0, column=0, padx=0, pady=0)
base_cmd = ttk.Entry(ventana)
base_cmd.grid(row=0, column=1, padx=0, pady=0)

# Argumentos
entradas = []
for i in range(3):
	label = ttk.Label(ventana, text=f"Argumento {i+1}:")
	label.grid(row=i+1, column=0, padx=0, pady=0)
	entry = DraggableEntry(ventana)
	entry.grid(row=i+1, column=1, padx=0, pady=0)
	entradas.append(entry)
	entry.bind("<Tab>", cambiar_foco)
	
	# Botones para subir y bajar
	boton_arriba = ttk.Button(ventana, text="↑", command=lambda idx=i: mover_entrada(idx, "arriba"))
	boton_arriba.grid(row=i+1, column=2, padx=0, pady=0)
	boton_abajo = ttk.Button(ventana, text="↓", command=lambda idx=i: mover_entrada(idx, "abajo"))
	boton_abajo.grid(row=i+1, column=3, padx=0, pady=0)

# Botón de creación
crear_btn = ttk.Button(ventana, text="Crear Comando", command=crear_comando)
crear_btn.grid(row=4, column=0, columnspan=4, padx=0, pady=10)

# Resultado
resultado = tk.StringVar()
resultado_label = ttk.Label(ventana, text="Comando Resultante:")
resultado_label.grid(row=5, column=0, padx=0, pady=0)
resultado_entry = ttk.Entry(ventana, textvariable=resultado, state="readonly")
resultado_entry.grid(row=5, column=1, columnspan=3, padx=0, pady=0)

# Evento para actualizar el orden al soltar una entrada
for entry in entradas:
	entry.bind("<ButtonRelease-1>", lambda event: actualizar_orden())

ventana.mainloop()
