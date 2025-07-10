import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def process_image(input_path, output_folder, filename):
    # 1. Grayscale
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Gagal membaca gambar dari: {input_path}")

    gray_path = os.path.join(output_folder, f"gray_{filename}")
    cv2.imwrite(gray_path, image)

    # 2. CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(image)
    colored_clahe = cv2.applyColorMap(enhanced, cv2.COLORMAP_JET)
    clahe_path = os.path.join(output_folder, f"clahe_{filename}")
    cv2.imwrite(clahe_path, colored_clahe)

    # 3. Edge Detection
    edges = cv2.Canny(enhanced, 30, 100)
    edge_overlay = colored_clahe.copy()
    edge_overlay[edges != 0] = [0, 0, 255]
    edge_path = os.path.join(output_folder, f"edge_{filename}")
    cv2.imwrite(edge_path, edge_overlay)

    # 4. Hitung edge count
    edge_count = int(np.count_nonzero(edges))

    # 5. Histogram dari hasil CLAHE
    hist_path = os.path.join(output_folder, f"hist_{filename}.png")
    plt.figure(figsize=(4, 3))
    plt.hist(enhanced.ravel(), bins=256, range=(0, 256), color='blue', alpha=0.7)
    plt.title('Histogram Intensitas')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(hist_path)
    plt.close()

    # 6. Return semua path
    return {
        'gray': gray_path.replace('\\', '/'),
        'clahe': clahe_path.replace('\\', '/'),
        'edge': edge_path.replace('\\', '/'),
        'edge_count': edge_count,
        'histogram': hist_path.replace('\\', '/')
    }
