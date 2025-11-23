import React, { useState, useContext } from 'react';
import { Button } from '../components';
import { useNavigate } from 'react-router-dom';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import api from '../helpers/AxiosClient';
import AuthContext from '../helpers/AuthContext';

// VULN-M4N5O6 & VULN-P7Q8R9: Clickjacking vulnerability
const DeleteAccount = () => {
    const navigate = useNavigate();
    const authCtx = useContext(AuthContext);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [confirm, setConfirm] = useState('');

    const handleDelete = async (e) => {
        e.preventDefault();
        
        if (confirm !== 'DELETE') {
            setError('Please type DELETE to confirm');
            return;
        }

        setLoading(true);
        setError('');

        try {
            await api.post('/auth/delete-account/', {});
            alert('Account deleted successfully');
            authCtx.logout();
            navigate('/');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to delete account');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='flex gap-8 rounded-lg items-center w-full h-[calc(100vh-10rem)]'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container justify-center items-center md:p-16'>
                <div className='text-4xl font-bold text-center text-red-600'>
                    Delete Account
                </div>
                <p className='text-gray-600 mt-2 text-center'>
                    This action cannot be undone. All your data will be permanently deleted.
                </p>
                <hr className='my-6 border-2 rounded-lg w-1/2' />
                
                <form onSubmit={handleDelete} className='w-full max-w-md space-y-4'>
                    <div>
                        <label htmlFor='confirm' className='block text-sm font-medium mb-2'>
                            Type "DELETE" to confirm
                        </label>
                        <input
                            type='text'
                            id='confirm'
                            value={confirm}
                            onChange={(e) => setConfirm(e.target.value)}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-red-500'
                            placeholder='Type DELETE'
                        />
                    </div>
                    
                    {error && (
                        <div className='text-red-500 text-sm text-center'>
                            {error}
                        </div>
                    )}
                    
                    <Button 
                        type="submit" 
                        className="py-2 w-full bg-red-600 hover:bg-red-700" 
                        isActive 
                        icon={faTrash} 
                        text={loading ? "Deleting..." : "Delete Account"}
                        disabled={loading}
                    />
                </form>

                <div className='mt-4 text-center'>
                    <button 
                        onClick={() => navigate('/')} 
                        className='text-blue-500 font-bold underline'
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    );
};

export default DeleteAccount;
