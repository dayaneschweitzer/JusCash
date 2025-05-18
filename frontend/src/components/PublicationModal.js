// components/PublicationModal.js
import React from 'react';

const PublicationModal = ({ publication, onClose }) => {
  if (!publication) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Publicação - {publication.processNumber}</h2>
          <button onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <p><strong>Data de publicação:</strong> {publication.publicationDate}</p>
          <p><strong>Autor(es):</strong> {publication.authors}</p>
          <p><strong>Réu:</strong> Instituto Nacional do Seguro Social - INSS</p>
          <p><strong>Advogado(s):</strong> {publication.lawyers}</p>
          <p><strong>Valor principal bruto/líquido:</strong> {publication.principalValue}</p>
          <p><strong>Valor dos juros moratórios:</strong> {publication.moraValue}</p>
          <p><strong>Valor dos honorários advocatícios:</strong> {publication.fees}</p>
          <p><strong>Conteúdo:</strong> {publication.content}</p>
        </div>
        <div className="modal-footer">
          <button onClick={onClose}>Fechar</button>
        </div>
      </div>
    </div>
  );
};

export default PublicationModal;