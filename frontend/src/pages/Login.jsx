import React, { useState, useContext } from 'react';
import AuthContext from '../helpers/AuthContext';
import { Button } from '../components';
import { Link, useNavigate } from 'react-router-dom';
import { faSignIn } from '@fortawesome/free-solid-svg-icons';
import api from '../helpers/AxiosClient';


const Login = () => {
    const navigate = useNavigate();
    const authCtx = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await api.post('/auth/login/', { email, password }, false);
            if (response.token) {
                authCtx.login(response);
                navigate('/');
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Invalid credentials. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='flex gap-8 rounded-lg items-center w-full h-[calc(100vh-10rem)]'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container justify-center items-center md:p-16'>
                <div className='text-4xl font-bold text-center'>
                    Welcome to
                    <br />
                    Barracks Merch Store
                </div>
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
                        <label htmlFor='password' className='block text-sm font-medium mb-2'>
                            Password
                        </label>
                        <input
                            type='password'
                            id='password'
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='Enter your password'
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
                        icon={faSignIn} 
                        text={loading ? "Signing in..." : "Sign in"}
                        disabled={loading}
                    />
                </form>

                <div className='mt-4 text-center'>
                    <p>Don't have an account? <Link to='/register' className='text-blue-500 font-bold underline'>Register here</Link></p>
                </div>

                <div className='text-center mt-auto'>
                    <Link to='/policies' className='text-blue-500 font-bold underline'>Refer to our policies</Link>
                </div>
            </div>
        </div>
    );
};
export default Login;

