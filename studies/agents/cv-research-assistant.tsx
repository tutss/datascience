import React, { useState } from 'react';
import { Search, FileText, ExternalLink, BookOpen, TrendingUp, Users, Calendar, Download } from 'lucide-react';

const ResearchAssistant = () => {
  const [searchTopic, setSearchTopic] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [papers, setPapers] = useState([]);
  const [summary, setSummary] = useState('');
  const [error, setError] = useState('');

  const searchPapers = async () => {
    if (!searchTopic.trim()) {
      setError('Please enter a research topic');
      return;
    }

    setIsSearching(true);
    setError('');
    setPapers([]);
    setSummary('');

    try {
      const prompt = `You are an expert computer vision and face recognition researcher. Search for and analyze 5 recent, high-quality research papers related to "${searchTopic}" in computer vision and face recognition.

For each paper, provide the following information in JSON format:
- title: Paper title
- authors: List of authors
- venue: Publication venue (conference/journal)
- year: Publication year
- abstract: Brief abstract/summary
- keyContributions: Main contributions and innovations
- methodology: Brief description of methods used
- datasets: Datasets mentioned or used
- arxivLink: If available, arXiv link (use format: https://arxiv.org/abs/[paper_id])
- significance: Why this paper is important to the field

After the papers, provide a "researchSummary" with:
- commonThemes: Key themes across the papers
- trendingTechniques: Popular methods and approaches
- futureDirections: Emerging research directions
- readingOrder: Suggested reading order with brief reasoning

Respond with a JSON object containing:
{
  "papers": [array of 5 papers with above structure],
  "researchSummary": {
    "commonThemes": [array of themes],
    "trendingTechniques": [array of techniques],
    "futureDirections": [array of directions],
    "readingOrder": [array of objects with {paperIndex, reason}]
  }
}

Focus on papers from top-tier venues like CVPR, ICCV, ECCV, TPAMI, etc. Prioritize recent work (2022-2024) unless classic foundational papers are relevant.

YOUR ENTIRE RESPONSE MUST BE A SINGLE, VALID JSON OBJECT. DO NOT INCLUDE ANY TEXT OUTSIDE THE JSON STRUCTURE.`;

      const response = await window.claude.complete(prompt);
      const data = JSON.parse(response);

      setPapers(data.papers || []);
      setSummary(data.researchSummary || {});

    } catch (error) {
      console.error('Search error:', error);
      setError('Failed to search papers. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      searchPapers();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            CV Research Assistant
          </h1>
          <p className="text-gray-600 text-lg">
            Discover cutting-edge papers in Computer Vision & Face Recognition
          </p>
        </div>

        {/* Search Section */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={searchTopic}
                onChange={(e) => setSearchTopic(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter your research topic (e.g., 'face recognition transformers', 'deepfake detection', 'facial expression analysis')"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                disabled={isSearching}
              />
            </div>
            <button
              onClick={searchPapers}
              disabled={isSearching}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-8 py-3 rounded-lg flex items-center gap-2 font-semibold transition-colors"
            >
              {isSearching ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Searching...
                </>
              ) : (
                <>
                  <Search size={20} />
                  Search Papers
                </>
              )}
            </button>
          </div>
          {error && (
            <p className="text-red-600 mt-2 text-sm">{error}</p>
          )}
        </div>

        {/* Research Summary */}
        {summary && Object.keys(summary).length > 0 && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <TrendingUp className="text-blue-600" />
              Research Overview
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Common Themes</h3>
                <ul className="text-gray-600 space-y-1">
                  {summary.commonThemes?.map((theme, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-blue-500 mt-1">•</span>
                      {theme}
                    </li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Trending Techniques</h3>
                <ul className="text-gray-600 space-y-1">
                  {summary.trendingTechniques?.map((technique, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-green-500 mt-1">•</span>
                      {technique}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {summary.futureDirections && summary.futureDirections.length > 0 && (
              <div className="mt-4">
                <h3 className="font-semibold text-gray-700 mb-2">Future Research Directions</h3>
                <ul className="text-gray-600 space-y-1">
                  {summary.futureDirections.map((direction, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-purple-500 mt-1">•</span>
                      {direction}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {summary.readingOrder && summary.readingOrder.length > 0 && (
              <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <BookOpen size={18} />
                  Suggested Reading Order
                </h3>
                <ol className="text-gray-600 space-y-2">
                  {summary.readingOrder.map((item, idx) => (
                    <li key={idx} className="flex gap-3">
                      <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-semibold">
                        {idx + 1}
                      </span>
                      <div>
                        <span className="font-medium">Paper {item.paperIndex + 1}</span>
                        <p className="text-sm text-gray-500">{item.reason}</p>
                      </div>
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        )}

        {/* Papers Grid */}
        {papers.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <FileText className="text-blue-600" />
              Research Papers ({papers.length})
            </h2>
            
            {papers.map((paper, index) => (
              <div key={index} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
                <div className="flex flex-col lg:flex-row gap-6">
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-xl font-bold text-gray-800 leading-tight">
                        {paper.title}
                      </h3>
                      <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium ml-4 whitespace-nowrap">
                        Paper {index + 1}
                      </span>
                    </div>
                    
                    <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3">
                      <div className="flex items-center gap-1">
                        <Users size={16} />
                        {Array.isArray(paper.authors) ? paper.authors.join(', ') : paper.authors}
                      </div>
                      <div className="flex items-center gap-1">
                        <Calendar size={16} />
                        {paper.venue} {paper.year}
                      </div>
                    </div>

                    <p className="text-gray-700 mb-4 leading-relaxed">
                      {paper.abstract}
                    </p>

                    <div className="grid md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Key Contributions</h4>
                        <p className="text-gray-600 text-sm">{paper.keyContributions}</p>
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Methodology</h4>
                        <p className="text-gray-600 text-sm">{paper.methodology}</p>
                      </div>
                    </div>

                    {paper.datasets && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-gray-700 mb-2">Datasets Used</h4>
                        <p className="text-gray-600 text-sm">{paper.datasets}</p>
                      </div>
                    )}

                    <div className="bg-gray-50 p-3 rounded-lg mb-4">
                      <h4 className="font-semibold text-gray-700 mb-1">Significance</h4>
                      <p className="text-gray-600 text-sm">{paper.significance}</p>
                    </div>

                    <div className="flex gap-3">
                      {paper.arxivLink && (
                        <a
                          href={paper.arxivLink}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="bg-red-100 hover:bg-red-200 text-red-700 px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium transition-colors"
                        >
                          <ExternalLink size={16} />
                          arXiv
                        </a>
                      )}
                      <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium transition-colors">
                        <Download size={16} />
                        Save for Later
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!papers.length && !isSearching && (
          <div className="text-center py-12">
            <FileText size={64} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              Ready to discover research papers?
            </h3>
            <p className="text-gray-500">
              Enter a computer vision or face recognition topic above to get started
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResearchAssistant;