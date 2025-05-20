import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FiSearch } from 'react-icons/fi';
import '../styles/SearchFilter.css';
import axios from 'axios';

const formatDate = (date) => {
  if (!date) return '';
  const d = new Date(date);
  const month = '' + (d.getMonth() + 1).toString().padStart(2, '0');
  const day = '' + d.getDate().toString().padStart(2, '0');
  const year = d.getFullYear();
  return [year, month, day].join('-'); // formato yyyy-MM-dd
};

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

  const handleBuscarClick = async () => {
    if (!fromDate || !toDate) {
      alert("Selecione as datas para buscar publicações no DJE");
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/scraper-dje', {
        from_date: formatDate(fromDate),
        to_date: formatDate(toDate)
      });
      console.log("Scraper executado:", response.data);
      setFilters({ query, fromDate, toDate });
    } catch (error) {
      console.error("Erro ao executar scraper:", error);
      alert("Erro ao buscar publicações no DJE.");
    }
  };

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
          <button className="search-button" onClick={handleBuscarClick}>
            <FiSearch />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchFilter;
