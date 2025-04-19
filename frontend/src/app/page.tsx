type SalesMan = {
  SalesName: string;
};

async function getSalesmen(): Promise<SalesMan[]> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/salesmen`, {
    cache: "no-store", // ⬅️ optional: for fresh data
  });
  return res.json();
}

export default async function Home() {
  const salesmen = await getSalesmen();

  return (
    <div style={{ padding: 24 }}>
      <h1>🧑‍💼 Salesmen</h1>
      <ul>
        {salesmen.map((s) => (
          <li key={s.SalesName}>{s.SalesName}</li>
        ))}
      </ul>
    </div>
  );
}
