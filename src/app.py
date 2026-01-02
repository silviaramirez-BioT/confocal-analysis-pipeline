import os
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pandas as pd

# Configuración inicial de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FluorescenceAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Analizador de Fluorescencia Confocal")
        self.geometry("800x650")
        
        # Estado de la aplicación
        self.input_file = None
        self.output_file = None
        
        self.create_widgets()
        
    def create_widgets(self):
        """Construye la interfaz gráfica."""
        
        # --- Título ---
        title_label = ctk.CTkLabel(
            self, 
            text="🔬 Analizador de Fluorescencia Confocal",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # --- Contenedor Principal ---
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # 1. Selección de Entrada
        ctk.CTkLabel(main_frame, text="1. Selecciona el archivo CSV (Fiji):", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5), anchor="w", padx=20)
        
        self.input_entry = ctk.CTkEntry(main_frame, placeholder_text="Seleccionar archivo...", width=500, state="readonly")
        self.input_entry.pack(pady=5, padx=20)
        
        ctk.CTkButton(main_frame, text="📁 Buscar CSV", command=self.select_input_file, width=200).pack(pady=5)
        
        # 2. Selección de Salida
        ctk.CTkLabel(main_frame, text="2. Destino del reporte Excel:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5), anchor="w", padx=20)
        
        self.output_entry = ctk.CTkEntry(main_frame, placeholder_text="Ubicación de guardado...", width=500, state="readonly")
        self.output_entry.pack(pady=5, padx=20)
        
        ctk.CTkButton(main_frame, text="💾 Seleccionar Destino", command=self.select_output_file, width=200).pack(pady=5)
        
        # 3. Opciones
        ctk.CTkLabel(main_frame, text="3. Configuración:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5), anchor="w", padx=20)
        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(options_frame, text="Área mínima (Filtro de ruido):").pack(side="left", padx=10, pady=10)
        self.threshold_entry = ctk.CTkEntry(options_frame, width=80)
        self.threshold_entry.pack(side="left", padx=5, pady=10)
        self.threshold_entry.insert(0, "0.05")
        
        # 4. Acción y Logs
        self.process_button = ctk.CTkButton(
            main_frame, text="▶️ PROCESAR DATOS", command=self.process_data,
            width=300, height=50, font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71", hover_color="#27ae60"
        )
        self.process_button.pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=500)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        self.status_text = ctk.CTkTextbox(main_frame, width=700, height=120)
        self.status_text.pack(pady=10, padx=20)
        self.log_message("✅ Sistema listo. Esperando archivos...")

    def log_message(self, message):
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")

    def select_input_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if filename:
            self.input_file = filename
            self.update_entry(self.input_entry, filename)
            self.log_message(f"📂 Entrada: {os.path.basename(filename)}")
            
            # Autogenerar salida
            if not self.output_file:
                suggested = str(Path(filename).parent / "Reporte_Analisis.xlsx")
                self.output_file = suggested
                self.update_entry(self.output_entry, suggested)

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if filename:
            self.output_file = filename
            self.update_entry(self.output_entry, filename)

    def update_entry(self, entry_widget, text):
        entry_widget.configure(state="normal")
        entry_widget.delete(0, "end")
        entry_widget.insert(0, text)
        entry_widget.configure(state="readonly")

    def process_data(self):
        if not self.input_file or not self.output_file:
            messagebox.showerror("Error", "Faltan archivos por seleccionar.")
            return
            
        self.process_button.configure(state="disabled", text="⏳ Procesando...")
        self.progress_bar.set(0)
        threading.Thread(target=self._run_analysis, daemon=True).start()

    def _run_analysis(self):
        try:
            area_limit = float(self.threshold_entry.get() or 0.05)
            self.log_message(f"\n🚀 Iniciando análisis (Filtro Área > {area_limit})...")
            self.progress_bar.set(0.2)
            
            # Lectura y Procesamiento
            df = pd.read_csv(self.input_file)
            
            # Extracción de metadatos del Label (Asumiendo formato 'C1-NombreImagen')
            df['Channel'] = df['Label'].apply(lambda x: x.split('-')[0] if '-' in str(x) else 'C1')
            df['Cell_ID'] = df.groupby('Channel').cumcount() + 1
            
            self.progress_bar.set(0.4)
            
            # Pivotar tabla
            df_pivot = df.pivot(index='Cell_ID', columns='Channel', values=['Area', 'Mean'])
            df_pivot.columns = [f"{col[0]}_{col[1]}" for col in df_pivot.columns]
            df_pivot = df_pivot.reset_index()
            
            # Filtrado
            total_cells = len(df_pivot)
            df_pivot = df_pivot[df_pivot.get('Area_C1', 0) > area_limit]
            self.log_message(f"🧹 Filtrado: {total_cells} -> {len(df_pivot)} células válidas.")
            
            self.progress_bar.set(0.6)
            
            # Cálculos Biológicos (Ratios e Intensidades)
            # Validamos que existan las columnas antes de calcular
            if 'Mean_C2' in df_pivot.columns and 'Mean_C1' in df_pivot.columns:
                df_pivot['Ratio_Verde_Azul_%'] = (df_pivot['Mean_C2'] / df_pivot['Mean_C1']) * 100
                df_pivot['Intensidad_Verde_Norm_%'] = (df_pivot['Mean_C2'] / 255) * 100
                
            if 'Mean_C3' in df_pivot.columns and 'Mean_C1' in df_pivot.columns:
                df_pivot['Ratio_Rojo_Azul_%'] = (df_pivot['Mean_C3'] / df_pivot['Mean_C1']) * 100
                df_pivot['Intensidad_Rojo_Norm_%'] = (df_pivot['Mean_C3'] / 255) * 100

            self.progress_bar.set(0.8)
            
            # Guardado
            df_pivot.to_excel(self.output_file, index=False)
            self.progress_bar.set(1.0)
            self.log_message(f"✅ ¡Éxito! Archivo guardado en:\n{self.output_file}")
            
            self.after(0, lambda: messagebox.showinfo("Completado", "Análisis finalizado con éxito."))

        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.after(0, lambda: self.process_button.configure(state="normal", text="▶️ PROCESAR DATOS"))

if __name__ == "__main__":
    app = FluorescenceAnalyzerApp()
    app.mainloop()