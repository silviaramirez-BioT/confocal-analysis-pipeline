// =======================================================
// MACRO FINAL: MEDICIÓN COMPLETA (Área + Intensidad + Perímetro)
// =======================================================

// --- 1. CONFIGURACIÓN ---
var tamMinimo = 0.70;       
var tamMaximo = "Infinity"; 
var circMinima = 0.0;       

// --- CONFIGURACIÓN VISUAL ---
var barraAncho = 10;        
var barraColor = "White";   
var barraPos   = "Lower Right"; 
// ----------------------------

run("Close All"); 
print("\\Clear"); 

pathArchivo = File.openDialog("Selecciona el archivo .LIF");
dirSalida = getDirectory("Selecciona la carpeta para guardar resultados");

dirProcesados = dirSalida + "Procesados_Canales" + File.separator; 
dirResultados = dirSalida + "Resultados_CSV" + File.separator;
dirRGB = dirSalida + "Imagenes_RGB" + File.separator; 

File.makeDirectory(dirProcesados);
File.makeDirectory(dirResultados);
File.makeDirectory(dirRGB);

run("Bio-Formats Macro Extensions");
Ext.setId(pathArchivo);
Ext.getSeriesCount(numSeries);
print("Se encontraron " + numSeries + " series.");

// --- AQUÍ ESTÁ EL CAMBIO: ACTIVAMOS TODO ---
// area = Área
// perimeter = Circunferencia
// mean, standard, min, integrated = Intensidades
// area_fraction = % de Área
// shape = Circularidad
run("Set Measurements...", "area mean standard min perimeter shape integrated area_fraction display redirect=None decimal=3");

// =======================================================
// BUCLE PRINCIPAL
// =======================================================
for (i = 0; i < numSeries; i++) {
    
    // Abrir serie
    run("Bio-Formats Importer", "open=[" + pathArchivo + "] autoscale color_mode=Composite view=Hyperstack stack_order=XYCZT series_" + (i+1));
    tituloOriginal = getTitle();
    
    // Leer dimensiones (Detectar canales)
    Stack.getDimensions(width, height, channels, slices, frames);
    print("Procesando serie " + (i+1) + ": " + tituloOriginal + " (" + channels + " canales)");

    c1_window = "";
    c2_window = "";
    c3_window = "";
    
    // --- LÓGICA DE CANALES (1, 2 o 3) ---
    if (channels > 1) {
        run("Split Channels");
        c1_window = "C1-" + tituloOriginal; 
        c2_window = "C2-" + tituloOriginal; 
        if (channels >= 3) { c3_window = "C3-" + tituloOriginal; }
        
        // Merge para visualización
        selectWindow(c1_window); run("Duplicate...", "title=C1-Original"); 
        selectWindow("C1-Original"); run("Duplicate...", "title=Azul-Merge");
        selectWindow(c2_window);     run("Duplicate...", "title=Verde-Merge");
        
        comandoMerge = "c1=[Azul-Merge] c2=[Verde-Merge] ";
        if (channels >= 3) {
            selectWindow(c3_window); run("Duplicate...", "title=Rojo-Merge");
            comandoMerge = comandoMerge + "c3=[Rojo-Merge] ";
        }
        run("Merge Channels...", comandoMerge + "create");
        run("Scale Bar...", "width="+barraAncho+" height=4 font=14 color="+barraColor+" background=None location=["+barraPos+"] bold overlay");
        run("Flatten"); 
        saveAs("PNG", dirRGB + "Composite_Serie_" + (i+1) + ".png");
        close(); 
        if (isOpen("Composite")) { selectWindow("Composite"); close(); }
    
    } else {
        // Caso Monocanal
        c1_window = tituloOriginal; 
        selectWindow(c1_window);
        run("Duplicate...", "title=C1-Original");
    }

    // --- PROCESAMIENTO DE MÁSCARA (Definición Alta) ---
    selectWindow(c1_window);
    run("Median...", "radius=1"); 
    run("Subtract Background...", "rolling=20"); 
    run("Auto Threshold", "method=Triangle white");
    run("Convert to Mask"); 
    run("Fill Holes");  
    run("Watershed");   

    // Detectar ROIs
    run("Analyze Particles...", "size=" + tamMinimo + "-" + tamMaximo + " circularity=" + circMinima + "-1.00 show=Nothing add");
    
    numROIs = roiManager("count");
    
    if (numROIs > 0) {
        // --- MEDIR (Aquí se aplicarán las medidas definidas arriba) ---
        
        // Canal 1 (Azul)
        selectWindow("C1-Original"); 
        roiManager("Measure"); 
        
        // Canal 2 (Verde - si existe)
        if (channels > 1) {
             selectWindow(c2_window); roiManager("Measure");
        }
        // Canal 3 (Rojo - si existe)
        if (channels > 2) {
            selectWindow(c3_window); roiManager("Measure"); 
        }
        
        // Guardar CSV
        selectWindow("Results");
        saveAs("Results", dirResultados + "Resultados_Serie_" + (i+1) + ".csv");
        run("Clear Results");
        roiManager("Delete");
    } else {
        print("   Advertencia: No se detectaron objetos en la serie " + (i+1));
    }

    // --- GUARDAR MÁSCARA E IMÁGENES INDIVIDUALES ---
    selectWindow(c1_window); 
    run("Scale Bar...", "width="+barraAncho+" height=4 font=14 color="+barraColor+" background=None location=["+barraPos+"] bold overlay");
    run("Flatten"); 
    saveAs("Tiff", dirProcesados + "Mask_Serie_" + (i+1) + ".tif");
    close(); 

    selectWindow("C1-Original");
    run("Scale Bar...", "width="+barraAncho+" height=4 font=14 color="+barraColor+" background=None location=["+barraPos+"] bold overlay");
    run("Flatten"); 
    saveAs("Tiff", dirProcesados + "C1_Azul_Serie_" + (i+1) + ".tif");
    close();

    if (channels > 1) {
        selectWindow(c2_window);
        run("Scale Bar...", "width="+barraAncho+" height=4 font=14 color="+barraColor+" background=None location=["+barraPos+"] bold overlay");
        run("Flatten");
        saveAs("Tiff", dirProcesados + "C2_Verde_Serie_" + (i+1) + ".tif");
        close(); 
    }

    if (channels > 2) {
        selectWindow(c3_window);
        run("Scale Bar...", "width="+barraAncho+" height=4 font=14 color="+barraColor+" background=None location=["+barraPos+"] bold overlay");
        run("Flatten");
        saveAs("Tiff", dirProcesados + "C3_Rojo_Serie_" + (i+1) + ".tif");
        close();
    }

    run("Close All");
}

showMessage("¡Proceso Terminado!");