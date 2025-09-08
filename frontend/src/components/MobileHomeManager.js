import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../App';

const MobileHomeManager = () => {
  const { token } = useContext(AuthContext);
  const [mobileHomes, setMobileHomes] = useState([]);
  const [stateRequirements, setStateRequirements] = useState([]);
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingHome, setEditingHome] = useState(null);
  const [selectedState, setSelectedState] = useState('CA');
  
  const [formData, setFormData] = useState({
    vin_number: '',
    make: '',
    model: '',
    year: '',
    serial_number: '',
    width: '',
    length: '',
    property_id: '',
    current_owner_name: '',
    current_owner_address: '',
    current_owner_phone: '',
    previous_owner_name: '',
    previous_owner_address: '',
    title_status: 'missing',
    lien_holder: '',
    lien_amount: '',
    acquisition_date: '',
    acquisition_method: '',
    park_location_space: '',
    manufactured_date: '',
    purchase_price: '',
    current_value: '',
    condition_notes: '',
    recovery_status: 'pending',
    recovery_notes: ''
  });

  useEffect(() => {
    if (token) {
      fetchMobileHomes();
      fetchStateRequirements();
      fetchProperties();
    }
  }, [token]);

  const fetchMobileHomes = async () => {
    try {
      const response = await axios.get('/api/mobile-homes', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMobileHomes(response.data);
    } catch (error) {
      console.error('Error fetching mobile homes:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStateRequirements = async () => {
    try {
      const response = await axios.get('/api/state-requirements', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStateRequirements(response.data);
    } catch (error) {
      console.error('Error fetching state requirements:', error);
    }
  };

  const fetchProperties = async () => {
    try {
      const response = await axios.get('/api/properties', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProperties(response.data);
    } catch (error) {
      console.error('Error fetching properties:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingHome) {
        await axios.put(`/api/mobile-homes/${editingHome.id}`, formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } else {
        await axios.post('/api/mobile-homes', formData, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      
      setShowForm(false);
      setEditingHome(null);
      resetForm();
      fetchMobileHomes();
    } catch (error) {
      console.error('Error saving mobile home:', error);
      alert('Error saving mobile home. Please check all fields.');
    }
  };

  const resetForm = () => {
    setFormData({
      vin_number: '',
      make: '',
      model: '',
      year: '',
      serial_number: '',
      width: '',
      length: '',
      property_id: '',
      current_owner_name: '',
      current_owner_address: '',
      current_owner_phone: '',
      previous_owner_name: '',
      previous_owner_address: '',
      title_status: 'missing',
      lien_holder: '',
      lien_amount: '',
      acquisition_date: '',
      acquisition_method: '',
      park_location_space: '',
      manufactured_date: '',
      purchase_price: '',
      current_value: '',
      condition_notes: '',
      recovery_status: 'pending',
      recovery_notes: ''
    });
  };

  const handleEdit = (home) => {
    setEditingHome(home);
    setFormData({
      vin_number: home.vin_number || '',
      make: home.make || '',
      model: home.model || '',
      year: home.year || '',
      serial_number: home.serial_number || '',
      width: home.width || '',
      length: home.length || '',
      property_id: home.property_id || '',
      current_owner_name: home.current_owner_name || '',
      current_owner_address: home.current_owner_address || '',
      current_owner_phone: home.current_owner_phone || '',
      previous_owner_name: home.previous_owner_name || '',
      previous_owner_address: home.previous_owner_address || '',
      title_status: home.title_status || 'missing',
      lien_holder: home.lien_holder || '',
      lien_amount: home.lien_amount || '',
      acquisition_date: home.acquisition_date || '',
      acquisition_method: home.acquisition_method || '',
      park_location_space: home.park_location_space || '',
      manufactured_date: home.manufactured_date || '',
      purchase_price: home.purchase_price || '',
      current_value: home.current_value || '',
      condition_notes: home.condition_notes || '',
      recovery_status: home.recovery_status || 'pending',
      recovery_notes: home.recovery_notes || ''
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this mobile home?')) {
      try {
        await axios.delete(`/api/mobile-homes/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchMobileHomes();
      } catch (error) {
        console.error('Error deleting mobile home:', error);
        alert('Error deleting mobile home.');
      }
    }
  };

  const downloadExcel = async (stateCode, propertyId = null) => {
    try {
      const url = propertyId 
        ? `/api/excel/property/${propertyId}?state_code=${stateCode}`
        : `/api/excel/states/${stateCode}`;
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      });

      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      });
      
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `${stateCode}_VIN_Recovery_${new Date().toISOString().split('T')[0]}.xlsx`;
      link.click();
    } catch (error) {
      console.error('Error downloading Excel:', error);
      alert('Error downloading Excel file.');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Mobile Home VIN/Title Recovery Manager</h2>
      
      {/* Action Buttons */}
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button 
          onClick={() => setShowForm(true)}
          style={{
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer',
            borderRadius: '4px'
          }}
        >
          Add Mobile Home
        </button>
        
        <select 
          value={selectedState} 
          onChange={(e) => setSelectedState(e.target.value)}
          style={{ padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
        >
          {stateRequirements.map(state => (
            <option key={state.state_code} value={state.state_code}>
              {state.state_name}
            </option>
          ))}
        </select>
        
        <button 
          onClick={() => downloadExcel(selectedState)}
          style={{
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer',
            borderRadius: '4px'
          }}
        >
          Download {selectedState} Excel
        </button>

        <button 
          onClick={() => downloadExcel('all')}
          style={{
            backgroundColor: '#17a2b8',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer',
            borderRadius: '4px'
          }}
        >
          Download All States Excel
        </button>
      </div>

      {/* Mobile Homes List */}
      <div style={{ marginBottom: '30px' }}>
        <h3>Mobile Homes ({mobileHomes.length})</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #ddd' }}>
            <thead>
              <tr style={{ backgroundColor: '#f8f9fa' }}>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>VIN</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Make/Model</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Year</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Owner</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Title Status</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Recovery Status</th>
                <th style={{ padding: '12px', border: '1px solid #ddd' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {mobileHomes.map(home => (
                <tr key={home.id}>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>{home.vin_number}</td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>{home.make} {home.model}</td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>{home.year}</td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>{home.current_owner_name}</td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                    <span style={{
                      padding: '4px 8px',
                      borderRadius: '4px',
                      backgroundColor: home.title_status === 'clear' ? '#d4edda' : '#f8d7da',
                      color: home.title_status === 'clear' ? '#155724' : '#721c24'
                    }}>
                      {home.title_status}
                    </span>
                  </td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                    <span style={{
                      padding: '4px 8px',
                      borderRadius: '4px',
                      backgroundColor: 
                        home.recovery_status === 'completed' ? '#d4edda' :
                        home.recovery_status === 'in_progress' ? '#fff3cd' : '#f8d7da',
                      color: 
                        home.recovery_status === 'completed' ? '#155724' :
                        home.recovery_status === 'in_progress' ? '#856404' : '#721c24'
                    }}>
                      {home.recovery_status}
                    </span>
                  </td>
                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                    <button 
                      onClick={() => handleEdit(home)}
                      style={{
                        backgroundColor: '#ffc107',
                        color: 'black',
                        border: 'none',
                        padding: '4px 8px',
                        cursor: 'pointer',
                        borderRadius: '4px',
                        marginRight: '5px'
                      }}
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDelete(home.id)}
                      style={{
                        backgroundColor: '#dc3545',
                        color: 'white',
                        border: 'none',
                        padding: '4px 8px',
                        cursor: 'pointer',
                        borderRadius: '4px'
                      }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Form Modal */}
      {showForm && (
        <div style={{
          position: 'fixed',
          top: '0',
          left: '0',
          right: '0',
          bottom: '0',
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: 'white',
            padding: '30px',
            borderRadius: '8px',
            width: '90%',
            maxWidth: '800px',
            maxHeight: '90vh',
            overflowY: 'auto'
          }}>
            <h3>{editingHome ? 'Edit Mobile Home' : 'Add New Mobile Home'}</h3>
            
            <form onSubmit={handleSubmit}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                <div>
                  <label>VIN Number *:</label>
                  <input
                    type="text"
                    name="vin_number"
                    value={formData.vin_number}
                    onChange={handleInputChange}
                    required
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>
                
                <div>
                  <label>Property:</label>
                  <select
                    name="property_id"
                    value={formData.property_id}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  >
                    <option value="">Select Property</option>
                    {properties.map(prop => (
                      <option key={prop.id} value={prop.id}>
                        {prop.address}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label>Make:</label>
                  <input
                    type="text"
                    name="make"
                    value={formData.make}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Model:</label>
                  <input
                    type="text"
                    name="model"
                    value={formData.model}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Year:</label>
                  <input
                    type="number"
                    name="year"
                    value={formData.year}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Serial Number:</label>
                  <input
                    type="text"
                    name="serial_number"
                    value={formData.serial_number}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Current Owner Name:</label>
                  <input
                    type="text"
                    name="current_owner_name"
                    value={formData.current_owner_name}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Current Owner Phone:</label>
                  <input
                    type="text"
                    name="current_owner_phone"
                    value={formData.current_owner_phone}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div style={{ gridColumn: '1 / -1' }}>
                  <label>Current Owner Address:</label>
                  <textarea
                    name="current_owner_address"
                    value={formData.current_owner_address}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px', minHeight: '60px' }}
                  />
                </div>

                <div>
                  <label>Title Status:</label>
                  <select
                    name="title_status"
                    value={formData.title_status}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  >
                    <option value="missing">Missing</option>
                    <option value="lost">Lost</option>
                    <option value="abandoned">Abandoned</option>
                    <option value="clear">Clear</option>
                  </select>
                </div>

                <div>
                  <label>Recovery Status:</label>
                  <select
                    name="recovery_status"
                    value={formData.recovery_status}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  >
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                    <option value="failed">Failed</option>
                  </select>
                </div>

                <div>
                  <label>Purchase Price:</label>
                  <input
                    type="number"
                    name="purchase_price"
                    value={formData.purchase_price}
                    onChange={handleInputChange}
                    step="0.01"
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Current Value:</label>
                  <input
                    type="number"
                    name="current_value"
                    value={formData.current_value}
                    onChange={handleInputChange}
                    step="0.01"
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Acquisition Date:</label>
                  <input
                    type="date"
                    name="acquisition_date"
                    value={formData.acquisition_date}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>

                <div>
                  <label>Park Location/Space:</label>
                  <input
                    type="text"
                    name="park_location_space"
                    value={formData.park_location_space}
                    onChange={handleInputChange}
                    style={{ width: '100%', padding: '8px', marginTop: '5px' }}
                  />
                </div>
              </div>

              <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingHome(null);
                    resetForm();
                  }}
                  style={{
                    backgroundColor: '#6c757d',
                    color: 'white',
                    border: 'none',
                    padding: '10px 20px',
                    cursor: 'pointer',
                    borderRadius: '4px'
                  }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  style={{
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    padding: '10px 20px',
                    cursor: 'pointer',
                    borderRadius: '4px'
                  }}
                >
                  {editingHome ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MobileHomeManager;