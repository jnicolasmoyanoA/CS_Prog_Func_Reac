import React, { useEffect, useState } from "react";

const CandleList = () => {
  const [selectedToken, setSelectedToken] = useState("btcusdt");
  const [candles, setCandles] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/candles");

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.token !== selectedToken) return;

      const newCandle = {
        open_time: msg.open_time,
        updated_at: new Date(msg.updated_at).toLocaleTimeString(),
        open: msg.open,
        high: msg.high,
        low: msg.low,
        close: msg.close,
        volume: msg.volume,
      };

      setCandles((prev) => [newCandle, ...prev.slice(0, 4)]);
    };

    return () => ws.close();
  }, [selectedToken]);

  const handleChangeToken = (e) => {
    setCandles([]);
    setSelectedToken(e.target.value);
  };

  return (
    <div style={wrapper}>
      <div style={container}>
        <div style={header}>
          <label style={label}>Token:</label>
          <select
            value={selectedToken}
            onChange={handleChangeToken}
            style={select}
          >
            <option value="btcusdt">BTC</option>
            <option value="ethusdt">ETH</option>
            <option value="adausdt">ADA</option>
            <option value="bnbusdt">BNB</option>
            <option value="xrpusdt">XRP</option>
            <option value="solusdt">SOL</option>
          </select>
        </div>

        {candles.length === 0 ? (
          <p style={{ color: "#ccc" }}>Cargando datos de {selectedToken.toUpperCase()}...</p>
        ) : (
          <table style={table}>
            <thead>
              <tr style={{ backgroundColor: "#333" }}>
                <th style={th}>Hora</th>
                <th style={th}>Open</th>
                <th style={th}>High</th>
                <th style={th}>Low</th>
                <th style={th}>Close</th>
                <th style={th}>Volume</th>
              </tr>
            </thead>
            <tbody>
              {candles.map((c, i) => (
                <tr key={i} style={{ backgroundColor: i % 2 === 0 ? "#2a2a2a" : "#1e1e1e" }}>
                  <td style={td}>{c.updated_at}</td>
                  <td style={td}>{c.open}</td>
                  <td style={td}>{c.high}</td>
                  <td style={td}>{c.low}</td>
                  <td style={td}>{c.close}</td>
                  <td style={td}>{c.volume}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

// Estilos
const wrapper = {
  minHeight: "100vh",
  backgroundColor: "#121212",
  display: "flex",
  justifyContent: "center",
  alignItems: "flex-start",
  paddingTop: 40,
};

const container = {
  width: "95%",
  maxWidth: "1000px",
  backgroundColor: "#1e1e1e",
  color: "#fff",
  padding: 20,
  borderRadius: 10,
  boxShadow: "0 0 10px rgba(0,0,0,0.5)",
};

const header = {
  marginBottom: 20,
  display: "flex",
  alignItems: "center",
};

const label = {
  marginRight: 10,
  fontWeight: "bold",
};

const select = {
  backgroundColor: "#2e2e2e",
  color: "#fff",
  padding: "6px 12px",
  border: "1px solid #555",
  borderRadius: 6,
  outline: "none",
};

const table = {
  width: "100%",
  borderCollapse: "collapse",
  fontSize: "14px",
};

const th = {
  padding: "8px",
  borderBottom: "1px solid #555",
  textAlign: "left",
};

const td = {
  padding: "8px",
  borderBottom: "1px solid #444",
};

export default CandleList;
