import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FiSearch } from 'react-icons/fi';
import '../styles/SearchFilter.css';

const SearchFilter = ({ filters, setFilters }) => {
  const [query, setQuery] = useState(filters.query);
  const [fromDate, setFromDate] = useState(filters.fromDate);
  const [toDate, setToDate] = useState(filters.toDate);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      setFilters({ query, fromDate, toDate });
    }, 500);
    return () => clearTimeout(timeoutId);
  }, [query, fromDate, toDate, setFilters]);

  return (
    <div className="search-filter">
      <div className="search-section">
        <label className="label-title">Pesquisar</label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Digite o número do Processo"
        />
      </div>

      <div className="date-group">
        <label className="label-title"></label>
        <div className="date-section">
          <div>
            <span>De:</span>
            <DatePicker
              selected={fromDate}
              onChange={(date) => setFromDate(date)}
              dateFormat="dd/MM/yyyy"
              placeholderText="DD/MM/AAAA"
              locale="pt-BR"
            />
          </div>
          <div>
            <span>Até:</span>
            <DatePicker
              selected={toDate}
              onChange={(date) => setToDate(date)}
              dateFormat="dd/MM/yyyy"
              placeholderText="DD/MM/AAAA"
              locale="pt-BR"
            />
          </div>
          <button className="search-button" onClick={() => setFilters({ query, fromDate, toDate })}>
            <FiSearch />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchFilter;
