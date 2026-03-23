import { useState, useEffect } from 'react';

// Models
type User = { name: string; email: string; password: string };
type Train = { train_id: number; train_name: string; source: string; destination: string; total_seats: number; available_seats: number };
type Booking = { booking_id: number; passenger_name: string; train_id: number; seats_booked: number; status: 'Booked' | 'Cancelled' };

// Initial Data
const INITIAL_TRAINS: Train[] = [
  { train_id: 1, train_name: "Rajdhani Express", source: "Delhi", destination: "Mumbai", total_seats: 200, available_seats: 200 },
  { train_id: 2, train_name: "Chennai Express", source: "Chennai", destination: "Bangalore", total_seats: 150, available_seats: 150 },
  { train_id: 3, train_name: "Shatabdi Express", source: "Kolkata", destination: "Delhi", total_seats: 180, available_seats: 180 },
  { train_id: 4, train_name: "Duronto Express", source: "Hyderabad", destination: "Pune", total_seats: 120, available_seats: 120 }
];

export default function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  
  // Storage hooks
  const [users, setUsers] = useState<User[]>([]);
  const [trains, setTrains] = useState<Train[]>(INITIAL_TRAINS);
  const [bookings, setBookings] = useState<Booking[]>([]);

  // Load from local storage
  useEffect(() => {
    const savedUsers = localStorage.getItem('railway_users');
    const savedTrains = localStorage.getItem('railway_trains');
    const savedBookings = localStorage.getItem('railway_bookings');
    
    if (savedUsers) setUsers(JSON.parse(savedUsers));
    if (savedTrains) setTrains(JSON.parse(savedTrains));
    else localStorage.setItem('railway_trains', JSON.stringify(INITIAL_TRAINS));
    if (savedBookings) setBookings(JSON.parse(savedBookings));
  }, []);

  // Save changes
  useEffect(() => { localStorage.setItem('railway_users', JSON.stringify(users)); }, [users]);
  useEffect(() => { localStorage.setItem('railway_trains', JSON.stringify(trains)); }, [trains]);
  useEffect(() => { localStorage.setItem('railway_bookings', JSON.stringify(bookings)); }, [bookings]);

  // Auth State
  const [authTab, setAuthTab] = useState<'login' | 'register'>('login');
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authName, setAuthName] = useState('');

  // Dashboard State
  const [dashTab, setDashTab] = useState<'book' | 'view' | 'cancel'>('book');
  const [bookName, setBookName] = useState('');
  const [bookTrainId, setBookTrainId] = useState('');
  const [bookSeats, setBookSeats] = useState('');
  const [cancelBookingId, setCancelBookingId] = useState('');
  const [alert, setAlert] = useState<{msg: string, type: 'error' | 'success'} | null>(null);

  const showAlert = (msg: string, type: 'error' | 'success') => {
    setAlert({msg, type});
    setTimeout(() => setAlert(null), 3000);
  };

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    if (!authName || !authEmail || !authPassword) return showAlert("Please fill all fields", "error");
    if (users.find(u => u.email === authEmail)) return showAlert("Email already registered!", "error");
    
    setUsers([...users, { name: authName, email: authEmail, password: authPassword }]);
    showAlert("Registered successfully! Please log in.", "success");
    setAuthTab('login');
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!authEmail || !authPassword) return showAlert("Please fill all fields", "error");
    const user = users.find(u => u.email === authEmail && u.password === authPassword);
    
    if (user) {
      setCurrentUser(user);
      showAlert(`Welcome ${user.name}!`, "success");
    } else {
      showAlert("Invalid email or password", "error");
    }
  };

  const handleBookTicket = (e: React.FormEvent) => {
    e.preventDefault();
    if (!bookName || !bookTrainId || !bookSeats) return showAlert("Please fill all fields", "error");
    
    const seats = parseInt(bookSeats);
    const trainId = parseInt(bookTrainId);
    if (isNaN(seats) || seats <= 0) return showAlert("Enter a valid number of seats", "error");

    const trainIndex = trains.findIndex(t => t.train_id === trainId);
    if (trainIndex === -1) return showAlert("Train not found", "error");
    
    const train = trains[trainIndex];
    if (seats > train.available_seats) return showAlert("Not enough available seats", "error");

    const newTrains = [...trains];
    newTrains[trainIndex].available_seats -= seats;
    
    const newBooking: Booking = {
      booking_id: bookings.length > 0 ? bookings[bookings.length - 1].booking_id + 1 : 1,
      passenger_name: bookName,
      train_id: trainId,
      seats_booked: seats,
      status: 'Booked'
    };

    setTrains(newTrains);
    setBookings([...bookings, newBooking]);
    showAlert(`Ticket booked successfully for ${bookName}! ID: ${newBooking.booking_id}`, "success");
    setBookName(''); setBookSeats('');
  };

  const handleCancelTicket = (e: React.FormEvent) => {
    e.preventDefault();
    if (!cancelBookingId) return showAlert("Please enter a booking ID", "error");
    
    const id = parseInt(cancelBookingId);
    const bookingIndex = bookings.findIndex(b => b.booking_id === id);
    
    if (bookingIndex === -1) return showAlert("Booking ID not found", "error");
    
    const booking = bookings[bookingIndex];
    if (booking.status === 'Cancelled') return showAlert("This booking is already cancelled", "error");

    const newBookings = [...bookings];
    newBookings[bookingIndex].status = 'Cancelled';
    
    const trainIndex = trains.findIndex(t => t.train_id === booking.train_id);
    const newTrains = [...trains];
    if (trainIndex !== -1) {
      newTrains[trainIndex].available_seats += booking.seats_booked;
    }

    setBookings(newBookings);
    setTrains(newTrains);
    showAlert(`Booking ${id} cancelled successfully!`, "success");
    setCancelBookingId('');
  };

  // Views
  if (!currentUser) return (
    <div className="app-container">
      <div className="glass-panel">
        <h1 className="title">🚆 Railway System</h1>
        {alert && <div className={`alert ${alert.type}`}>{alert.msg}</div>}
        
        <div className="tabs">
          <button className={`tab ${authTab === 'login' ? 'active' : ''}`} onClick={() => setAuthTab('login')}>Login</button>
          <button className={`tab ${authTab === 'register' ? 'active' : ''}`} onClick={() => setAuthTab('register')}>Register</button>
        </div>

        {authTab === 'login' ? (
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Email Address</label>
              <input type="email" className="input" value={authEmail} onChange={e => setAuthEmail(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input type="password" className="input" value={authPassword} onChange={e => setAuthPassword(e.target.value)} />
            </div>
            <button className="btn">Sign In</button>
          </form>
        ) : (
          <form onSubmit={handleRegister}>
            <div className="form-group">
              <label>Full Name</label>
              <input type="text" className="input" value={authName} onChange={e => setAuthName(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Email Address</label>
              <input type="email" className="input" value={authEmail} onChange={e => setAuthEmail(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input type="password" className="input" value={authPassword} onChange={e => setAuthPassword(e.target.value)} />
            </div>
            <button className="btn">Create Account</button>
          </form>
        )}
      </div>
    </div>
  );

  return (
    <div className="app-container" style={{ maxWidth: '1000px' }}>
      <div className="glass-panel">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h1 className="title" style={{ margin: 0 }}>🚆 Portal</h1>
          <button className="btn danger" style={{ width: 'auto' }} onClick={() => setCurrentUser(null)}>Logout</button>
        </div>

        {alert && <div className={`alert ${alert.type}`}>{alert.msg}</div>}

        <div className="tabs">
          <button className={`tab ${dashTab === 'book' ? 'active' : ''}`} onClick={() => setDashTab('book')}>Book Ticket</button>
          <button className={`tab ${dashTab === 'view' ? 'active' : ''}`} onClick={() => setDashTab('view')}>View Bookings</button>
          <button className={`tab ${dashTab === 'cancel' ? 'active' : ''}`} onClick={() => setDashTab('cancel')}>Cancel Ticket</button>
        </div>

        {dashTab === 'book' && (
          <div>
            <form onSubmit={handleBookTicket} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr auto', gap: '1rem', alignItems: 'end' }}>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Passenger Name</label>
                <input type="text" className="input" value={bookName} onChange={e => setBookName(e.target.value)} />
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Select Train</label>
                <select className="select" value={bookTrainId} onChange={e => setBookTrainId(e.target.value)}>
                  <option value="">-- Choose Train --</option>
                  {trains.map(t => (
                    <option key={t.train_id} value={t.train_id}>{t.train_id} - {t.train_name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Seats</label>
                <input type="number" className="input" min="1" value={bookSeats} onChange={e => setBookSeats(e.target.value)} />
              </div>
              <button className="btn" style={{ height: '45px' }}>Book Ticket</button>
            </form>

            <h3 style={{ marginTop: '2.5rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Available Trains</h3>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Train Name</th>
                    <th>Source</th>
                    <th>Destination</th>
                    <th>Available Seats</th>
                  </tr>
                </thead>
                <tbody>
                  {trains.map(t => (
                    <tr key={t.train_id}>
                      <td>{t.train_name}</td>
                      <td>{t.source}</td>
                      <td>{t.destination}</td>
                      <td>{t.available_seats} / {t.total_seats}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {dashTab === 'view' && (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Booking ID</th>
                  <th>Passenger</th>
                  <th>Train</th>
                  <th>Seats</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {bookings.length === 0 ? (
                  <tr><td colSpan={5} style={{textAlign:'center', color:'gray'}}>No bookings yet.</td></tr>
                ) : bookings.map(b => {
                  const train = trains.find(t => t.train_id === b.train_id);
                  return (
                    <tr key={b.booking_id}>
                      <td>#{b.booking_id}</td>
                      <td>{b.passenger_name}</td>
                      <td>{train?.train_name || 'Unknown'}</td>
                      <td>{b.seats_booked}</td>
                      <td>
                        <span className={`badge ${b.status === 'Booked' ? 'success' : 'danger'}`}>
                          {b.status}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}

        {dashTab === 'cancel' && (
          <form onSubmit={handleCancelTicket} style={{ maxWidth: '400px' }}>
            <div className="form-group">
              <label>Enter Booking ID</label>
              <input type="number" className="input" placeholder="e.g. 1" value={cancelBookingId} onChange={e => setCancelBookingId(e.target.value)} />
            </div>
            <button className="btn danger">Cancel Ticket</button>
          </form>
        )}
      </div>
    </div>
  );
}
