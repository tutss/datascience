"use client";

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

export default function Mimir() {
  const [searchQuery, setSearchQuery] = useState('');
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isTablesOpen, setIsTablesOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [availableTables, setAvailableTables] = useState<string[]>([]);
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [tableInfo, setTableInfo] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const sidebarRef = useRef<HTMLDivElement>(null);

  // Fetch tables when component mounts
  useEffect(() => {
    const fetchTables = async () => {
      try {
        const { data } = await axios.get('/api/tables');
        setAvailableTables(data.tables.split(', '));
      } catch (error) {
        console.error('Error fetching tables:', error);
      }
    };

    fetchTables();
  }, []);

  // Add click outside handler
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (sidebarRef.current && !sidebarRef.current.contains(event.target as Node)) {
        setIsSidebarOpen(false);
      }
    };

    // Add event listener when sidebar is open
    if (isSidebarOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    // Cleanup
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isSidebarOpen]);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const { data } = await axios.post('/api/search', 
        { query: searchQuery },
        { 
          timeout: 300000, // 5 minutes in milliseconds
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
      setQuery(data.query);
      setResult(data.result);
    } catch (error) {
      console.error('Error:', error);
      setResult('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTableClick = async (tableName: string) => {
    try {
      const { data } = await axios.get(`/api/tables/${tableName}`);
      setTableInfo(data.table_info);
      setSelectedTable(tableName);
      setIsModalOpen(true);
    } catch (error) {
      console.error('Error fetching table info:', error);
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <div 
        ref={sidebarRef}
        className={`fixed left-0 top-0 h-full bg-white shadow-lg transition-transform duration-300 ease-in-out ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}
      >
        {/* Hamburger Button - Now inside sidebar */}
        <button
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="p-2 hover:bg-gray-100"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
        <div className="w-64 p-4">
          <button
            onClick={() => setIsTablesOpen(!isTablesOpen)}
            className="w-full text-left px-4 py-2 hover:bg-gray-100 rounded-md flex items-center justify-between"
          >
            <span>Tables</span>
            <svg
              className={`w-4 h-4 transform transition-transform ${isTablesOpen ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {isTablesOpen && (
            <div className="pl-4 mt-2">
              {availableTables.map((table, index) => (
                <div 
                  key={index} 
                  className="px-4 py-2 hover:bg-gray-100 rounded-md cursor-pointer"
                  onClick={() => handleTableClick(table)}
                >
                  {table}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col items-center justify-center">
        {/* Hamburger Button - Only visible when sidebar is closed */}
        {!isSidebarOpen && (
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="fixed top-4 left-4 p-2 rounded-md hover:bg-gray-200"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        )}

        <h1 className="text-5xl font-bold mb-6">Mimir</h1>

        <div className="w-full max-w-2xl flex shadow rounded-full overflow-hidden bg-white">
          <input
            type="text"
            placeholder="Search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !isLoading) {
                handleSearch();
              }
            }}
            className="flex-grow px-6 py-4 text-lg outline-none pr-8"
            disabled={isLoading}
          />
          <button
            onClick={handleSearch}
            className="px-8 py-4 bg-blue-500 hover:bg-blue-600 text-white flex items-center gap-2 text-lg font-medium ml-2"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Loading...</span>
              </>
            ) : (
              'Send'
            )}
          </button>
        </div>

        {(query || result) && (
          <div className="mt-8 max-w-2xl p-4 bg-white shadow rounded-md">
            {query && (
              <p className="text-gray-800 whitespace-pre-wrap">
                <span className="text-lg font-semibold">Query:</span> {query}
              </p>
            )}
            {result && (
              <div>
                <span className="text-lg font-semibold">Result:</span>
                <div className="mt-2 p-2 bg-gray-50 rounded-md overflow-x-auto">
                  <ReactMarkdown>{result}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Table Information: {selectedTable}</h2>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            <div className="mt-4">
              <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto">
                {tableInfo}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
