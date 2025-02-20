import os
import mysql.connector
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox

# Cargar las variables de entorno (.env)
load_dotenv() # Esto hay que retirarlo cuando se cree el .exe

def open_tunnel():
    """Crea y retorna un túnel SSH usando las variables de entorno."""
    return SSHTunnelForwarder(
        (os.getenv("SSH_HOST"), int(os.getenv("SSH_PORT", 22))),                    # Reemplazar con lsa credenciales cuando se haga el .exe
        ssh_username=os.getenv("SSH_USERNAME"),                                     # Reemplazar con lsa credenciales cuando se haga el .exe
        ssh_password=os.getenv("SSH_PASSWORD"),                                     # Reemplazar con lsa credenciales cuando se haga el .exe
        allow_agent=False,
        remote_bind_address=(os.getenv("DB_HOST"), int(os.getenv("DB_PORT", 3306))) # Reemplazar con lsa credenciales cuando se haga el .exe
    )

def get_db_connection(tunnel):
    """Retorna una conexión a la base de datos utilizando el puerto local del túnel SSH."""
    return mysql.connector.connect(
        host='127.0.0.1',
        port=tunnel.local_bind_port,
        user=os.getenv("DB_USERNAME"),                                              # Reemplazar con lsa credenciales cuando se haga el .exe
        password=os.getenv("DB_PASSWORD"),                                          # Reemplazar con lsa credenciales cuando se haga el .exe
        database=os.getenv("DB_NAME")   /var                                        # Reemplazar con lsa credenciales cuando se haga el .exe
    )

def fetch_order_addresses(order_id):
    """Ejecuta la consulta SELECT en view_order_address para el pedido indicado."""
    query = "SELECT * FROM view_order_address WHERE OrderID = %s"
    with open_tunnel() as tunnel:
        conn = get_db_connection(tunnel)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (order_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    return results

def update_order_addresses(order_id, delivery_addr, invoice_addr):
    """Actualiza la tabla ps_orders para asignar las nuevas direcciones de entrega y facturación."""
    query = """
    UPDATE ps_orders
    SET id_address_delivery = %s,
        id_address_invoice = %s
    WHERE id_order = %s
    """
    with open_tunnel() as tunnel:
        conn = get_db_connection(tunnel)
        cursor = conn.cursor()
        cursor.execute(query, (delivery_addr, invoice_addr, order_id))
        conn.commit()
        cursor.close()
        conn.close()

# Variables globales para almacenar la lista de direcciones y el mapeo de texto a AddressID
addresses_mapping = {}

def buscar_direcciones():
    """Función llamada al pulsar 'Buscar direcciones': consulta la DB y actualiza los combobox."""
    global addresses_mapping
    order_id_text = entry_order.get().strip()
    if not order_id_text.isdigit():
        messagebox.showerror("Error", "El ID del pedido debe ser un número entero.")
        return

    order_id = int(order_id_text)
    try:
        addresses = fetch_order_addresses(order_id)
    except Exception as e:
        messagebox.showerror("Error en la conexión", f"No se pudo conectar a la base de datos:\n{e}")
        return

    if not addresses:
        messagebox.showinfo("Información", "No se encontraron direcciones para ese pedido.")
        return

    # Preparar la lista de direcciones para los combobox
    display_list = []
    addresses_mapping = {}  # Reiniciar el mapeo
    for addr in addresses:
        # Formato: "ID: <AddressID> - <Address> - <FirstName> <LastName>"
        display_text = f"ID: {addr['AddressID']} - {addr['Address']} - {addr['FirstName']} {addr['LastName']}"
        display_list.append(display_text)
        addresses_mapping[display_text] = addr['AddressID']

    # Actualizar los combobox
    delivery_combo['values'] = display_list
    invoice_combo['values'] = display_list

    # Seleccionar por defecto el primer elemento
    if display_list:
        delivery_var.set(display_list[0])
        invoice_var.set(display_list[0])
    
    messagebox.showinfo("Direcciones encontradas", f"Se encontraron {len(display_list)} direcciones.")

def actualizar_pedido():
    """Función llamada al pulsar 'Actualizar pedido': toma las selecciones y actualiza el pedido."""
    order_id_text = entry_order.get().strip()
    if not order_id_text.isdigit():
        messagebox.showerror("Error", "El ID del pedido debe ser un número entero.")
        return
    order_id = int(order_id_text)

    delivery_selection = delivery_var.get()
    invoice_selection = invoice_var.get()
    if not delivery_selection or not invoice_selection:
        messagebox.showerror("Error", "Debes seleccionar ambas direcciones.")
        return

    delivery_address_id = addresses_mapping.get(delivery_selection)
    invoice_address_id = addresses_mapping.get(invoice_selection)

    # Confirmación
    confirm = messagebox.askyesno("Confirmar actualización",
        f"¿Deseas actualizar el pedido {order_id}?\n\nEntrega: {delivery_selection}\nFacturación: {invoice_selection}")
    if not confirm:
        return

    try:
        update_order_addresses(order_id, delivery_address_id, invoice_address_id)
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar el pedido:\n{e}")
        return

    messagebox.showinfo("Éxito", "El pedido se actualizó correctamente.")

# Configuración de la interfaz Tkinter
root = tk.Tk()
root.title("Cambio de Direcciones - PrestaShop")
root.geometry("680x300")
root.resizable(False, False)

# Frame para ingresar el ID del pedido y buscar direcciones
frame_order = tk.Frame(root, padx=10, pady=10)
frame_order.pack(fill=tk.X)

label_order = tk.Label(frame_order, text="ID del Pedido:")
label_order.pack(side=tk.LEFT)

entry_order = tk.Entry(frame_order, width=10)
entry_order.pack(side=tk.LEFT, padx=5)

button_buscar = tk.Button(frame_order, text="Buscar direcciones", command=buscar_direcciones)
button_buscar.pack(side=tk.LEFT, padx=5)

# Frame para mostrar las direcciones y permitir la selección
frame_addresses = tk.Frame(root, padx=10, pady=10)
frame_addresses.pack(fill=tk.X)

# Combobox para Dirección de Entrega
delivery_var = tk.StringVar()
label_delivery = tk.Label(frame_addresses, text="Dirección de Entrega:")
label_delivery.grid(row=0, column=0, sticky=tk.W, pady=5)
delivery_combo = ttk.Combobox(frame_addresses, textvariable=delivery_var, state="readonly", width=80)
delivery_combo.grid(row=0, column=1, pady=5, padx=5)

# Combobox para Dirección de Facturación
invoice_var = tk.StringVar()
label_invoice = tk.Label(frame_addresses, text="Dirección de Facturación:")
label_invoice.grid(row=1, column=0, sticky=tk.W, pady=5)
invoice_combo = ttk.Combobox(frame_addresses, textvariable=invoice_var, state="readonly", width=80)
invoice_combo.grid(row=1, column=1, pady=5, padx=5)

# Botón para actualizar el pedido
button_actualizar = tk.Button(root, text="Actualizar pedido", command=actualizar_pedido, padx=10, pady=5)
button_actualizar.pack(pady=10)

root.mainloop()
