"use strict";
let plotlyReady;
function loadPlotly() {
  if (!plotlyReady) plotlyReady = new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "assets/plotly.min.js";
    script.onload = resolve;
    script.onerror = () => { plotlyReady = undefined; script.remove(); reject(new Error("Biblioteca indisponível")); };
    document.head.append(script);
  });
  return plotlyReady;
}
document.querySelectorAll("button[data-chart]").forEach(button => {
  button.addEventListener("click", async () => {
    const figure = button.closest("figure");
    const status = figure.querySelector(".chart-status");
    const target = figure.querySelector(".interactive");
    if (button.dataset.loaded) {
      const show = target.hidden;
      target.hidden = !show;
      figure.querySelector("img").hidden = show;
      button.textContent = show ? "Mostrar figura estática" : "Explorar gráfico interativo";
      button.setAttribute("aria-expanded", String(show));
      if (show) window.Plotly.Plots.resize(target);
      return;
    }
    button.disabled = true; status.textContent = "Carregando versão interativa…";
    try {
      await loadPlotly();
      const response = await fetch(`assets/${button.dataset.chart}.json`);
      if (!response.ok) throw new Error("Dados indisponíveis");
      const plot = await response.json();
      target.hidden = false;
      await window.Plotly.newPlot(target, plot.data, plot.layout, {responsive:true, displaylogo:false, scrollZoom:false, toImageButtonOptions:{format:"svg"}});
      figure.querySelector("img").hidden = true;
      button.dataset.loaded = "true"; button.textContent = "Mostrar figura estática";
      button.setAttribute("aria-expanded", "true"); status.textContent = "Passe o cursor ou toque nos pontos para consultar valores.";
    } catch (error) {
      target.hidden = true;
      status.textContent = "Não foi possível carregar a interação. A figura estática e os dados para download continuam disponíveis.";
    } finally { button.disabled = false; }
  });
});
