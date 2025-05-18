import React from 'react';
import { FaClock, FaCalendarAlt } from 'react-icons/fa';
import '../styles/PublicationCard.css';

const statusColor = {
  novas: '#dc3545',
  lidas: '#28a745',
  enviados: '#ffc107',
  concluidas: '#6c757d'
};

const formatarData = (dataStr) => {
  if (!dataStr) return '';
  const [ano, mes, dia] = dataStr.split('-');
  return `${dia}/${mes}/${ano}`;
};

const calcularTempo = (dataStr) => {
  const data = new Date(dataStr);
  const agora = new Date();
  const diffMs = agora - data;
  const diffHoras = Math.floor(diffMs / (1000 * 60 * 60));
  return `${diffHoras}h`;
};

const PublicationCard = ({ publication, onClick }) => {
  return (
    <div className="publication-card" onClick={onClick}>
      <div className="status-dot" style={{ backgroundColor: statusColor[publication.status] }} />

      <div className="processo">{publication.processNumber}</div>

      <div className="card-info">
        <FaClock className="icon" />
        <span>{calcularTempo(publication.publicationDate)}</span>
      </div>

      <div className="card-info">
        <FaCalendarAlt className="icon" />
        <span>{formatarData(publication.publicationDate)}</span>
      </div>
    </div>
  );
};

export default PublicationCard;

