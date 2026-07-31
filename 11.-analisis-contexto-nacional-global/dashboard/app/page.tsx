"use client";
import { useEffect, useMemo, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

type Row = { country: string; year: number; indicator: string; value: number; growth_pct?: number | null };

export default function Home() {
  const [rows, setRows] = useState<Row[]>([]);
  const [indicator, setIndicator] = useState("Uso de internet (% de población)");
  useEffect(() => { fetch("/data/indicators.json").then(r => r.json()).then(setRows); }, []);
  const indicators = [...new Set(rows.map(r => r.indicator))];
  const selected = rows.filter(r => r.indicator === indicator);
  const countries = [...new Set(selected.map(r => r.country))];
  const chart = useMemo(() => {
    const years = [...new Set(selected.map(r => r.year))].sort();
    return years.map(year => Object.assign({ year }, ...selected.filter(r => r.year === year).map(r => ({ [r.country]: r.value }))));
  }, [selected]);
  const palette = ["#f2b134", "#38bdf8", "#34d399", "#f472b6"];
  return <main>
    <nav><span>ECONOMÍA · UTC</span><a href="#datos">Datos</a><a href="/informe_final.pdf">Informe</a></nav>
    <header><p className="eyebrow">PROYECTO INTEGRADOR</p><h1>Ecuador frente al<br/><em>contexto global</em></h1><p>Una plantilla interactiva para convertir datos verificables en análisis económico comprensible.</p></header>
    <section className="cards">
      <article><small>PAÍSES</small><strong>{countries.length || "—"}</strong><p>Ecuador y economías de referencia</p></article>
      <article><small>PERIODO</small><strong>{selected.length ? Math.min(...selected.map(r => r.year)) + "–" + Math.max(...selected.map(r => r.year)) : "—"}</strong><p>Ventana disponible</p></article>
      <article><small>ÚLTIMA ACTUALIZACIÓN</small><strong>Demo</strong><p>Sustituir con fecha real</p></article>
    </section>
    <section className="panel">
      <div><p className="eyebrow">EVOLUCIÓN COMPARADA</p><h2>{indicator}</h2></div>
      <select value={indicator} onChange={e => setIndicator(e.target.value)}>{indicators.map(x => <option key={x}>{x}</option>)}</select>
      <div className="chart"><ResponsiveContainer width="100%" height={380}><LineChart data={chart}><CartesianGrid stroke="#273142"/><XAxis dataKey="year" stroke="#9aa6b2"/><YAxis stroke="#9aa6b2"/><Tooltip/><Legend/>{countries.map((c,i)=><Line key={c} type="monotone" dataKey={c} stroke={palette[i%palette.length]} strokeWidth={3} dot={false}/>)}</LineChart></ResponsiveContainer></div>
      <p className="note">Interpretación de demostración: el equipo debe explicar aquí tendencias, diferencias, mecanismos, rupturas y límites. Mostrar una curva no equivale a analizarla.</p>
    </section>
    <section id="datos" className="panel"><p className="eyebrow">TRAZABILIDAD</p><h2>Datos utilizados</h2><div className="table"><table><thead><tr><th>País</th><th>Año</th><th>Indicador</th><th>Valor</th></tr></thead><tbody>{selected.slice(-12).map((r,i)=><tr key={i}><td>{r.country}</td><td>{r.year}</td><td>{r.indicator}</td><td>{r.value}</td></tr>)}</tbody></table></div><p className="note">Datos ilustrativos. Deben reemplazarse y citarse antes de la entrega.</p></section>
    <footer>Universidad Técnica de Cotopaxi · Carrera de Economía · 2026</footer>
  </main>;
}
