import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

df = pd.read_excel("libro_ingresos_egresos.xlsx")
df["mes"] = df["fecha"].dt.to_period("M").astype(str)

resumen = df.pivot_table(index="mes", columns="tipo", values="monto", aggfunc="sum", fill_value=0)
resumen["saldo"] = resumen["Ingreso"] - resumen["Egreso"]

por_categoria = df.groupby(["tipo", "categoria"])["monto"].sum().reset_index()

print(resumen)
print(por_categoria)

with pd.ExcelWriter("reporte_mensual.xlsx") as writer:
    resumen.to_excel(writer, sheet_name="Resumen mensual")
    por_categoria.to_excel(writer, sheet_name="Por categoría", index=False)

meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
x = range(len(resumen))
ancho = 0.38

fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor("#F7F9FC")
ax.set_facecolor("#F7F9FC")

ax.bar([i - ancho / 2 for i in x], resumen["Ingreso"], ancho, label="Ingresos", color="#2E86AB")
ax.bar([i + ancho / 2 for i in x], resumen["Egreso"], ancho, label="Egresos", color="#E4572E")
ax.plot(x, resumen["saldo"], color="#2B2D42", marker="o", linewidth=2, label="Saldo", zorder=3)

for i, v in enumerate(resumen["saldo"]):
    ax.annotate(f"${v/1000:,.0f}k", (i, v), textcoords="offset points", xytext=(0, 12),
                ha="center", fontsize=9, color="#2B2D42", fontweight="bold", zorder=4,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#2B2D42", lw=0.8, alpha=0.95))

ax.set_xticks(list(x))
ax.set_xticklabels(meses)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1_000_000:.1f}M"))
ax.set_title("Ingresos, egresos y saldo por mes", fontsize=15, fontweight="bold", loc="left", pad=15)
ax.set_ylabel("Monto (CLP)")
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.08))
fig.text(0.99, 0.01, "Datos de ejemplo", ha="right", fontsize=8, color="gray", style="italic")

plt.tight_layout()
plt.savefig("grafico_mensual.png", dpi=150)
plt.show()