import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function VerifyCertificate() {
  const { id } = useParams();
  const [cert, setCert] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/verify/${id}`)
      .then((res) => res.json())
      .then((data) => setCert(data))
      .catch((err) => console.error(err));
  }, [id]);

  if (!cert) {
    return (
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <p className="text-xl text-gray-600">Loading certificate...</p>
      </div>
    );
  }

  if (cert.error) {
    return (
      <div className="flex justify-center items-center h-screen bg-red-100">
        <p className="text-xl text-red-600">{cert.error}</p>
      </div>
    );
  }

  return (
    <div className="flex justify-center items-center h-screen bg-gradient-to-r from-green-100 to-green-300">
      <div className="bg-white shadow-xl rounded-lg p-8 max-w-lg w-full text-center">
        <h1 className="text-3xl font-bold text-green-600 mb-6">
          🎓 Verified Certificate
        </h1>
        <p className="text-xl font-semibold mb-2">Name: {cert.name}</p>
        <p className="text-lg mb-2">Course: {cert.course}</p>
        <p className="text-lg mb-4">Date: {cert.date}</p>
        <p className="text-sm text-gray-500">Certificate ID: {cert.id}</p>
      </div>
    </div>
  );
}