import React from 'react';
import '../styles/PublicationCard.css';

const statusColors = {
  novas: '#e74c3c',        // vermelho
  lidas: '#2ecc71',        // verde
  enviados: '#f1c40f',     // amarelo
  concluidas: '#bdc3c7'    // cinza
};

const PublicationCard = ({ publication, onClick }) => {
  const dotColor = statusColors[publication.status] || '#ccc';

  return (
    <div className="publication-card" onClick={onClick}>
      <span className="status-dot" style={{ backgroundColor: dotColor }}></span>
      <div><strong>{publication.processNumber}</strong></div>
      <div>Data: {publication.publicationDate}</div>
      <div>Última atualização: {publication.lastUpdate || publication.publicationDate}</div>
    </div>
  );
};

export default PublicationCard;
