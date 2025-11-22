import React, { useState } from 'react';
import { Button } from '../components';
import { Link, useNavigate } from 'react-router-dom';
import { faUserPlus } from '@fortawesome/free-solid-svg-icons';
import api from '../helpers/AxiosClient';


const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone_no: '',
        password: '',
        password2: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.password2) {
            setError('Passwords do not match');
            return;
        }

        setLoading(true);

        try {
            const response = await api.post('/auth/register/', formData, false);
            if (response.token) {
                // Registration successful, redirect to login
                navigate('/login');
            }
        } catch (err) {
            const errorMsg = err.response?.data;
            if (typeof errorMsg === 'object') {
                // Handle field-specific errors
                const firstError = Object.values(errorMsg)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else {
                setError('Registration failed. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='flex gap-8 rounded-lg items-center w-full h-[calc(100vh-10rem)]'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container justify-center items-center md:p-16 overflow-y-auto'>
                <div className='text-4xl font-bold text-center mb-6'>
                    Create Account
                    <br />
                    Barracks Merch Store
                </div>
                <hr className='my-6 border-2 rounded-lg w-1/2' />
                
                <form onSubmit={handleSubmit} className='w-full max-w-md space-y-4'>
                    <div>
                        <label htmlFor='name' className='block text-sm font-medium mb-2'>
                            Full Name
                        </label>
                        <input
                            type='text'
                            id='name'
                            name='name'
                            value={formData.name}
                            onChange={handleChange}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Enter your full name'
                        />
                    </div>
                    <div>
                        <label htmlFor='email' className='block text-sm font-medium mb-2'>
                            Email
                        </label>
                        <input
                            type='email'
                            id='email'
                            name='email'
                            value={formData.email}
                            onChange={handleChange}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Enter your email'
                        />
                    </div>
                    <div>
                        <label htmlFor='phone_no' className='block text-sm font-medium mb-2'>
                            Phone Number (Optional)
                        </label>
                        <input
                            type='tel'
                            id='phone_no'
                            name='phone_no'
                            value={formData.phone_no}
                            onChange={handleChange}
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Enter your phone number'
                        />
                    </div>
                    <div>
                        <label htmlFor='password' className='block text-sm font-medium mb-2'>
                            Password
                        </label>
                        <input
                            type='password'
                            id='password'
                            name='password'
                            value={formData.password}
                            onChange={handleChange}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Enter your password'
                        />
                    </div>
                    <div>
                        <label htmlFor='password2' className='block text-sm font-medium mb-2'>
                            Confirm Password
                        </label>
                        <input
                            type='password'
                            id='password2'
                            name='password2'
                            value={formData.password2}
                            onChange={handleChange}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Confirm your password'
                        />
                    </div>
                    
                    {error && (
                        <div className='text-red-500 text-sm text-center'>
                            {error}
                        </div>
                    )}
                    
                    <Button 
                        type="submit" 
                        className="py-2 w-full" 
                        isActive 
                        icon={faUserPlus} 
                        text={loading ? "Creating account..." : "Register"}
                        disabled={loading}
                    />
                </form>

                <div className='mt-4 text-center'>
                    <p>Already have an account? <Link to='/login' className='text-blue-500 font-bold underline'>Sign in here</Link></p>
                </div>

                <div className='text-center mt-auto'>
                    <Link to='/policies' className='text-blue-500 font-bold underline'>Refer to our policies</Link>
                </div>
            </div>
        </div>
    );
};

export default Register;
