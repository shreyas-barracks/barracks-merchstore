import React, { useState } from 'react';
import { Button } from '../components';
import { Link, useNavigate } from 'react-router-dom';
import { faKey } from '@fortawesome/free-solid-svg-icons';
import api from '../helpers/AxiosClient';

// VULN-L1M2N3: Insecure Password Change - Frontend component
const ForgotPassword = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        try {
            // VULN-L1M2N3: No authentication or verification required
            const response = await api.post('/auth/change-password/', {
                email,
                new_password: newPassword
            }, false);
            
            setSuccess('Password changed successfully! Redirecting to login...');
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to change password');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='flex gap-8 rounded-lg items-center w-full h-[calc(100vh-10rem)]'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container justify-center items-center md:p-16'>
                <div className='text-4xl font-bold text-center'>
                    Reset Password
                </div>
                <p className='text-gray-600 mt-2 text-center'>
                    Enter your email and new password
                </p>
                <hr className='my-6 border-2 rounded-lg w-1/2' />
                
                <form onSubmit={handleSubmit} className='w-full max-w-md space-y-4'>
                    <div>
                        <label htmlFor='email' className='block text-sm font-medium mb-2'>
                            Email
                        </label>
                        <input
                            type='email'
                            id='email'
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Enter your email'
                        />
                    </div>
                    <div>
                        <label htmlFor='newPassword' className='block text-sm font-medium mb-2'>
                            New Password
                        </label>
                        <input
                            type='password'
                            id='newPassword'
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Enter new password'
                        />
                    </div>
                    
                    {error && (
                        <div className='text-red-500 text-sm text-center'>
                            {error}
                        </div>
                    )}
                    
                    {success && (
                        <div className='text-green-500 text-sm text-center'>
                            {success}
                        </div>
                    )}
                    
                    <Button 
                        type="submit" 
                        className="py-2 w-full" 
                        isActive 
                        icon={faKey} 
                        text={loading ? "Changing..." : "Change Password"}
                        disabled={loading}
                    />
                </form>

                <div className='mt-4 text-center'>
                    <p>Remember your password? <Link to='/login' className='text-blue-500 font-bold underline'>Login here</Link></p>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
