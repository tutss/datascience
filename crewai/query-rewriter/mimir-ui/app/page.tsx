"use client";

import { useState } from 'react';
import axios from 'axios';

export default function Mimir() {
  const [searchQuery, setSearchQuery] = useState('');
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');

  const handleSearch = async () => {
    try {
      const { data } = await axios.post('/api/search', { query: searchQuery });
      setQuery(data.query);
      setResult(data.result);
    } catch (error) {
      setResult('An error occurred. Please try again.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-5xl font-bold mb-6">Mimir</h1>

      <div className="w-full max-w-md flex shadow rounded-full overflow-hidden bg-white">
        <input
          type="text"
          placeholder="Search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-grow px-4 py-2 outline-none"
        />
        <button
          onClick={handleSearch}
          className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white"
        >
          Send
        </button>
      </div>

      {query && (
        <div className="mt-8 max-w-md p-4 bg-white shadow rounded-md">
          <p className="text-gray-800 whitespace-pre-wrap">{query}</p>
        </div>
      )}
      {result && (
        <div className="mt-8 max-w-md p-4 bg-white shadow rounded-md">
          <p className="text-gray-800 whitespace-pre-wrap">{result}</p>
        </div>
      )}
    </div>
  );
}
