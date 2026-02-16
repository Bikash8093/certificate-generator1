import { useState } from "react";

export default function CertificateForm() {
  const [form, setForm] = useState({ name: "", course: "", date: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        alert("Error generating certificate");
        return;
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "certificate.pdf";
      a.click();
    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    }
  };

  return (
    <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
      <h1 className="text-2xl font-bold text-center text-blue-600 mb-6">
        🎓 Certificate Generator
      </h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Full Name"
          className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-400 outline-none"
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Course Name"
          className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-400 outline-none"
          onChange={(e) => setForm({ ...form, course: e.target.value })}
        />
        <input
          type="date"
          className="w-full border rounded-lg p-3 focus:ring-2 focus:ring-blue-400 outline-none"
          onChange={(e) => setForm({ ...form, date: e.target.value })}
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          Generate Certificate
        </button>
      </form>
    </div>
  );
}