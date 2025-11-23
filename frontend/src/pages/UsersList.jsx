import React, { useState, useEffect } from 'react';
import { Loader } from '../components';
import api from '../helpers/AxiosClient';

// VULN-Q7R8S9: User Information Disclosure
const UsersList = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        // VULN-Q7R8S9: No authentication required to view all users
        fetch(`${api._defaults.baseURL}/auth/users/list/`)
            .then(response => response.json())
            .then(data => {
                setUsers(data);
                setLoading(false);
            })
            .catch(err => {
                setError('Failed to load users');
                setLoading(false);
            });
    }, []);

    if (loading) return <Loader />;

    return (
        <div className='flex gap-8 rounded-lg items-center w-full h-[calc(100vh-10rem)]'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container overflow-auto'>
                <div className='text-4xl font-bold text-center mb-6'>
                    Users List
                    <span className='text-sm block text-gray-500 mt-2'>
                        (No authentication required - VULN-Q7R8S9)
                    </span>
                </div>
                <hr className='my-4 border-2 rounded-lg' />
                
                {error && (
                    <div className='text-red-500 text-center mb-4'>
                        {error}
                    </div>
                )}
                
                <div className='overflow-x-auto'>
                    <table className='w-full border-collapse'>
                        <thead>
                            <tr className='bg-gray-100'>
                                <th className='border p-2 text-left'>Name</th>
                                <th className='border p-2 text-left'>Email</th>
                                <th className='border p-2 text-left'>Phone</th>
                                <th className='border p-2 text-left'>Position</th>
                                <th className='border p-2 text-left'>Member</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map((user, index) => (
                                <tr key={index} className='hover:bg-gray-50'>
                                    <td className='border p-2' dangerouslySetInnerHTML={{ __html: user.name }}></td>
                                    <td className='border p-2'>{user.email}</td>
                                    <td className='border p-2'>{user.phone_no || 'N/A'}</td>
                                    <td className='border p-2'>{user.position}</td>
                                    <td className='border p-2'>{user.is_member ? 'Yes' : 'No'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                
                {users.length === 0 && !loading && (
                    <div className='text-center mt-4 text-gray-500'>
                        No users found
                    </div>
                )}
            </div>
        </div>
    );
};

export default UsersList;
