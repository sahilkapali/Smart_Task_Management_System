import { useEffect, useState } from 'react';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const { logout } = useAuth();

  const fetchTasks = async () => {
    const res = await api.get('tasks/');
    setTasks(res.data);
  };

  const addTask = async (e) => {
    e.preventDefault();
    await api.post('tasks/', { title, description: "Task created via React", status: false });
    setTitle('');
    fetchTasks();
  };

  const toggleTask = async (task) => {
    await api.patch(`tasks/${task.id}/`, { status: !task.status });
    fetchTasks();
  };

  const deleteTask = async (id) => {
    await api.delete(`tasks/${id}/`);
    fetchTasks();
  };

  useEffect(() => { fetchTasks(); }, []);

  return (
    <div className="dashboard-container">
      <div className="nav">
        <h1>Smart Tasks</h1>
        <button onClick={logout} style={{background: '#475569'}}>Logout</button>
      </div>

      <form onSubmit={addTask} style={{display: 'flex', gap: '10px'}}>
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Add a new task..." required />
        <button type="submit" style={{height: '45px', marginTop: '8px'}}>Add</button>
      </form>

      <div>
        {tasks.map(t => (
          <div key={t.id} className={`task-card ${t.status ? 'completed' : ''}`}>
            <span style={{cursor: 'pointer'}} onClick={() => toggleTask(t)}>
              {t.status ? '✅ ' : '⭕ '} {t.title}
            </span>
            <button className="btn-delete" onClick={() => deleteTask(t.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}