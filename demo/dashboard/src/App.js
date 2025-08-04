// App.js
import React, { useEffect, useState } from "react";
import mqtt from "mqtt";
import GaugeChart from "react-gauge-chart";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

function LedBar({ count }) {
  const LED_N = 12;
  const ratio = count / LED_N;
  const red = Math.floor(255 * ratio);
  const green = Math.floor(255 * (1 - ratio));
  const color = `rgb(${red}, ${green}, 0)`;

  return (
    <div style={{ display: "flex", gap: 4 }}>
      {[...Array(LED_N)].map((_, i) => (
        <div
          key={i}
          style={{
            width: 18,
            height: 30,
            borderRadius: 4,
            backgroundColor: i < count ? color : "#ccc",
            boxShadow: i < count ? `0 0 5px ${color}` : "none",
            transition: "background-color 0.3s",
          }}
        />
      ))}
    </div>
  );
}

function Widget({ title, children }) {
  return (
    <div
      style={{
        width: 260,
        padding: 20,
        margin: 10,
        border: "1px solid #ddd",
        borderRadius: 10,
        backgroundColor: "#fafafa",
        boxShadow: "2px 2px 6px #eee",
        textAlign: "center",
      }}
    >
      <h3>{title}</h3>
      <div style={{ marginTop: 15 }}>{children}</div>
    </div>
  );
}

export default function App() {
  const [position, setPosition] = useState("-");
  const [angle, setAngle] = useState(0);
  const [leds, setLeds] = useState(0);
  const [distance, setDistance] = useState([]);

  useEffect(() => {
    const client = mqtt.connect("ws://0.0.0.0:1880");

    client.on("connect", () => {
      console.log("Connected to MQTT broker");
      client.subscribe("TOPIC/#");
    });

    client.on("message", (topic, message) => {
      const value = message.toString();
      const now = new Date().toLocaleTimeString();

      if (topic.includes("direction")) setPosition(value);
      else if (topic.includes("angle")) setAngle(parseInt(value));
      else if (topic.includes("leds")) setLeds(parseInt(value));
      else if (topic.includes("distance")) {
        const num = parseFloat(value);
        setDistance((log) => {
          const newLog = [...log, { time: now, value: num }];
          return newLog.length > 30 ? newLog.slice(-30) : newLog;
        });
      }
    });

    return () => client.end();
  }, []);

  const distanceChart = {
    labels: distance.map((d) => d.time),
    datasets: [
      {
        label: "Distance (cm)",
        data: distance.map((d) => d.value),
        fill: false,
        borderColor: "#4BC0C0",
        tension: 0.3,
        pointRadius: 2,
      },
    ],
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif", textAlign: "center" }}>
      <h1>MQTT Dashboard</h1>

      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center" }}>
        <Widget title="Position">
          <div
            style={{
              fontSize: 24,
              fontWeight: "bold",
              color:
                position.toLowerCase() === "center"
                  ? "green"
                  : position.toLowerCase() === "left"
                  ? "orange"
                  : position.toLowerCase() === "right"
                  ? "orange"
                  : "black",
            }}
          >
            {position.toUpperCase()}
          </div>
        </Widget>

        <Widget title="Angle">
        <GaugeChart
          id="angle-gauge"
          nrOfLevels={180}
          percent={angle / 180}
          textColor="#000000"
          hideText={true}
          formatTextValue={() => `${Math.round(angle)}°`}
          animate={false}
        />
          <div style={{ fontSize: 22, marginTop: 10 }}>{angle}°</div>
        </Widget>


        <Widget title="LEDs On">
          <LedBar count={leds} />
          <div style={{ marginTop: 10, fontSize: 20 }}>{leds} LEDs</div>
        </Widget>
      </div>

      <div style={{ marginTop: 40, maxWidth: 900, marginLeft: "auto", marginRight: "auto" }}>
        <h2>Distance</h2>
        <Line
          data={distanceChart}
          options={{
            responsive: true,
            animation: false,
            scales: {
              y: {
                min: 0,
                title: { display: true, text: "cm" },
              },
              x: {
                title: { display: true, text: "Time" },
              },
            },
          }}
        />
      </div>
    </div>
  );
}
