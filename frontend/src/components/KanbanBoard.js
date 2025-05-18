// KanbanBoard.js
import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import PublicationCard from './PublicationCard';
import PublicationModal from './PublicationModal';
import SearchFilter from './SearchFilter';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import axios from 'axios';
import '../styles/KanbanBoard.css';

const KanbanBoard = ({ user, onLogout }) => {
  const [columns, setColumns] = useState({
    novas: { title: 'Nova Publicação', items: [] },
    lidas: { title: 'Publicação Lida', items: [] },
    enviados: { title: 'Enviar para Advogado Responsável', items: [] },
    concluidas: { title: 'Concluído', items: [] },
  });

  const [selectedPublication, setSelectedPublication] = useState(null);
  const [filters, setFilters] = useState({ query: '', fromDate: '', toDate: '' });

  useEffect(() => {
    fetchPublications();
  }, [filters]);

  const fetchPublications = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/publicacoes', { params: filters });
      const publications = response.data;

      const newColumns = {
        novas: { title: 'Nova Publicação', items: [] },
        lidas: { title: 'Publicação Lida', items: [] },
        enviados: { title: 'Enviar para Advogado Responsável', items: [] },
        concluidas: { title: 'Concluído', items: [] },
      };

      publications.forEach((pub) => {
        newColumns[pub.status || 'novas'].items.push(pub);
      });

      setColumns(newColumns);
    } catch (error) {
      console.error("Erro ao buscar publicações", error);
    }
  };

  const onDragEnd = async (result) => {
    if (!result.destination) return;

    const { source, destination } = result;

    const allowedTransitions = {
      novas: ['lidas'],
      lidas: ['enviados'],
      enviados: ['lidas'],
      concluidas: [],
    };

    const sourceColId = source.droppableId;
    const destColId = destination.droppableId;

    if (sourceColId !== destColId && !allowedTransitions[sourceColId]?.includes(destColId)) {
      alert('Movimentação não permitida');
      return;
    }

    const sourceItems = [...columns[sourceColId].items];
    const destItems = [...columns[destColId].items];
    const [movedItem] = sourceItems.splice(source.index, 1);

    movedItem.status = destColId;
    destItems.splice(destination.index, 0, movedItem);

    setColumns({
      ...columns,
      [sourceColId]: { ...columns[sourceColId], items: sourceItems },
      [destColId]: { ...columns[destColId], items: destItems },
    });

    await axios.patch(`http://127.0.0.1:8000/api/publicacoes/${movedItem.id}`, { status: movedItem.status });
  };

  return (
    <div className="kanban-container">
      <Navbar onLogout={onLogout} />
      <SearchFilter filters={filters} setFilters={setFilters} />

      <DragDropContext onDragEnd={onDragEnd}>
        <div className="kanban-board">
          {Object.entries(columns).map(([colId, colData]) => (
            <Droppable droppableId={colId} key={colId}>
              {(provided) => (
                <div className="kanban-column" ref={provided.innerRef} {...provided.droppableProps}>
                  <h3>{colData.title} <span>{colData.items.length}</span></h3>
                  {colData.items.map((item, index) => (
                    <Draggable draggableId={item.id.toString()} index={index} key={item.id}>
                      {(provided) => (
                        <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                          <PublicationCard publication={item} onClick={() => setSelectedPublication(item)} />
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          ))}
        </div>
      </DragDropContext>

      {selectedPublication && (
        <PublicationModal publication={selectedPublication} onClose={() => setSelectedPublication(null)} />
      )}
    </div>
  );
};

export default KanbanBoard;
