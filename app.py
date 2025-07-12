import streamlit as st
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Optimasi Produksi", layout="centered")

st.title("📈 Aplikasi Optimasi Produksi (Linear Programming)")
st.markdown("Masukkan parameter di bawah ini untuk menghitung kombinasi produk optimal.")

# Input
a1 = st.number_input("Keuntungan per unit Produk A", value=40)
a2 = st.number_input("Keuntungan per unit Produk B", value=30)
b1 = st.number_input("Bahan baku per unit A (kg)", value=2)
b2 = st.number_input("Bahan baku per unit B (kg)", value=1)
total_bahan = st.number_input("Total bahan baku tersedia (kg)", value=100)
c1 = st.number_input("Jam kerja per unit A", value=1)
c2 = st.number_input("Jam kerja per unit B", value=2)
total_jam = st.number_input("Total jam kerja tersedia", value=80)

if st.button("Hitung Optimasi"):
    # Fungsi objektif
    c = [-a1, -a2]
    # Kendala
    A = [[b1, b2], [c1, c2]]
    b = [total_bahan, total_jam]
    bounds = [(0, None), (0, None)]

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        x, y = res.x
        st.success(f"Jumlah optimal produksi:")
        st.write(f"Produk A: {x:.2f} unit")
        st.write(f"Produk B: {y:.2f} unit")
        st.write(f"Total keuntungan maksimal: Rp {-res.fun:.2f}")

        # Visualisasi
        x_vals = np.linspace(0, max(x+10, 50), 400)
        y1 = (total_bahan - b1 * x_vals) / b2
        y2 = (total_jam - c1 * x_vals) / c2

        plt.figure(figsize=(8,6))
        plt.plot(x_vals, y1, label="Kendala Bahan Baku")
        plt.plot(x_vals, y2, label="Kendala Jam Kerja")
        plt.fill_between(x_vals, np.minimum(y1, y2), alpha=0.3)
        plt.plot(x, y, 'ro', label='Solusi Optimal')
        plt.xlabel('Produk A')
        plt.ylabel('Produk B')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.error("Gagal menemukan solusi.")
